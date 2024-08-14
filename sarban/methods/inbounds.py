from typing import Union

import sarban
from sarban import errors

class Inbounds:
    def get_users(
        self: "sarban.SARBAN"
    ) -> Union[dict, errors.NotFound]:
        """Get inbounds of the Marzban.
        
        Returns:
            `~Dict | errors.NotFound`: On success, a dict is returned else 404 error will be raised
        """
        

        params = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path="users",
            method="GET",
            headers=params
        )

        return self.verify_response(response)
