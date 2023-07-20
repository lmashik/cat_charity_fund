from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBaseAdvanced
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBaseAdvanced):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Поиск id проекта по имени."""
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_opened_projects(
            self, session: AsyncSession
    ) -> Optional[List[CharityProject]]:
        db_opened_projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested is False
            )
        )
        return db_opened_projects.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)


# async def create_charity_project(
#         new_project: CharityProjectCreate,
#         session: AsyncSession,
# ) -> CharityProject:
#     """Создание проекта в базе."""
#     new_project_data = new_project.dict()
#     db_project = CharityProject(**new_project_data)
#
#     session.add(db_project)
#     await session.commit()
#     await session.refresh(db_project)
#
#     return db_project


# async def read_all_projects_from_db(
#         session: AsyncSession,
# ) -> Optional[List[CharityProject]]:
#     db_projects = await session.execute(select(CharityProject))
#     return db_projects.scalars().all()


# async def get_charity_project_by_id(
#         project_id: int,
#         session: AsyncSession,
# ) -> Optional[CharityProject]:
#     db_project = await session.get(CharityProject, project_id)
#     return db_project


# async def update_charity_project(
#         db_project: CharityProject,
#         project_in: CharityProjectUpdate,
#         session: AsyncSession,
# ) -> CharityProject:
#     obj_data = jsonable_encoder(db_project)
#     update_data = project_in.dict(exclude_unset=True)
#
#     for field in obj_data:
#         if field in update_data:
#             setattr(db_project, field, update_data[field])
#
#     session.add(db_project)
#     await session.commit()
#     await session.refresh(db_project)
#     return db_project


# async def delete_charity_project(
#         db_project: CharityProject,
#         session: AsyncSession,
# ) -> CharityProject:
#     await session.delete(db_project)
#     await session.commit()
#     return db_project
