from fastapi import APIRouter, HTTPException, status, Depends
from models.schemas import WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse
from utils.auth import get_current_user
from database import engine
from sqlalchemy import text
from typing import List
from datetime import datetime

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])

@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    workspace_data: WorkspaceCreate,
    current_user: str = Depends(get_current_user)
):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                INSERT INTO workspaces (user_id, name, description, created_at, updated_at)
                VALUES (:user_id, :name, :description, :created_at, :updated_at)
                RETURNING id, user_id, name, description, created_at, updated_at
            """),
            {
                "user_id": current_user,
                "name": workspace_data.name,
                "description": workspace_data.description,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        )
        conn.commit()
        workspace = result.fetchone()

        return WorkspaceResponse(
            id=str(workspace.id),
            user_id=str(workspace.user_id),
            name=workspace.name,
            description=workspace.description,
            created_at=workspace.created_at,
            updated_at=workspace.updated_at
        )

@router.get("", response_model=List[WorkspaceResponse])
async def get_workspaces(current_user: str = Depends(get_current_user)):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT id, user_id, name, description, created_at, updated_at
                FROM workspaces
                WHERE user_id = :user_id
                ORDER BY created_at DESC
            """),
            {"user_id": current_user}
        )
        workspaces = result.fetchall()

        return [
            WorkspaceResponse(
                id=str(ws.id),
                user_id=str(ws.user_id),
                name=ws.name,
                description=ws.description,
                created_at=ws.created_at,
                updated_at=ws.updated_at
            )
            for ws in workspaces
        ]

@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(
    workspace_id: str,
    current_user: str = Depends(get_current_user)
):
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT id, user_id, name, description, created_at, updated_at
                FROM workspaces
                WHERE id = :workspace_id AND user_id = :user_id
            """),
            {"workspace_id": workspace_id, "user_id": current_user}
        )
        workspace = result.fetchone()

        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found"
            )

        return WorkspaceResponse(
            id=str(workspace.id),
            user_id=str(workspace.user_id),
            name=workspace.name,
            description=workspace.description,
            created_at=workspace.created_at,
            updated_at=workspace.updated_at
        )

@router.put("/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(
    workspace_id: str,
    workspace_data: WorkspaceUpdate,
    current_user: str = Depends(get_current_user)
):
    with engine.connect() as conn:
        existing = conn.execute(
            text("SELECT id FROM workspaces WHERE id = :workspace_id AND user_id = :user_id"),
            {"workspace_id": workspace_id, "user_id": current_user}
        ).fetchone()

        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found"
            )

        updates = {}
        if workspace_data.name is not None:
            updates["name"] = workspace_data.name
        if workspace_data.description is not None:
            updates["description"] = workspace_data.description

        if not updates:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )

        set_clause = ", ".join([f"{key} = :{key}" for key in updates.keys()])
        updates["workspace_id"] = workspace_id
        updates["user_id"] = current_user
        updates["updated_at"] = datetime.utcnow()

        result = conn.execute(
            text(f"""
                UPDATE workspaces
                SET {set_clause}, updated_at = :updated_at
                WHERE id = :workspace_id AND user_id = :user_id
                RETURNING id, user_id, name, description, created_at, updated_at
            """),
            updates
        )
        conn.commit()
        workspace = result.fetchone()

        return WorkspaceResponse(
            id=str(workspace.id),
            user_id=str(workspace.user_id),
            name=workspace.name,
            description=workspace.description,
            created_at=workspace.created_at,
            updated_at=workspace.updated_at
        )

@router.delete("/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workspace(
    workspace_id: str,
    current_user: str = Depends(get_current_user)
):
    with engine.connect() as conn:
        result = conn.execute(
            text("DELETE FROM workspaces WHERE id = :workspace_id AND user_id = :user_id"),
            {"workspace_id": workspace_id, "user_id": current_user}
        )
        conn.commit()

        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found"
            )

        return None
