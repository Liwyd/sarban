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

        headers = {
            'accept': 'application/json',
        }

        response = self.request(
            path=f"{self.full_address}/sus/{token}/info",
            method="GET",
            headers=headers
        )

        return self.verify_response(response)

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