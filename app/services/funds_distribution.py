from typing import List, Optional, Union

from app.models import CharityProject, Donation

MyComplexType = Union[Donation, CharityProject]


def funds_distribution(
        to_items: Optional[List[MyComplexType]], funds: MyComplexType
) -> MyComplexType:
    if to_items:
        first_item = to_items[0]
        if first_item.full_amount - first_item.invested_amount <= funds.full_amount:
            first_item.invested_amount = first_item.full_amount
            first_item.fully_invested = True
            to_items.pop(0)
            funds.invested_amount = first_item.full_amount - first_item.invested_amount
            funds_distribution(to_items, funds)
        else:
            funds.invested_amount = funds.full_amount
            funds.fully_invested = True
            first_item.invested_amount += funds.full_amount




#
#
# def new_donation_appear(donation: Donation, session: AsyncSession):
#     # open_project = CharityProject.query.filter_by(fully_invested=False).first()
#     open_projects = session.execute(
#         select(CharityProject).where(CharityProject.fully_invested is False)
#     )
#     open_project = open_projects.scalars().first()
#
#     if open_project:
#         if open_project.full_amount - open_project.invested_amount <= donation.full_amount:
#             open_project.invested_amount = open_project.full_amount
#             open_project.fully_invested = True
#             donation.invested_amount = open_project.full_amount - open_project.invested_amount
#             session.commit()
#             new_donation_appear(donation, session)
#         else:
#             donation.invested_amount = donation.full_amount
#             donation.fully_invested = True
#             open_project.invested_amount += donation.full_amount
#             session.commit()
#
#
# def new_project_appear(project: CharityProject):
#     open_donation = Donation.query.filter_by(fully_invested=False).first()
#
#     if open_donation:
#         if open_donation.full_amount - open_donation.invested_amount <= project.full_amount:
#             open_donation.invested_amount = open_donation.full_amount
#             open_donation.fully_invested = True
#             project.invested_amount = open_donation.full_amount - open_donation.invested_amount
#             new_project_appear(project)
#         else:
#             project.invested_amount = project.full_amount
#             project.fully_invested = True
#             open_donation.invested_amount += project.full_amount
