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
        user_donations = user_donations.scalars().all()
        return user_donations


donation_crud = CRUDDonation(Donation)
