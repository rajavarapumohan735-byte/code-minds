from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from models.schemas import PaperCreate, PaperResponse, PaperImport, SearchQuery
from utils.auth import get_current_user
from utils.ai import generate_embedding
from utils.pdf_parser import extract_text_from_pdf_bytes
from database import engine
from sqlalchemy import text
from typing import List
from datetime import datetime
import httpx

router = APIRouter(prefix="/papers", tags=["Papers"])

@router.post("/search", response_model=List[PaperResponse])
async def search_papers(
    search_query: SearchQuery,
    current_user: str = Depends(get_current_user)
):
    query = search_query.query
    limit = search_query.limit

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://export.arxiv.org/api/query",
                params={
                    "search_query": f"all:{query}",
                    "start": 0,
                    "max_results": limit
                },
                timeout=30.0
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Error fetching papers from arXiv"
                )

            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)

            namespace = {
                'atom': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }

            papers = []
            for entry in root.findall('atom:entry', namespace):
                title_elem = entry.find('atom:title', namespace)
                summary_elem = entry.find('atom:summary', namespace)
                published_elem = entry.find('atom:published', namespace)
                id_elem = entry.find('atom:id', namespace)

                authors = []
                for author in entry.findall('atom:author', namespace):
                    name_elem = author.find('atom:name', namespace)
                    if name_elem is not None and name_elem.text:
                        authors.append(name_elem.text)

                arxiv_id = id_elem.text.split('/abs/')[-1] if id_elem is not None else None

                paper_data = PaperCreate(
                    title=title_elem.text.strip() if title_elem is not None else "Untitled",
                    authors=authors,
                    abstract=summary_elem.text.strip() if summary_elem is not None else "",
                    publication_date=published_elem.text.split('T')[0] if published_elem is not None else None,
                    arxiv_id=arxiv_id,
                    pdf_url=f"https://arxiv.org/pdf/{arxiv_id}.pdf" if arxiv_id else None
                )

                with engine.connect() as conn:
                    embedding = generate_embedding(paper_data.title + " " + paper_data.abstract)

                    result = conn.execute(
                        text("""
                            INSERT INTO papers (title, authors, abstract, publication_date, pdf_url, arxiv_id, embedding, created_at)
                            VALUES (:title, :authors, :abstract, :publication_date, :pdf_url, :arxiv_id, :embedding, :created_at)
                            ON CONFLICT (arxiv_id) WHERE arxiv_id IS NOT NULL DO UPDATE
                            SET title = EXCLUDED.title
                            RETURNING id, title, authors, abstract, publication_date, pdf_url, arxiv_id, created_at
                        """),
                        {
                            "title": paper_data.title,
                            "authors": paper_data.authors,
                            "abstract": paper_data.abstract,
                            "publication_date": paper_data.publication_date,
                            "pdf_url": paper_data.pdf_url,
                            "arxiv_id": paper_data.arxiv_id,
                            "embedding": str(embedding),
                            "created_at": datetime.utcnow()
                        }
                    )
                    conn.commit()
                    paper = result.fetchone()

                    papers.append(PaperResponse(
                        id=str(paper.id),
                        title=paper.title,
                        authors=paper.authors,
                        abstract=paper.abstract,
                        publication_date=paper.publication_date,
                        pdf_url=paper.pdf_url,
                        arxiv_id=paper.arxiv_id,
                        doi=None,
                        created_at=paper.created_at
                    ))

            return papers

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching papers: {str(e)}"
        )

@router.post("/import", status_code=status.HTTP_201_CREATED)
async def import_paper(
    paper_import: PaperImport,
    current_user: str = Depends(get_current_user)
):
    with engine.connect() as conn:
        workspace = conn.execute(
            text("SELECT id FROM workspaces WHERE id = :workspace_id AND user_id = :user_id"),
            {"workspace_id": paper_import.workspace_id, "user_id": current_user}
        ).fetchone()

        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found"
            )

        paper = conn.execute(
            text("SELECT id FROM papers WHERE id = :paper_id"),
            {"paper_id": paper_import.paper_id}
        ).fetchone()

        if not paper:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paper not found"
            )

        try:
            conn.execute(
                text("""
                    INSERT INTO workspace_papers (workspace_id, paper_id, added_at)
                    VALUES (:workspace_id, :paper_id, :added_at)
                """),
                {
                    "workspace_id": paper_import.workspace_id,
                    "paper_id": paper_import.paper_id,
                    "added_at": datetime.utcnow()
                }
            )
            conn.commit()
        except Exception as e:
            if "unique" in str(e).lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Paper already in workspace"
                )
            raise e

        return {"message": "Paper imported successfully"}

