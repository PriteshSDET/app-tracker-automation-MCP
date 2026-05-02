"""
Authentication API client for handling user authentication
"""

from typing import Dict, Any, Optional
from api.client import APIClient
from utils.config import Config
from utils.logger import Logger


class AuthAPI(APIClient):
    """Authentication API client"""
    
    def __init__(self, base_url: str = None):
        super().__init__(base_url)
        self.logger = Logger()
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Perform user login
        
        Args:
            username: User username
            password: User password
            
        Returns:
            Dictionary containing login response
        """
        login_data = {
            "username": username,
            "password": password,
            "remember_me": False
        }
        
        response = self.post("/auth/login", json_data=login_data)
        
        if self.is_success(response):
            return self.handle_response(response)
        else:
            error_msg = f"Login failed with status {response.status_code}"
            self.logger.error(error_msg)
            raise requests.HTTPError(error_msg)
    
    def logout(self, token: str) -> Dict[str, Any]:
        """
        Perform user logout
        
        Args:
            token: Authentication token
            
        Returns:
            Dictionary containing logout response
        """
        self.set_auth_token(token)
        response = self.post("/auth/logout")
        
        if self.is_success(response):
            return self.handle_response(response)
        else:
            error_msg = f"Logout failed with status {response.status_code}"
            self.logger.error(error_msg)
            raise requests.HTTPError(error_msg)
    
    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """
        Refresh authentication token
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            Dictionary containing new token data
        """
        refresh_data = {
            "refresh_token": refresh_token
        }
        
        response = self.post("/auth/refresh", json_data=refresh_data)
        
        if self.is_success(response):
            return self.handle_response(response)
        else:
            error_msg = f"Token refresh failed with status {response.status_code}"
            self.logger.error(error_msg)
            raise requests.HTTPError(error_msg)
    
    def get_auth_token(self, username: str, password: str) -> str:
        """
        Get authentication token for user
        
        Args:
            username: User username
            password: User password
            
        Returns:
            Authentication token string
        """
        login_response = self.login(username, password)
        return login_response.get("access_token")
    
    def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register new user
        
        Args:
            user_data: User registration data
            
        Returns:
            Dictionary containing registration response
        """
        response = self.post("/auth/register", json_data=user_data)
        
        if self.is_success(response):
            return self.handle_response(response)
        else:
            error_msg = f"User registration failed with status {response.status_code}"
            self.logger.error(error_msg)
            raise requests.HTTPError(error_msg)
    
    def forgot_password(self, email: str) -> Dict[str, Any]:
        """
        Request password reset
        
        Args:
            email: User email address
            
        Returns:
            Dictionary containing password reset response
        """
        reset_data = {
            "email": email
        }
        
        response = self.post("/auth/forgot-password", json_data=reset_data)
        
        if self.is_success(response):
            return self.handle_response(response)
        else:
            error_msg = f"Password reset request failed with status {response.status_code}"
            self.logger.error(error_msg)
            raise requests.HTTPError(error_msg)
    
    def reset_password(self, token: str, new_password: str) -> Dict[str, Any]:
        """
        Reset password with token
        
        Args:
            token: Password reset token
            new_password: New password
            
        Returns:
            Dictionary containing password reset response
        """
        reset_data = {
            "token": token,
            "new_password": new_password
        }
        
        response = self.post("/auth/reset-password", json_data=reset_data)
        
        if self.is_success(response):
            return self.handle_response(response)
        else:
            error_msg = f"Password reset failed with status {response.status_code}"
            self.logger.error(error_msg)
            raise requests.HTTPError(error_msg)
    
    def change_password(self, token: str, current_password: str, new_password: str) -> Dict[str, Any]:
        """
        Change user password
        
        Args:
            token: Authentication token
            current_password: Current password
            new_password: New password
            
        Returns:
            Dictionary containing password change response
        """
        self.set_auth_token(token)
        
        password_data = {
            "current_password": current_password,
            "new_password": new_password
        }
        
        response = self.post("/auth/change-password", json_data=password_data)
        
        if self.is_success(response):
            return self.handle_response(response)
        else:
            error_msg = f"Password change failed with status {response.status_code}"
            self.logger.error(error_msg)
            raise requests.HTTPError(error_msg)
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify authentication token validity
        
        Args:
            token: Authentication token
            
        Returns:
            Dictionary containing token verification response
        """
        self.set_auth_token(token)
        response = self.get("/auth/verify")
        
        if self.is_success(response):
            return self.handle_response(response)
        else:
            error_msg = f"Token verification failed with status {response.status_code}"
            self.logger.error(error_msg)
            raise requests.HTTPError(error_msg)
    
    def get_user_profile(self, token: str) -> Dict[str, Any]:
        """
        Get user profile information
        
        Args:
            token: Authentication token
            
        Returns:
            Dictionary containing user profile data
        """
        self.set_auth_token(token)
        response = self.get("/auth/profile")
        
        if self.is_success(response):
            return self.handle_response(response)
        else:
            error_msg = f"Failed to get user profile with status {response.status_code}"
            self.logger.error(error_msg)
            raise requests.HTTPError(error_msg)
    
    def update_user_profile(self, token: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user profile information
        
        Args:
            token: Authentication token
            profile_data: Updated profile data
            
        Returns:
            Dictionary containing updated profile response
        """
        self.set_auth_token(token)
        response = self.put("/auth/profile", json_data=profile_data)
        
        if self.is_success(response):
            return self.handle_response(response)
        else:
            error_msg = f"Failed to update user profile with status {response.status_code}"
            self.logger.error(error_msg)
            raise requests.HTTPError(error_msg)

