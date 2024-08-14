import json
from typing import Any
import sarban
from sarban import errors

class Login:
    def login(
        self: "sarban.SARBAN",
        username: str,
        password: str
    ) -> Any:
        """Login into marzan panel.

        Parameters:
            username (``str``):
                Username of panel
                
            password (``str``):
                Password of panel

        Returns:
            `~Any`: On success, True is returned else an error will be raised
        """
        
        if self.session_string:
            raise errors.AlreadyLogin()
        


        headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'grant_type': '',
            'username': username,
            'password': password,
            'scope': '',
            'client_id': '',
            'client_secret': ''
        }


        send_request = self.request(
            path="admin/token",
            method="POST",
            data=data,
            headers=headers
        )
        if send_request.status_code == 200:
            self.token = json.loads(send_request.text)["access_token"]
            return True
            
        raise errors.BadLogin()