@router.get("/workspace/{workspace_id}", response_model=List[PaperResponse])
async def get_workspace_papers(
    workspace_id: str,
    current_user: str = Depends(get_current_user)
):
    with engine.connect() as conn:
        workspace = conn.execute(
            text("SELECT id FROM workspaces WHERE id = :workspace_id AND user_id = :user_id"),
            {"workspace_id": workspace_id, "user_id": current_user}
        ).fetchone()

        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found"
            )

        result = conn.execute(
            text("""
                SELECT p.id, p.title, p.authors, p.abstract, p.publication_date,
                       p.pdf_url, p.arxiv_id, p.doi, p.created_at
                FROM papers p
                JOIN workspace_papers wp ON p.id = wp.paper_id
                WHERE wp.workspace_id = :workspace_id
                ORDER BY wp.added_at DESC
            """),
            {"workspace_id": workspace_id}
        )
        papers = result.fetchall()

        return [
            PaperResponse(
                id=str(paper.id),
                title=paper.title,
                authors=paper.authors,
                abstract=paper.abstract,
                publication_date=paper.publication_date,
                pdf_url=paper.pdf_url,
                arxiv_id=paper.arxiv_id,
                doi=paper.doi,
                created_at=paper.created_at
            )
            for paper in papers
        ]

@router.post("/upload", response_model=PaperResponse)
async def upload_paper(
    file: UploadFile = File(...),
    title: str = "",
    authors: str = "",
    current_user: str = Depends(get_current_user)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )

    try:
        contents = await file.read()
        extracted_text = extract_text_from_pdf_bytes(contents)

        authors_list = [a.strip() for a in authors.split(",")] if authors else []

        embedding = generate_embedding(title + " " + extracted_text[:1000])

        with engine.connect() as conn:
            result = conn.execute(
                text("""
                    INSERT INTO papers (title, authors, abstract, pdf_text, embedding, created_at)
                    VALUES (:title, :authors, :abstract, :pdf_text, :embedding, :created_at)
                    RETURNING id, title, authors, abstract, publication_date, pdf_url, arxiv_id, doi, created_at
                """),
                {
                    "title": title or file.filename,
                    "authors": authors_list,
                    "abstract": extracted_text[:500],
                    "pdf_text": extracted_text,
                    "embedding": str(embedding),
                    "created_at": datetime.utcnow()
                }
            )
            conn.commit()
            paper = result.fetchone()

            return PaperResponse(
                id=str(paper.id),
                title=paper.title,
                authors=paper.authors,
                abstract=paper.abstract,
                publication_date=paper.publication_date,
                pdf_url=paper.pdf_url,
                arxiv_id=paper.arxiv_id,
                doi=paper.doi,
                created_at=paper.created_at
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing PDF: {str(e)}"
        )

@router.delete("/workspace/{workspace_id}/paper/{paper_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_paper_from_workspace(
    workspace_id: str,
    paper_id: str,
    current_user: str = Depends(get_current_user)
):
    with engine.connect() as conn:
        workspace = conn.execute(
            text("SELECT id FROM workspaces WHERE id = :workspace_id AND user_id = :user_id"),
            {"workspace_id": workspace_id, "user_id": current_user}
        ).fetchone()

        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found"
            )

        result = conn.execute(
            text("DELETE FROM workspace_papers WHERE workspace_id = :workspace_id AND paper_id = :paper_id"),
            {"workspace_id": workspace_id, "paper_id": paper_id}
        )
        conn.commit()

        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paper not found in workspace"
            )

        return None
