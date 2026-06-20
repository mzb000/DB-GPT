import pytest
from app.services.auth_service import register_user, login_user
from app.core.exceptions import BadRequestError, CredentialsError


@pytest.mark.asyncio
async def test_register_user(db_session):
    result = await register_user(db_session, "new@test.com", "password123", "New User")
    assert "access_token" in result


@pytest.mark.asyncio
async def test_register_duplicate(db_session, test_user):
    with pytest.raises(BadRequestError):
        await register_user(db_session, "test@test.com", "pass", "Duplicate")


@pytest.mark.asyncio
async def test_login_success(db_session, test_user):
    result = await login_user(db_session, "test@test.com", "testpass")
    assert "access_token" in result


@pytest.mark.asyncio
async def test_login_failure(db_session, test_user):
    with pytest.raises(CredentialsError):
        await login_user(db_session, "test@test.com", "wrongpass")
