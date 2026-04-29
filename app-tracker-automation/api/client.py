"""
API client base class for HTTP requests
"""

import requests
import json
from typing import Dict, Any, Optional
from utils.config import Config
from utils.logger import Logger


class APIClient:
    """Base API client class"""
    
    def __init__(self, base_url: str = None):
        """Initialize API client with base URL"""
        self.base_url = base_url or Config.API_URL
        self.session = requests.Session()
        self.logger = Logger()
        
        # Set default headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "InsurancePortal-Automation/1.0"
        })
    
    def set_auth_token(self, token: str):
        """Set authentication token"""
        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })
    
    def clear_auth_token(self):
        """Clear authentication token"""
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
    
    def get(self, endpoint: str, params: Dict[str, Any] = None, **kwargs) -> requests.Response:
        """Perform GET request"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"GET request to: {url}")
        
        try:
            response = self.session.get(url, params=params, **kwargs)
            self._log_response(response)
            return response
        except Exception as e:
            self.logger.error(f"GET request failed: {str(e)}")
            raise
    
    def post(self, endpoint: str, data: Dict[str, Any] = None, json_data: Dict[str, Any] = None, **kwargs) -> requests.Response:
        """Perform POST request"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"POST request to: {url}")
        
        try:
            if json_data:
                response = self.session.post(url, json=json_data, **kwargs)
            else:
                response = self.session.post(url, data=data, **kwargs)
            
            self._log_response(response)
            return response
        except Exception as e:
            self.logger.error(f"POST request failed: {str(e)}")
            raise
    
    def put(self, endpoint: str, data: Dict[str, Any] = None, json_data: Dict[str, Any] = None, **kwargs) -> requests.Response:
        """Perform PUT request"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"PUT request to: {url}")
        
        try:
            if json_data:
                response = self.session.put(url, json=json_data, **kwargs)
            else:
                response = self.session.put(url, data=data, **kwargs)
            
            self._log_response(response)
            return response
        except Exception as e:
            self.logger.error(f"PUT request failed: {str(e)}")
            raise
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Perform DELETE request"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"DELETE request to: {url}")
        
        try:
            response = self.session.delete(url, **kwargs)
            self._log_response(response)
            return response
        except Exception as e:
            self.logger.error(f"DELETE request failed: {str(e)}")
            raise
    
    def patch(self, endpoint: str, data: Dict[str, Any] = None, json_data: Dict[str, Any] = None, **kwargs) -> requests.Response:
        """Perform PATCH request"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"PATCH request to: {url}")
        
        try:
            if json_data:
                response = self.session.patch(url, json=json_data, **kwargs)
            else:
                response = self.session.patch(url, data=data, **kwargs)
            
            self._log_response(response)
            return response
        except Exception as e:
            self.logger.error(f"PATCH request failed: {str(e)}")
            raise
    
    def _log_response(self, response: requests.Response):
        """Log response details"""
        self.logger.info(f"Response status: {response.status_code}")
        self.logger.debug(f"Response headers: {dict(response.headers)}")
        
        try:
            if response.content:
                self.logger.debug(f"Response body: {response.json()}")
        except:
            self.logger.debug(f"Response body: {response.text}")
    
    def handle_response(self, response: requests.Response, expected_status: int = 200) -> Dict[str, Any]:
        """Handle API response and return JSON data"""
        if response.status_code != expected_status:
            error_msg = f"Expected status {expected_status}, got {response.status_code}"
            self.logger.error(error_msg)
            raise requests.HTTPError(error_msg)
        
        try:
            return response.json()
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode JSON response: {str(e)}")
            raise
    
    def is_success(self, response: requests.Response) -> bool:
        """Check if response is successful"""
        return 200 <= response.status_code < 300
    
    def close(self):
        """Close the session"""
        self.session.close()
        self.logger.info("API client session closed")


class RESTClient(APIClient):
    """REST API client with additional convenience methods"""
    
    def __init__(self, base_url: str = None):
        super().__init__(base_url)
    
    def get_resource(self, resource_id: str, endpoint: str = "") -> requests.Response:
        """Get specific resource by ID"""
        return self.get(f"{endpoint}/{resource_id}")
    
    def create_resource(self, data: Dict[str, Any], endpoint: str = "") -> requests.Response:
        """Create new resource"""
        return self.post(endpoint, json_data=data)
    
    def update_resource(self, resource_id: str, data: Dict[str, Any], endpoint: str = "") -> requests.Response:
        """Update existing resource"""
        return self.put(f"{endpoint}/{resource_id}", json_data=data)
    
    def delete_resource(self, resource_id: str, endpoint: str = "") -> requests.Response:
        """Delete resource by ID"""
        return self.delete(f"{endpoint}/{resource_id}")
    
    def list_resources(self, params: Dict[str, Any] = None, endpoint: str = "") -> requests.Response:
        """List all resources with optional parameters"""
        return self.get(endpoint, params=params)
