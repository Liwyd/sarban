from typing import Any, Dict, List, Optional
import sarban


class UserTemplate:
    def add_user_template(
        self: "sarban.SARBAN",
        name: Optional[str] = None,
        data_limit: Optional[int] = None,
        expire_duration: Optional[int] = None,
        username_prefix: Optional[str] = None,
        username_suffix: Optional[str] = None,
        inbounds: Optional[Dict[str, List[str]]] = None
    ) -> Dict[str, Any]:
        """Add a new user template.

        Parameters:
            name (``str``, optional):
                Template name (up to 64 characters)
                
            data_limit (``int``, optional):
                Data limit in bytes (>= 0)
                
            expire_duration (``int``, optional):
                Expire duration in seconds (>= 0)
                
            username_prefix (``str``, optional):
                Username prefix (1-20 characters)
                
            username_suffix (``str``, optional):
                Username suffix (1-20 characters)
                
            inbounds (``Dict[str, List[str]]``, optional):
                Dictionary of protocol:inbound_tags, empty means all inbounds

        Returns:
            `~Dict`: Created user template information.
        """
        data = {}
        
        if name is not None:
            data["name"] = name
        if data_limit is not None:
            data["data_limit"] = data_limit
        if expire_duration is not None:
            data["expire_duration"] = expire_duration
        if username_prefix is not None:
            data["username_prefix"] = username_prefix
        if username_suffix is not None:
            data["username_suffix"] = username_suffix
        if inbounds is not None:
            data["inbounds"] = inbounds

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        response = self.request(
            path="user_template",
            method="POST",
            headers=headers,
            data=data
        )

        return self.verify_response(response)

    def get_user_templates(
        self: "sarban.SARBAN",
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get a list of User Templates with optional pagination.

        Parameters:
            offset (``int``, optional):
                Pagination offset
                
            limit (``int``, optional):
                Maximum number of results

        Returns:
            `~List[Dict]`: List of user templates.
        """
        params = {}
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path="user_template",
            method="GET",
            headers=headers,
            params=params if params else None
        )

        return self.verify_response(response)

    def get_user_template(
        self: "sarban.SARBAN",
        template_id: int
    ) -> Dict[str, Any]:
        """Get User Template information with id.

        Parameters:
            template_id (``int``):
                Template ID

        Returns:
            `~Dict`: User template information.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path=f"user_template/{template_id}",
            method="GET",
            headers=headers
        )

        return self.verify_response(response)

    def modify_user_template(
        self: "sarban.SARBAN",
        template_id: int,
        name: Optional[str] = None,
        data_limit: Optional[int] = None,
        expire_duration: Optional[int] = None,
        username_prefix: Optional[str] = None,
        username_suffix: Optional[str] = None,
        inbounds: Optional[Dict[str, List[str]]] = None
    ) -> Dict[str, Any]:
        """Modify User Template.

        Parameters:
            template_id (``int``):
                Template ID
                
            name (``str``, optional):
                Template name (up to 64 characters)
                
            data_limit (``int``, optional):
                Data limit in bytes (>= 0)
                
            expire_duration (``int``, optional):
                Expire duration in seconds (>= 0)
                
            username_prefix (``str``, optional):
                Username prefix (1-20 characters)
                
            username_suffix (``str``, optional):
                Username suffix (1-20 characters)
                
            inbounds (``Dict[str, List[str]]``, optional):
                Dictionary of protocol:inbound_tags

        Returns:
            `~Dict`: Updated user template information.
        """
        data = {}
        
        if name is not None:
            data["name"] = name
        if data_limit is not None:
            data["data_limit"] = data_limit
        if expire_duration is not None:
            data["expire_duration"] = expire_duration
        if username_prefix is not None:
            data["username_prefix"] = username_prefix
        if username_suffix is not None:
            data["username_suffix"] = username_suffix
        if inbounds is not None:
            data["inbounds"] = inbounds

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        response = self.request(
            path=f"user_template/{template_id}",
            method="PUT",
            headers=headers,
            data=data
        )

        return self.verify_response(response)

    def remove_user_template(
        self: "sarban.SARBAN",
        template_id: int
    ) -> bool:
        """Remove a User Template by its ID.

        Parameters:
            template_id (``int``):
                Template ID to remove

        Returns:
            `~bool`: True on success.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path=f"user_template/{template_id}",
            method="DELETE",
            headers=headers
        )

        self.verify_response(response)
        return True

