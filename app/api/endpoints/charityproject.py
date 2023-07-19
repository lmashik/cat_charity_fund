from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charityproject import (
    create_charity_project, delete_charity_project, get_charity_project_by_id,
    get_project_id_by_name, read_all_projects_from_db, update_charity_project
)
from app.models.charityproject import CharityProject
from app.schemas.charityproject import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создание проектов. Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    new_project = await create_charity_project(charity_project, session)
    return new_project


@router.get(
    '/',
    response_model=Optional[List[CharityProjectDB]],
    response_model_exclude_none=True,
)
async def get_all_projects(session: AsyncSession = Depends(get_async_session)):
    """Получение проектов."""
    projects = await read_all_projects_from_db(session)
    return projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Редактирование проектов. Только для суперюзеров."""
    charity_project = await check_project_exists(project_id, session)

    if charity_project.close_date:
        raise HTTPException(
            status_code=405,
            detail='Нельзя изменить закрытый проект!'
        )

    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)

    if obj_in.full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='Требуемая сумма проекта не может быть меньше вложенной!'
        )

    charity_project = await update_charity_project(
        charity_project, obj_in, session
    )

    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Удаление проектов. Только для суперюзеров."""
    charity_project = await check_project_exists(project_id, session)
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=405,
            detail='Нельзя удалить проект, в который были вложения!'
        )
    charity_project = await delete_charity_project(charity_project, session)
    return charity_project


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверка уникальности названия проекта."""
    project_id = await get_project_id_by_name(project_name, session)
    if project_id:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверка существования проекта."""
    charity_project = await get_charity_project_by_id(project_id, session)
    if not charity_project:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project
