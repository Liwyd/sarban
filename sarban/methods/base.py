import requests
import json
from typing import Any, Optional, Dict, Union

import sarban
from sarban import errors


class Base:
    def request(
        self: "sarban.SARBAN",
        path: str,
        method: str,
        headers: dict,
        data: Optional[Union[dict, str]] = None,
        params: Optional[dict] = None
    ) -> requests.Response:
        """Request to the Marzban API.

        Parameters:
            path (``str``):
                The request path relative to /api/
                
            method (``str``):
                The HTTP method (GET, POST, PUT, DELETE)
                
            data (``dict | str``, optional):
                The request body data
                
            headers (``dict``):
                The request headers
            
            params (``dict``, optional):
                Query parameters for GET requests

        Returns:
            `~requests.Response`: The HTTP response object.
        """
        url = f"{self.full_address}/api/{path}"

        try:
            if method == "GET":
                response = requests.get(
                    url, 
                    headers=headers, 
                    params=params,
                    verify=self.https,
                    timeout=30
                )
            elif method == "POST":
                if isinstance(data, str) or (isinstance(data, dict) and "admin/token" in path):
                    response = requests.post(
                        url, 
                        headers=headers, 
                        data=data, 
                        verify=self.https,
                        timeout=30
                    )
                else:
                    response = requests.post(
                        url, 
                        headers=headers, 
                        json=data, 
                        verify=self.https,
                        timeout=30
                    )
            elif method == "PUT":
                response = requests.put(
                    url, 
                    headers=headers, 
                    json=data, 
                    verify=self.https,
                    timeout=30
                )
            elif method == "DELETE":
                response = requests.delete(
                    url, 
                    headers=headers, 
                    verify=self.https,
                    timeout=30
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            return response
        except requests.exceptions.RequestException as e:
            raise errors.HTTPException(0, f"Request failed: {str(e)}")

    def verify_response(
        self: "sarban.SARBAN",
        response: requests.Response
    ) -> Any:
        """Verify and parse API response.

        Parameters:
            response (``requests.Response``):
                The HTTP response object

        Returns:
            `~Any`: Parsed JSON response on success.

        Raises:
            `~errors.Unauthorized`: If status code is 401
            `~errors.Forbidden`: If status code is 403
            `~errors.NotFound`: If status code is 404
            `~errors.Conflict`: If status code is 409
            `~errors.BadRequest`: If status code is 400
            `~errors.ValidationError`: If status code is 422
            `~errors.HTTPException`: For other HTTP errors
        """
        content_type = response.headers.get('Content-Type', '')
        
        if response.status_code == 200:
            if 'application/json' in content_type:
                try:
                    return response.json()
                except json.JSONDecodeError:
                    return {}
            return {}
        
        if response.status_code == 401:
            error_detail = "Not authenticated"
            if 'application/json' in content_type:
                try:
                    error_data = response.json()
                    error_detail = error_data.get('detail', error_detail)
                except json.JSONDecodeError:
                    pass
            raise errors.Unauthorized(error_detail)
        
        if response.status_code == 403:
            error_detail = "You are not allowed to perform this action"
            if 'application/json' in content_type:
                try:
                    error_data = response.json()
                    error_detail = error_data.get('detail', error_detail)
                except json.JSONDecodeError:
                    pass
            raise errors.Forbidden(error_detail)
        
        if response.status_code == 404:
            error_detail = "Entity not found"
            if 'application/json' in content_type:
                try:
                    error_data = response.json()
                    error_detail = error_data.get('detail', error_detail)
                except json.JSONDecodeError:
                    pass
            raise errors.NotFound(error_detail)
        
        if response.status_code == 409:
            error_detail = "Entity already exists"
            if 'application/json' in content_type:
                try:
                    error_data = response.json()
                    error_detail = error_data.get('detail', error_detail)
                except json.JSONDecodeError:
                    pass
            raise errors.Conflict(error_detail)
        
        if response.status_code == 400:
            error_detail = "Bad request"
            if 'application/json' in content_type:
                try:
                    error_data = response.json()
                    error_detail = error_data.get('detail', error_detail)
                except json.JSONDecodeError:
                    pass
            raise errors.BadRequest(error_detail)
        
        if response.status_code == 422:
            error_detail = "Validation error"
            if 'application/json' in content_type:
                try:
                    error_data = response.json()
                    if 'detail' in error_data:
                        detail = error_data['detail']
                        if isinstance(detail, list) and len(detail) > 0:
                            error_detail = detail[0].get('msg', error_detail)
                        else:
                            error_detail = str(detail)
                except (json.JSONDecodeError, (KeyError, IndexError)):
                    pass
            raise errors.ValidationError(error_detail)
        
        raise errors.HTTPException(
            response.status_code,
            f"HTTP {response.status_code} error occurred"
        )