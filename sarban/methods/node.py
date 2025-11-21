from typing import Any, Dict, List, Optional
import sarban


class Node:
    def get_node_settings(
        self: "sarban.SARBAN"
    ) -> Dict[str, Any]:
        """Retrieve the current node settings, including TLS certificate.

        Returns:
            `~Dict`: Node settings including min_node_version and certificate.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path="node/settings",
            method="GET",
            headers=headers
        )

        return self.verify_response(response)

    def add_node(
        self: "sarban.SARBAN",
        name: str,
        address: str,
        port: int = 62050,
        api_port: int = 62051,
        usage_coefficient: float = 1.0,
        add_as_new_host: bool = True
    ) -> Dict[str, Any]:
        """Add a new node to the database and optionally add it as a host.

        Parameters:
            name (``str``):
                Node name
                
            address (``str``):
                Node IP address or hostname
                
            port (``int``, optional):
                Node port. Defaults to 62050.
                
            api_port (``int``, optional):
                Node API port. Defaults to 62051.
                
            usage_coefficient (``float``, optional):
                Usage coefficient. Defaults to 1.0.
                
            add_as_new_host (``bool``, optional):
                Whether to add as new host. Defaults to True.

        Returns:
            `~Dict`: Created node information.
        """
        data = {
            "name": name,
            "address": address,
            "port": port,
            "api_port": api_port,
            "usage_coefficient": usage_coefficient,
            "add_as_new_host": add_as_new_host
        }

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        response = self.request(
            path="node",
            method="POST",
            headers=headers,
            data=data
        )

        return self.verify_response(response)

    def get_node(
        self: "sarban.SARBAN",
        node_id: int
    ) -> Dict[str, Any]:
        """Retrieve details of a specific node by its ID.

        Parameters:
            node_id (``int``):
                Node ID

        Returns:
            `~Dict`: Node information.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path=f"node/{node_id}",
            method="GET",
            headers=headers
        )

        return self.verify_response(response)

    def modify_node(
        self: "sarban.SARBAN",
        node_id: int,
        name: Optional[str] = None,
        address: Optional[str] = None,
        port: Optional[int] = None,
        api_port: Optional[int] = None,
        usage_coefficient: Optional[float] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update a node's details. Only accessible to sudo admins.

        Parameters:
            node_id (``int``):
                Node ID
                
            name (``str``, optional):
                New node name
                
            address (``str``, optional):
                New node address
                
            port (``int``, optional):
                New node port
                
            api_port (``int``, optional):
                New API port
                
            usage_coefficient (``float``, optional):
                New usage coefficient
                
            status (``str``, optional):
                New node status (connected, connecting, error, disabled)

        Returns:
            `~Dict`: Updated node information.
        """
        data = {}
        
        if name is not None:
            data["name"] = name
        if address is not None:
            data["address"] = address
        if port is not None:
            data["port"] = port
        if api_port is not None:
            data["api_port"] = api_port
        if usage_coefficient is not None:
            data["usage_coefficient"] = usage_coefficient
        if status is not None:
            data["status"] = status

        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        response = self.request(
            path=f"node/{node_id}",
            method="PUT",
            headers=headers,
            data=data
        )

        return self.verify_response(response)

    def remove_node(
        self: "sarban.SARBAN",
        node_id: int
    ) -> bool:
        """Delete a node and remove it from xray in the background.

        Parameters:
            node_id (``int``):
                Node ID to remove

        Returns:
            `~bool`: True on success.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path=f"node/{node_id}",
            method="DELETE",
            headers=headers
        )

        self.verify_response(response)
        return True

    def get_nodes(
        self: "sarban.SARBAN"
    ) -> List[Dict[str, Any]]:
        """Retrieve a list of all nodes. Accessible only to sudo admins.

        Returns:
            `~List[Dict]`: List of all nodes.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path="nodes",
            method="GET",
            headers=headers
        )

        return self.verify_response(response)

    def reconnect_node(
        self: "sarban.SARBAN",
        node_id: int
    ) -> bool:
        """Trigger a reconnection for the specified node. Only accessible to sudo admins.

        Parameters:
            node_id (``int``):
                Node ID to reconnect

        Returns:
            `~bool`: True on success.
        """
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = self.request(
            path=f"node/{node_id}/reconnect",
            method="POST",
            headers=headers
        )

        self.verify_response(response)
        return True

    def get_usage(
        self: "sarban.SARBAN",
        start: Optional[str] = None,
        end: Optional[str] = None
    ) -> Dict[str, Any]:
        """Retrieve usage statistics for nodes within a specified date range.

        Parameters:
            start (``str``, optional):
                Start date (ISO format)
                
            end (``str``, optional):
                End date (ISO format)

        Returns:
            `~Dict`: Usage statistics for all nodes.
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
            path="nodes/usage",
            method="GET",
            headers=headers,
            params=params if params else None
        )

        return self.verify_response(response)

