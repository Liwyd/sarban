from typing import Union, Dict, Any

import sarban
from sarban import errors


class Inbounds:
    def get_users(
        self: "sarban.SARBAN"
    ) -> Union[Dict[str, Any], errors.NotFound]:
        """Get all users (legacy method for backward compatibility).
        
        Note: This method is kept for backward compatibility.
        Consider using get_users() from Clients class instead.
        
        Returns:
            `~Dict`: Users response with users list and total count.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path="users",
            method="GET",
            headers=headers
        )

        return self.verify_response(response)
