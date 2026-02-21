from fastapi import APIRouter, HTTPException, status, Depends
from models.schemas import (
    ChatRequest, ChatResponse, MessageResponse,
    ConversationCreate, ConversationResponse
)
from utils.auth import get_current_user
from utils.ai import generate_chat_response, build_context_from_papers, create_research_assistant_prompt
from database import engine
from sqlalchemy import text
from typing import List
from datetime import datetime

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation_data: ConversationCreate,
    current_user: str = Depends(get_current_user)
):
    with engine.connect() as conn:
        workspace = conn.execute(
            text("SELECT id FROM workspaces WHERE id = :workspace_id AND user_id = :user_id"),
            {"workspace_id": conversation_data.workspace_id, "user_id": current_user}
        ).fetchone()

        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found"
            )

        result = conn.execute(
            text("""
                INSERT INTO conversations (workspace_id, title, created_at, updated_at)
                VALUES (:workspace_id, :title, :created_at, :updated_at)
                RETURNING id, workspace_id, title, created_at, updated_at
            """),
            {
                "workspace_id": conversation_data.workspace_id,
                "title": conversation_data.title,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        )
        conn.commit()
        conversation = result.fetchone()

        return ConversationResponse(
            id=str(conversation.id),
            workspace_id=str(conversation.workspace_id),
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        )

@router.get("/conversations/workspace/{workspace_id}", response_model=List[ConversationResponse])
async def get_workspace_conversations(
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
                SELECT id, workspace_id, title, created_at, updated_at
                FROM conversations
                WHERE workspace_id = :workspace_id
                ORDER BY updated_at DESC
            """),
            {"workspace_id": workspace_id}
        )
        conversations = result.fetchall()

        return [
            ConversationResponse(
                id=str(conv.id),
                workspace_id=str(conv.workspace_id),
                title=conv.title,
                created_at=conv.created_at,
                updated_at=conv.updated_at
            )
            for conv in conversations
        ]

@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: str,
    current_user: str = Depends(get_current_user)
):
    with engine.connect() as conn:
        conversation = conn.execute(
            text("""
                SELECT c.id FROM conversations c
                JOIN workspaces w ON c.workspace_id = w.id
                WHERE c.id = :conversation_id AND w.user_id = :user_id
            """),
            {"conversation_id": conversation_id, "user_id": current_user}
        ).fetchone()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        result = conn.execute(
            text("""
                SELECT id, conversation_id, role, content, created_at
                FROM messages
                WHERE conversation_id = :conversation_id
                ORDER BY created_at ASC
            """),
            {"conversation_id": conversation_id}
        )
        messages = result.fetchall()

        return [
            MessageResponse(
                id=str(msg.id),
                conversation_id=str(msg.conversation_id),
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at
            )
            for msg in messages
        ]

@router.post("", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    current_user: str = Depends(get_current_user)
):
    with engine.connect() as conn:
        conversation = conn.execute(
            text("""
                SELECT c.id, c.workspace_id FROM conversations c
                JOIN workspaces w ON c.workspace_id = w.id
                WHERE c.id = :conversation_id AND w.user_id = :user_id
            """),
            {"conversation_id": chat_request.conversation_id, "user_id": current_user}
        ).fetchone()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        papers_result = conn.execute(
            text("""
                SELECT p.id, p.title, p.authors, p.abstract, p.pdf_text
                FROM papers p
                JOIN workspace_papers wp ON p.id = wp.paper_id
                WHERE wp.workspace_id = :workspace_id
            """),
            {"workspace_id": chat_request.workspace_id}
        )
        papers = papers_result.fetchall()

        papers_list = [
            {
                "id": str(paper.id),
                "title": paper.title,
                "authors": paper.authors,
                "abstract": paper.abstract,
                "pdf_text": paper.pdf_text
            }
            for paper in papers
        ]

        context = build_context_from_papers(papers_list)

        messages_result = conn.execute(
            text("""
                SELECT role, content FROM messages
                WHERE conversation_id = :conversation_id
                ORDER BY created_at ASC
                LIMIT 10
            """),
            {"conversation_id": chat_request.conversation_id}
        )
        history = messages_result.fetchall()

        conversation_messages = create_research_assistant_prompt(context, chat_request.message)

        for msg in history:
            conversation_messages.append({"role": msg.role, "content": msg.content})

        conversation_messages.append({"role": "user", "content": chat_request.message})

        try:
            ai_response = generate_chat_response(conversation_messages)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating AI response: {str(e)}"
            )

        user_message_result = conn.execute(
            text("""
                INSERT INTO messages (conversation_id, role, content, created_at)
                VALUES (:conversation_id, :role, :content, :created_at)
                RETURNING id, conversation_id, role, content, created_at
            """),
            {
                "conversation_id": chat_request.conversation_id,
                "role": "user",
                "content": chat_request.message,
                "created_at": datetime.utcnow()
            }
        )
        user_message = user_message_result.fetchone()

        assistant_message_result = conn.execute(
            text("""
                INSERT INTO messages (conversation_id, role, content, created_at)
                VALUES (:conversation_id, :role, :content, :created_at)
                RETURNING id, conversation_id, role, content, created_at
            """),
            {
                "conversation_id": chat_request.conversation_id,
                "role": "assistant",
                "content": ai_response,
                "created_at": datetime.utcnow()
            }
        )
        assistant_message = assistant_message_result.fetchone()

        conn.execute(
            text("""
                UPDATE conversations
                SET updated_at = :updated_at
                WHERE id = :conversation_id
            """),
            {"conversation_id": chat_request.conversation_id, "updated_at": datetime.utcnow()}
        )
        conn.commit()

        return ChatResponse(
            message=MessageResponse(
                id=str(user_message.id),
                conversation_id=str(user_message.conversation_id),
                role=user_message.role,
                content=user_message.content,
                created_at=user_message.created_at
            ),
            response=MessageResponse(
                id=str(assistant_message.id),
                conversation_id=str(assistant_message.conversation_id),
                role=assistant_message.role,
                content=assistant_message.content,
                created_at=assistant_message.created_at
            )
        )

@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    current_user: str = Depends(get_current_user)
):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                DELETE FROM conversations
                WHERE id = :conversation_id
                AND workspace_id IN (
                    SELECT id FROM workspaces WHERE user_id = :user_id
                )
            """),
            {"conversation_id": conversation_id, "user_id": current_user}
        )
        conn.commit()

        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        return None
