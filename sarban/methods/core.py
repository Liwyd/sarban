from typing import Any, Dict
import sarban


class Core:
    def get_core_stats(
        self: "sarban.SARBAN"
    ) -> Dict[str, Any]:
        """Retrieve core statistics such as version and uptime.

        Returns:
            `~Dict`: Core statistics including version, started status, and logs_websocket.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path="core",
            method="GET",
            headers=headers
        )

        return self.verify_response(response)

    def restart_core(
        self: "sarban.SARBAN"
    ) -> bool:
        """Restart the core and all connected nodes.

        Returns:
            `~bool`: True on success.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path="core/restart",
            method="POST",
            headers=headers
        )

        self.verify_response(response)
        return True

    def get_core_config(
        self: "sarban.SARBAN"
    ) -> Dict[str, Any]:
        """Get the current core configuration.

        Returns:
            `~Dict`: Core configuration object.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path="core/config",
            method="GET",
            headers=headers
        )

        return self.verify_response(response)

    def modify_core_config(
        self: "sarban.SARBAN",
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Modify the core configuration and restart the core.

        Parameters:
            config (``Dict``):
                Core configuration object

        Returns:
            `~Dict`: Updated core configuration.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        response = self.request(
            path="core/config",
            method="PUT",
            headers=headers,
            data=config
        )

        return self.verify_response(response)

