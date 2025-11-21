from typing import Any, Optional, List, Dict, Union
import sarban
from sarban import errors


class Admin:
    def get_current_admin(
        self: "sarban.SARBAN"
    ) -> Dict[str, Any]:
        """Get current authenticated admin information.

        Returns:
            `~Dict`: Admin information including username, is_sudo, telegram_id, etc.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path="admin",
            method="GET",
            headers=headers
        )

        return self.verify_response(response)

    def create_admin(
        self: "sarban.SARBAN",
        username: str,
        password: str,
        is_sudo: bool = False,
        telegram_id: Optional[int] = None,
        discord_webhook: Optional[str] = None,
        users_usage: Optional[int] = None
    ) -> Dict[str, Any]:
        """Create a new admin.

        Parameters:
            username (``str``):
                Admin username
                
            password (``str``):
                Admin password
                
            is_sudo (``bool``, optional):
                Whether the admin has sudo privileges. Defaults to False.
                
            telegram_id (``int``, optional):
                Telegram ID for notifications
                
            discord_webhook (``str``, optional):
                Discord webhook URL for notifications
                
            users_usage (``int``, optional):
                Usage limit for users under this admin

        Returns:
            `~Dict`: Created admin information.
        """
        data = {
            "username": username,
            "password": password,
            "is_sudo": is_sudo
        }

        if telegram_id is not None:
            data["telegram_id"] = telegram_id
        if discord_webhook is not None:
            data["discord_webhook"] = discord_webhook
        if users_usage is not None:
            data["users_usage"] = users_usage

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        response = self.request(
            path="admin",
            method="POST",
            headers=headers,
            data=data
        )

        return self.verify_response(response)

    def modify_admin(
        self: "sarban.SARBAN",
        username: str,
        password: Optional[str] = None,
        is_sudo: Optional[bool] = None,
        telegram_id: Optional[int] = None,
        discord_webhook: Optional[str] = None
    ) -> Dict[str, Any]:
        """Modify an existing admin's details.

        Parameters:
            username (``str``):
                Admin username to modify
                
            password (``str``, optional):
                New password
                
            is_sudo (``bool``, optional):
                New sudo status
                
            telegram_id (``int``, optional):
                New Telegram ID
                
            discord_webhook (``str``, optional):
                New Discord webhook URL

        Returns:
            `~Dict`: Updated admin information.
        """
        data = {}
        
        if password is not None:
            data["password"] = password
        if is_sudo is not None:
            data["is_sudo"] = is_sudo
        if telegram_id is not None:
            data["telegram_id"] = telegram_id
        if discord_webhook is not None:
            data["discord_webhook"] = discord_webhook

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        response = self.request(
            path=f"admin/{username}",
            method="PUT",
            headers=headers,
            data=data
        )

        return self.verify_response(response)

    def remove_admin(
        self: "sarban.SARBAN",
        username: str
    ) -> bool:
        """Remove an admin from the database.

        Parameters:
            username (``str``):
                Admin username to remove

        Returns:
            `~bool`: True on success.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path=f"admin/{username}",
            method="DELETE",
            headers=headers
        )

        self.verify_response(response)
        return True

    def get_admins(
        self: "sarban.SARBAN",
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        username: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Fetch a list of admins with optional filters.

        Parameters:
            offset (``int``, optional):
                Pagination offset
                
            limit (``int``, optional):
                Maximum number of results
                
            username (``str``, optional):
                Filter by username

        Returns:
            `~List[Dict]`: List of admin information.
        """
        params = {}
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        if username is not None:
            params["username"] = username

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path="admins",
            method="GET",
            headers=headers,
            params=params if params else None
        )

        return self.verify_response(response)

    def disable_all_active_users(
        self: "sarban.SARBAN",
        username: str
    ) -> bool:
        """Disable all active users under a specific admin.

        Parameters:
            username (``str``):
                Admin username

        Returns:
            `~bool`: True on success.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path=f"admin/{username}/users/disable",
            method="POST",
            headers=headers
        )

        self.verify_response(response)
        return True

    def activate_all_disabled_users(
        self: "sarban.SARBAN",
        username: str
    ) -> bool:
        """Activate all disabled users under a specific admin.

        Parameters:
            username (``str``):
                Admin username

        Returns:
            `~bool`: True on success.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path=f"admin/{username}/users/activate",
            method="POST",
            headers=headers
        )

        self.verify_response(response)
        return True

    def reset_admin_usage(
        self: "sarban.SARBAN",
        username: str
    ) -> Dict[str, Any]:
        """Reset usage of admin.

        Parameters:
            username (``str``):
                Admin username

        Returns:
            `~Dict`: Updated admin information.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path=f"admin/usage/reset/{username}",
            method="POST",
            headers=headers
        )

        return self.verify_response(response)

    def get_admin_usage(
        self: "sarban.SARBAN",
        username: str
    ) -> int:
        """Retrieve the usage of given admin.

        Parameters:
            username (``str``):
                Admin username

        Returns:
            `~int`: Admin usage in bytes.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path=f"admin/usage/{username}",
            method="GET",
            headers=headers
        )

        return self.verify_response(response)

