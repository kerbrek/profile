from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from pydantic import NonNegativeInt, PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, schemas
from .database import async_session

app = FastAPI()


async def get_db():
    async with async_session() as db:
        yield db


@app.get("/", response_class=RedirectResponse)
async def redirect_to_docs():
    return "/docs"


@app.get(
    "/profiles/",
    response_model=schemas.ProfileList,
)
async def read_all_profiles(
    skip: NonNegativeInt = 0,
    limit: PositiveInt = 10,
    db: AsyncSession = Depends(get_db),
):
    db_profiles = await crud.get_all_profiles(db, skip=skip, limit=limit)
    return {"profiles": db_profiles}


@app.get(
    "/profiles/{profile_id}",
    response_model=schemas.Profile,
    responses={404: {"description": "Not Found"}},
)
async def read_profile(profile_id: PositiveInt, db: AsyncSession = Depends(get_db)):
    db_profile = await crud.get_profile(db, profile_id)
    if db_profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db_profile


@app.post(
    "/profiles/",
    response_model=schemas.Profile,
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(
    profile: schemas.ProfileCreate,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    db_profile = await crud.create_profile(db, profile)
    response.headers["Location"] = f"/profiles/{db_profile.id}"
    return db_profile


@app.put(
    "/profiles/{profile_id}",
    response_model=schemas.Profile,
    responses={404: {"description": "Not Found"}},
)
async def update_profile(
    profile_id: PositiveInt,
    profile: schemas.ProfileUpdate,
    db: AsyncSession = Depends(get_db),
):
    db_profile = await crud.update_profile(db, profile_id, profile)
    if db_profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return db_profile


@app.delete(
    "/profiles/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Not Found"}},
)
async def delete_profile(profile_id: PositiveInt, db: AsyncSession = Depends(get_db)):
    db_profile = await crud.delete_profile(db, profile_id)
    if db_profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
