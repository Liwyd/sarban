from typing import Any, Dict, List, Optional
import sarban


class System:
    def get_system_stats(
        self: "sarban.SARBAN"
    ) -> Dict[str, Any]:
        """Fetch system stats including memory, CPU, and user metrics.

        Returns:
            `~Dict`: System statistics including version, memory, CPU, users, and bandwidth.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path="system",
            method="GET",
            headers=headers
        )

        return self.verify_response(response)

    def get_inbounds(
        self: "sarban.SARBAN"
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Retrieve inbound configurations grouped by protocol.

        Returns:
            `~Dict`: Inbound configurations grouped by protocol type.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path="inbounds",
            method="GET",
            headers=headers
        )

        return self.verify_response(response)

    def get_hosts(
        self: "sarban.SARBAN"
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Get a list of proxy hosts grouped by inbound tag.

        Returns:
            `~Dict`: Proxy hosts grouped by inbound tag.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path="hosts",
            method="GET",
            headers=headers
        )

        return self.verify_response(response)

    def modify_hosts(
        self: "sarban.SARBAN",
        hosts: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Modify proxy hosts and update the configuration.

        Parameters:
            hosts (``Dict``):
                Dictionary of hosts grouped by inbound tag

        Returns:
            `~Dict`: Updated proxy hosts.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        response = self.request(
            path="hosts",
            method="PUT",
            headers=headers,
            data=hosts
        )

        return self.verify_response(response)

