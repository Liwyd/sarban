from typing import Any
import sarban
from sarban import errors


class Login:
    def login(
        self: "sarban.SARBAN",
        username: str,
        password: str
    ) -> bool:
        """Login into Marzban panel.

        Parameters:
            username (``str``):
                Username of panel
                
            password (``str``):
                Password of panel

        Returns:
            `~bool`: True on successful login.

        Raises:
            `~errors.AlreadyLogin`: If already logged in
            `~errors.BadLogin`: If credentials are invalid
        """
        if self.token:
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

        response = self.request(
            path="admin/token",
            method="POST",
            data=data,
            headers=headers
        )

        if response.status_code == 200:
            try:
                result = response.json()
                self.token = result.get("access_token")
                if not self.token:
                    raise errors.BadLogin()
                return True
            except (ValueError, KeyError):
                raise errors.BadLogin()
        elif response.status_code == 401:
            raise errors.BadLogin()
        else:
            raise errors.HTTPException(response.status_code, "Login failed")
