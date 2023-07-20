from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_by_user(
            self,
            user: User,
            session: AsyncSession,
    ) -> Optional[List[Donation]]:
        user_donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return user_donations.scalars().all()

    async def get_unallocated_donations(
            self, session: AsyncSession
    ) -> Optional[List[Donation]]:
        db_unallocated_donations = await session.execute(
            select(Donation).where(Donation.fully_invested is False)
        )
        return db_unallocated_donations.scalars().all()


donation_crud = CRUDDonation(Donation)
