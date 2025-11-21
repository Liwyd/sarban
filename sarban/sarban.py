from sarban.methods import Methods


class SARBAN(Methods):
    """Main SARBAN client class for interacting with Marzban API.
    
    This class provides all methods for managing Marzban panel including
    admin management, user management, node management, and more.
    
    Example:
        ```python
        from sarban import SARBAN
        
        sb = SARBAN(
            full_address="https://panel.example.com:2087",
            https=True
        )
        sb.login("admin", "password")
        ```
    """
    
    def __init__(
        self,
        full_address: str,
        https: bool = True,
    ) -> None:
        """Initialize SARBAN client.
        
        Parameters:
            full_address (``str``):
                Full address of Marzban panel (e.g., "panel.example.com:2087")
                
            https (``bool``, optional):
                Whether to use HTTPS. Defaults to True.
        """
        super().__init__()

        self.full_address = full_address.rstrip('/')
        if not self.full_address.startswith(('http://', 'https://')):
            self.full_address = f"{'https' if https else 'http'}://{self.full_address}"
        
        self.https = https
        self.token = None
