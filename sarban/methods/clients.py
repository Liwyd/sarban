import json
from typing import Union
import time, uuid


import sarban
from sarban import errors

class Clients:
    def __UUIDgen() -> str:
        timestamp = int(time.time() * 1000)
        generated_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(timestamp)))

        return generated_uuid

    def get_client(
        self: "sarban.SARBAN",
        username: str,
    ) -> Union[dict, errors.NotFound]:
        """Get client from the existing inbound.

        Parameters:
            username (``str``):
               username of the client

            
        Returns:
            `~Dict`: On success, a dict is returned or else 404 an error will be raised
        """
        
        # OLD WAY ==============================
        # all_users = self.get_users()

        # for user in range(all_users["total"]):
        #     if all_users["users"][user]["username"] == username:
        #         return all_users["users"][user]

        # raise errors.NotFound()
        #=======================================


        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path=f"user/{username}",
            method="GET",
            headers=headers
        )

        return self.verify_response(response)

    def get_client_by_subLink(
        self: "sarban.SARBAN",
        token: str,
    ) -> Union[dict, errors.NotFound]:
        """Get client from the existing inbound.

        Parameters:
            token (``str``):
               token of the client(sublinks token)

            
        Returns:
            `~Dict`: On success, a dict is returned or else 404 an error will be raised
        """
        import requests
        
        headers = {
            'accept': 'application/json',
        }

        url = f"{self.full_address}/sub/{token}/info"
        
        response = requests.get(
            url,
            headers=headers,
            verify=self.https,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise errors.NotFound()

    def add_client(
        self: "sarban.SARBAN",
        username: str,
        inboundTag: list,
        note:str = "",
        enable: str = "active",
        flow: str = "xtls-rprx-vision",
        total_gb: int = 0,
        expire_time: int = 0,
    ) -> Union[dict, errors.NotFound]:
        """Add client to the existing inbounds.

        Parameters:
            username (``str``):
                username of client
                
            inboundTag (``str(list)``):
               list of inbounds avaible for client
                
            note (``str``, optional):
               Note for client
                
            enable (``str``, optional):
               Status of the client
                
            flow (``str``, optional):
               Flow of the client
                
            total_gb (``int``, optional):
                Download and uploader limition of the client and it's in GB
                
            expire_time (``str``, optional):
                Client expiration date and it's in timestamp
                
        Returns:
            `~Dict`: On success, a dict is returned else 404 error will be raised
        """
        
        
        data = {
        "username": username,
        "proxies": {
            "vless": {
            "flow": flow
            }
        },
        "inbounds": {
            "vless": inboundTag
        },
        "expire": expire_time,
        "data_limit": total_gb*1024**3,
        "data_limit_reset_strategy": "no_reset",
        "status": enable,
        "note": note
        }

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }


        response = self.request(
            path="user",
            method="POST",
            data=data,
            headers= headers
        )

        return self.verify_response(response)

    def delete_client(
        self: "sarban.SARBAN",
        username: str,
    ) -> Union[dict, errors.NotFound]:
        """Delete client

        Parameters:
            username (``str``):
               username of the client
                
        Returns:
            `~Dict`: On success, a dict is returned else 404 error will be raised
        """

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        

        response = self.request(
            path=f"user/{username}",
            method="DELETE",
            headers=headers
        )

        return self.verify_response(response)

    def edit_client(
        self: "sarban.SARBAN",
        username: str,
        inboundTag: list,
        note:str = "",
        enable: str = "active",
        flow: str = "xtls-rprx-vision",
        total_gb: int = 0,
        expire_time: int = 0,
    ) -> Union[dict, errors.NotFound]:
        """edit client

        Parameters:
            username (``str``):
                username of client
                
            inboundTag (``str(list)``):
               list of inbounds avaible for client
                
            note (``str``, optional):
               Note for client
                
            enable (``str``, optional):
               Status of the client
                
            flow (``str``, optional):
               Flow of the client
                
            total_gb (``int``, optional):
                Download and uploader limition of the client and it's in GB
                
            expire_time (``str``, optional):
                Client expiration date and it's in timestamp
                
        Returns:
            `~Dict`: On success, a dict is returned else 404 error will be raised
        """


        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        data = {}


        # adding proxies
        new = {
            "proxies": {
                "vless": {
                    "flow": flow
                }
            }
        }
        data.update(new)
        
        # adding inbounds
        new = {
            "inbounds": {
                "vless": inboundTag
            }
        }
        data.update(new)

        # adding other deatails if needed
        if total_gb:
            new = {
                "data_limit": total_gb*(1024**3),
            }
            data.update(new)
        if enable != "active":
            new = {
                "status": enable
            }
            data.update(new)
        if expire_time:
            new = {
                "expire": expire_time
            }
            data.update(new)
        if note != "":
            new = {
                "note": note
            }
            data.update(new)


        response = self.request(
            path=f"user/{username}",
            method="PUT",
            headers=headers,
            data=data
        )

        return self.verify_response(response)

    def reset_user_data_usage(
        self: "sarban.SARBAN",
        username: str
    ) -> Union[dict, errors.NotFound]:
        """Reset user data usage.

        Parameters:
            username (``str``):
                Username of the client

        Returns:
            `~Dict`: Updated user information.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path=f"user/{username}/reset",
            method="POST",
            headers=headers
        )

        return self.verify_response(response)

    def revoke_user_subscription(
        self: "sarban.SARBAN",
        username: str
    ) -> Union[dict, errors.NotFound]:
        """Revoke user subscription (Subscription link and proxies).

        Parameters:
            username (``str``):
                Username of the client

        Returns:
            `~Dict`: Updated user information.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path=f"user/{username}/revoke_sub",
            method="POST",
            headers=headers
        )

        return self.verify_response(response)

    def get_user_usage(
        self: "sarban.SARBAN",
        username: str,
        start: str = "",
        end: str = ""
    ) -> Union[dict, errors.NotFound]:
        """Get user usage statistics.

        Parameters:
            username (``str``):
                Username of the client
                
            start (``str``, optional):
                Start date (ISO format)
                
            end (``str``, optional):
                End date (ISO format)

        Returns:
            `~Dict`: User usage statistics.
        """
        params = {}
        if start:
            params["start"] = start
        if end:
            params["end"] = end

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path=f"user/{username}/usage",
            method="GET",
            headers=headers,
            params=params if params else None
        )

        return self.verify_response(response)

    def active_next_plan(
        self: "sarban.SARBAN",
        username: str
    ) -> Union[dict, errors.NotFound]:
        """Reset user by next plan.

        Parameters:
            username (``str``):
                Username of the client

        Returns:
            `~Dict`: Updated user information.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path=f"user/{username}/active-next",
            method="POST",
            headers=headers
        )

        return self.verify_response(response)

    def set_owner(
        self: "sarban.SARBAN",
        username: str,
        admin_username: str
    ) -> Union[dict, errors.NotFound]:
        """Set a new owner (admin) for a user.

        Parameters:
            username (``str``):
                Username of the client
                
            admin_username (``str``):
                New admin username

        Returns:
            `~Dict`: Updated user information.
        """
        params = {"admin_username": admin_username}

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path=f"user/{username}/set-owner",
            method="PUT",
            headers=headers,
            params=params
        )

        return self.verify_response(response)

    def get_users(
        self: "sarban.SARBAN",
        offset: int = None,
        limit: int = None,
        username: list = None,
        search: str = None,
        admin: list = None,
        status: str = None,
        sort: str = None
    ) -> Union[dict, errors.NotFound]:
        """Get all users with optional filters.

        Parameters:
            offset (``int``, optional):
                Pagination offset
                
            limit (``int``, optional):
                Maximum number of results
                
            username (``list``, optional):
                Filter by usernames
                
            search (``str``, optional):
                Search query
                
            admin (``list``, optional):
                Filter by admin usernames
                
            status (``str``, optional):
                Filter by status (active, disabled, limited, expired, on_hold)
                
            sort (``str``, optional):
                Sort field

        Returns:
            `~Dict`: Users response with users list and total count.
        """
        params = {}
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        if username is not None:
            params["username"] = username
        if search is not None:
            params["search"] = search
        if admin is not None:
            params["admin"] = admin
        if status is not None:
            params["status"] = status
        if sort is not None:
            params["sort"] = sort

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path="users",
            method="GET",
            headers=headers,
            params=params if params else None
        )

        return self.verify_response(response)

    def reset_users_data_usage(
        self: "sarban.SARBAN"
    ) -> bool:
        """Reset all users data usage.

        Returns:
            `~bool`: True on success.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path="users/reset",
            method="POST",
            headers=headers
        )

        self.verify_response(response)
        return True

    def get_users_usage(
        self: "sarban.SARBAN",
        start: str = "",
        end: str = "",
        admin: list = None
    ) -> Union[dict, errors.NotFound]:
        """Get all users usage statistics.

        Parameters:
            start (``str``, optional):
                Start date (ISO format)
                
            end (``str``, optional):
                End date (ISO format)
                
            admin (``list``, optional):
                Filter by admin usernames

        Returns:
            `~Dict`: Users usage statistics.
        """
        params = {}
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        if admin is not None:
            params["admin"] = admin

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path="users/usage",
            method="GET",
            headers=headers,
            params=params if params else None
        )

        return self.verify_response(response)

    def get_expired_users(
        self: "sarban.SARBAN",
        expired_after: str = None,
        expired_before: str = None
    ) -> list:
        """Get users who have expired within the specified date range.

        Parameters:
            expired_after (``str``, optional):
                UTC datetime (ISO format)
                
            expired_before (``str``, optional):
                UTC datetime (ISO format)

        Returns:
            `~List[str]`: List of expired usernames.
        """
        params = {}
        if expired_after is not None:
            params["expired_after"] = expired_after
        if expired_before is not None:
            params["expired_before"] = expired_before

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path="users/expired",
            method="GET",
            headers=headers,
            params=params if params else None
        )

        return self.verify_response(response)

    def delete_expired_users(
        self: "sarban.SARBAN",
        expired_after: str = None,
        expired_before: str = None
    ) -> list:
        """Delete users who have expired within the specified date range.

        Parameters:
            expired_after (``str``, optional):
                UTC datetime (ISO format)
                
            expired_before (``str``, optional):
                UTC datetime (ISO format)

        Returns:
            `~List[str]`: List of deleted usernames.
        """
        params = {}
        if expired_after is not None:
            params["expired_after"] = expired_after
        if expired_before is not None:
            params["expired_before"] = expired_before

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path="users/expired",
            method="DELETE",
            headers=headers,
            params=params if params else None
        )

        return self.verify_response(response)