from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas
from .models import Profile


async def get_all_profiles(db: AsyncSession, skip: int, limit: int) -> List[Profile]:
    result = await db.execute(
        select(Profile).order_by(Profile.id).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_profile(db: AsyncSession, profile_id: int) -> Optional[Profile]:
    return await db.get(Profile, profile_id)


async def create_profile(db: AsyncSession, profile: schemas.ProfileCreate) -> Profile:
    db_profile = Profile(**profile.dict())
    db.add(db_profile)
    await db.commit()
    return db_profile


async def update_profile(
    db: AsyncSession, profile_id: int, profile: schemas.ProfileUpdate
) -> Optional[Profile]:
    db_profile = await db.get(Profile, profile_id)
    if db_profile is None:
        return None

    for key, value in profile.dict(exclude={"id"}, exclude_unset=True).items():
        if hasattr(db_profile, key):
            setattr(db_profile, key, value)

    await db.commit()
    return db_profile


async def delete_profile(db: AsyncSession, profile_id: int) -> Optional[Profile]:
    db_profile = await db.get(Profile, profile_id)
    if db_profile is None:
        return None

    await db.delete(db_profile)
    await db.commit()
    return db_profile
