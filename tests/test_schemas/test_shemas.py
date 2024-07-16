import pytest
from contextlib import nullcontext as does_not_raise

from app.shemas.score import MethodRequest
from pydantic import ValidationError


@pytest.mark.parametrize("data,error", [
    ({"account": "horns&hoofs", "login": "admin", "method": "clients_interests",
      "token": "d3573aff1555cd67dccf21b95fe8c4dc8732f33fd4e32461b7fe6a71d83c947688515e36774c00fb630b039fe2223c991f045f13f24091386050205c324687a0",
      "arguments": {"client_ids": [1, 2, 3, 4], "date": "20.07.2017"}}, does_not_raise()),
    ({"account": "horns&hoofs", "login": "h&f", "method": "online_score",
      "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95",
      "arguments": {"phone": "79175002040", "email": "stupnikov@otus.ru", "first_name": "Стансилав",
                    "last_name": "Ступников", "birthday": "01.01.1990", "gender": 1}}, does_not_raise()),
    ({"account": "horns&hoofs", "login": "h&f", "method": "online_score",
      "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95",
      "arguments": {}}, pytest.raises(ValidationError)),
    ({"account": "horns&hoofs", "login": "h&f", "method": "online_score",
      "token": "55cc9ce545bcd144300fe9efc28e65d415b923ebb6be1e19d2750a2c03e80dd209a27954dca045e5bb12418e7d89b6d718a9e35af34e14e1d5bcd5a08f21fc95",
      "arguments": {"phone": "79175002040", "last_name": "Ступников", "gender": 1}}, pytest.raises(ValidationError))
])
def test_schema_score(data, error):
    with error as e:
        request = MethodRequest(**data)