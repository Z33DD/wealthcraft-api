from typing import Callable
from wealthcraft.dao import DAO

from wealthcraft.models import User
from wealthcraft.services import auth


def test_create_token_with_a_user(
    dao: DAO,
    user_factory: Callable[..., User],
):
    user = user_factory()
    assert user.id is not None

    token = auth.create_access_token(user)
    payload = auth.verify_token(token)
    del user

    assert payload.user is not None
    assert payload.user.id is not None

    user = dao.user.get(payload.user.id)

    assert user is not None
