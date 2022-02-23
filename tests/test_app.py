# pylint: disable=unused-argument,redefined-outer-name
import pytest
from app import schemas
from app.init_db import alembic_create_tables, alembic_drop_tables
from app.main import app
from httpx import AsyncClient, Response

profile_sample_request_body = """{
  "name": "John",
  "sex": 1,
  "device_list": [
    "Mobile"
  ]
}"""

profile_sample_response_body = """{
  "name": "John",
  "sex": 1,
  "number_of_purchases": 0,
  "avg_price_of_cart": null,
  "days_since_last_purchase": null,
  "last_purchase_date": null,
  "average_days_beetween_purchases": null,
  "average_number_of_purchases": null,
  "device_list": [
    "Mobile"
  ],
  "locations_list": null,
  "last_seen_location": null,
  "id": 1
}"""

updated_profile_sample_request_body = """{
  "number_of_purchases": 3,
  "avg_price_of_cart": 1000,
  "days_since_last_purchase": 2,
  "last_purchase_date": "2022-02-21T17:59:44.807Z",
  "average_days_beetween_purchases": 2,
  "average_number_of_purchases": 1,
  "device_list": [
    "Mobile", "Web"
  ],
  "locations_list": [
    "russia"
  ],
  "last_seen_location": {
    "latitude": 55.753797,
    "longitude": 37.6212683
  }
}"""

updated_profile_sample_response_body = """{
  "name": "John",
  "sex": 1,
  "number_of_purchases": 3,
  "avg_price_of_cart": 1000,
  "days_since_last_purchase": 2,
  "last_purchase_date": "2022-02-21T17:59:44.807000+00:00",
  "average_days_beetween_purchases": 2,
  "average_number_of_purchases": 1,
  "device_list": [
    "Mobile",
    "Web"
  ],
  "locations_list": [
    "russia"
  ],
  "last_seen_location": {
    "latitude": 55.753797,
    "longitude": 37.6212683
  },
  "id": 1
}"""

profile_sample = schemas.Profile.parse_raw(profile_sample_response_body)
updated_profile_sample = schemas.Profile.parse_raw(updated_profile_sample_response_body)


@pytest.fixture
async def init_db():
    await alembic_drop_tables()
    await alembic_create_tables()


@pytest.fixture
async def aclient():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


async def create_profile(async_client: AsyncClient):
    response: Response = await async_client.post(
        "/profiles/", content=profile_sample_request_body
    )
    assert response.status_code == 201
    new_profile = schemas.Profile.parse_raw(response.text)
    return new_profile


async def test_create_profile(init_db, aclient: AsyncClient):
    new_profile = await create_profile(aclient)
    assert new_profile == profile_sample


async def test_read_profile(init_db, aclient: AsyncClient):
    response: Response = await aclient.get("/profiles/")
    assert response.status_code == 200
    profile_list = schemas.ProfileList.parse_raw(response.text)
    assert profile_list.profiles == []

    new_profile = await create_profile(aclient)
    assert new_profile == profile_sample

    response: Response = await aclient.get("/profiles/1")
    assert response.status_code == 200
    profile = schemas.Profile.parse_raw(response.text)
    assert profile == profile_sample

    response: Response = await aclient.get("/profiles/")
    assert response.status_code == 200
    profile_list = schemas.ProfileList.parse_raw(response.text)
    profile = profile_list.profiles[0]
    assert profile == profile_sample


async def test_update_profile(init_db, aclient: AsyncClient):
    new_profile = await create_profile(aclient)
    assert new_profile == profile_sample

    response: Response = await aclient.put(
        "/profiles/1", content=updated_profile_sample_request_body
    )
    assert response.status_code == 200
    updated_profile = schemas.Profile.parse_raw(response.text)
    assert updated_profile == updated_profile_sample

    response: Response = await aclient.get("/profiles/1")
    assert response.status_code == 200
    profile = schemas.Profile.parse_raw(response.text)
    assert profile == updated_profile_sample


async def test_delete_profile_and_404_error(init_db, aclient: AsyncClient):
    new_profile = await create_profile(aclient)
    assert new_profile == profile_sample

    response: Response = await aclient.delete("/profiles/1")
    assert response.status_code == 204

    response: Response = await aclient.get("/profiles/")
    assert response.status_code == 200
    profile_list = schemas.ProfileList.parse_raw(response.text)
    assert profile_list.profiles == []

    response: Response = await aclient.get("/profiles/1")
    assert response.status_code == 404

    response: Response = await aclient.put(
        "/profiles/1", content=updated_profile_sample_request_body
    )
    assert response.status_code == 404

    response: Response = await aclient.delete("/profiles/1")
    assert response.status_code == 404
