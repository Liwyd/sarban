from typing import Any, Dict, Optional
import sarban


class Subscription:
    def user_subscription(
        self: "sarban.SARBAN",
        token: str,
        user_agent: Optional[str] = None
    ) -> Any:
        """Provides a subscription link based on the user agent (Clash, V2Ray, etc.).

        Parameters:
            token (``str``):
                User subscription token
                
            user_agent (``str``, optional):
                User agent header to determine client type

        Returns:
            `~Any`: Subscription content (format depends on user agent).
        """
        headers = {
            'accept': 'application/json',
        }
        
        if user_agent:
            headers['User-Agent'] = user_agent

        url = f"{self.full_address}/sub/{token}/"
        
        import requests
        response = requests.get(
            url,
            headers=headers,
            verify=self.https,
            timeout=30
        )
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                return response.json()
            return response.text
        else:
            from sarban import errors
            raise errors.HTTPException(response.status_code, "Failed to get subscription")

    def user_subscription_info(
        self: "sarban.SARBAN",
        token: str
    ) -> Dict[str, Any]:
        """Retrieves detailed information about the user's subscription.

        Parameters:
            token (``str``):
                User subscription token

        Returns:
            `~Dict`: Subscription user information.
        """
        headers = {
            'accept': 'application/json',
        }

        url = f"{self.full_address}/sub/{token}/info"
        
        import requests
        response = requests.get(
            url,
            headers=headers,
            verify=self.https,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            from sarban import errors
            raise errors.HTTPException(response.status_code, "Failed to get subscription info")

    def user_get_usage(
        self: "sarban.SARBAN",
        token: str,
        start: str = "",
        end: str = ""
    ) -> Any:
        """Fetches the usage statistics for the user within a specified date range.

        Parameters:
            token (``str``):
                User subscription token
                
            start (``str``, optional):
                Start date (ISO format)
                
            end (``str``, optional):
                End date (ISO format)

        Returns:
            `~Any`: User usage statistics.
        """
        params = {}
        if start:
            params["start"] = start
        if end:
            params["end"] = end

        headers = {
            'accept': 'application/json',
        }

        url = f"{self.full_address}/sub/{token}/usage"
        
        import requests
        response = requests.get(
            url,
            headers=headers,
            params=params if params else None,
            verify=self.https,
            timeout=30
        )
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                return response.json()
            return response.text
        else:
            from sarban import errors
            raise errors.HTTPException(response.status_code, "Failed to get usage")

    def user_subscription_with_client_type(
        self: "sarban.SARBAN",
        token: str,
        client_type: str,
        user_agent: Optional[str] = None
    ) -> Any:
        """Provides a subscription link based on the specified client type.

        Parameters:
            token (``str``):
                User subscription token
                
            client_type (``str``):
                Client type (sing-box, clash-meta, clash, outline, v2ray, v2ray-json)
                
            user_agent (``str``, optional):
                User agent header

        Returns:
            `~Any`: Subscription content (format depends on client type).
        """
        headers = {
            'accept': 'application/json',
        }
        
        if user_agent:
            headers['User-Agent'] = user_agent

        url = f"{self.full_address}/sub/{token}/{client_type}"
        
        import requests
        response = requests.get(
            url,
            headers=headers,
            verify=self.https,
            timeout=30
        )
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                return response.json()
            return response.text
        else:
            from sarban import errors
            raise errors.HTTPException(response.status_code, "Failed to get subscription")

