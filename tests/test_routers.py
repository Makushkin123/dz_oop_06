import pytest
from httpx import AsyncClient, ASGITransport
from main import app as fast_app


@pytest.fixture(scope="function", autouse=True)
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=fast_app), base_url="http://test") as ac:
        yield ac


@pytest.mark.parametrize("json_data,code", [
    (
            {"account": "horns&hoofs", "login": "admin", "method": "clients_interests",
             "token": "d3573aff1555cd67dccf21b95fe8c4dc8732f33fd4e32461b7fe6a71d83c947688515e36774c00fb630b039fe2223c991f045f13f24091386050205c324687a0",
             "arguments": {"client_ids": [1, 2, 3, 4], "date": "20.07.2017"}}, 200
    ),
    (
            {"account": "horns&hoofs", "login": "admin", "method": "clients_interests",
             "token": "d3573aff1555cd67dccf21b95fe8c4dc8732f33fd4e32461b7fe6a71d83c947688515e36774c00fb630b039fe2223c991f045f13f24091386050205c324687a0",
             "arguments": {"date": "20.07.2017"}}, 422
    ),
    (
            {"account": "horns&hoofs", "login": "admin", "method": "clients_interests",
             "token": "d3573aff1555cd67dccf21b95fe8c4dc8732f33fd4e32461b7fe6a71d83c947688515e36774c00fb630b039fe2223c991f045f13f24091386050205c324687a0",
             "arguments": {"client_ids": [1, 2, 3, 4]}}, 200
    ),
]
)
@pytest.mark.asyncio
async def test_get_score_api_(json_data, code, ac):
    responce = await ac.post("/method", json=json_data)
    assert responce.status_code == code
