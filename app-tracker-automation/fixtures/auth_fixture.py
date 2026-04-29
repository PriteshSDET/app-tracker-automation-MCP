"""
Authentication fixture for user authentication management
"""

import pytest
from utils.config import Config
from utils.logger import Logger
from api.auth_api import AuthAPI


@pytest.fixture(scope="session")
def auth_token():
    """Fixture providing authentication token"""
    logger = Logger()
    auth_api = AuthAPI()
    
    try:
        # Get authentication token
        token = auth_api.get_auth_token(
            username=Config.TEST_USERNAME,
            password=Config.TEST_PASSWORD
        )
        logger.info("Authentication token obtained successfully")
        return token
    except Exception as e:
        logger.error(f"Failed to get authentication token: {str(e)}")
        pytest.fail(f"Authentication failed: {str(e)}")


@pytest.fixture(scope="function")
def user_data():
    """Fixture providing test user data"""
    return {
        "username": Config.TEST_USERNAME,
        "password": Config.TEST_PASSWORD,
        "email": Config.TEST_EMAIL,
        "full_name": Config.TEST_FULL_NAME,
        "role": Config.TEST_ROLE
    }


@pytest.fixture(scope="function")
def admin_user_data():
    """Fixture providing admin user data"""
    return {
        "username": Config.ADMIN_USERNAME,
        "password": Config.ADMIN_PASSWORD,
        "email": Config.ADMIN_EMAIL,
        "full_name": Config.ADMIN_FULL_NAME,
        "role": "admin"
    }


@pytest.fixture(scope="function")
def agent_user_data():
    """Fixture providing agent user data"""
    return {
        "username": Config.AGENT_USERNAME,
        "password": Config.AGENT_PASSWORD,
        "email": Config.AGENT_EMAIL,
        "full_name": Config.AGENT_FULL_NAME,
        "role": "agent"
    }


@pytest.fixture(scope="session")
def test_permissions():
    """Fixture providing test permissions"""
    return {
        "read": True,
        "write": True,
        "delete": False,
        "admin": False
    }
