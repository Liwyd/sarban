def sub_generator(userToken: str, fullAddress: str, verify: bool = False) -> str:
    """Generate subscription link for user.
    
    Parameters:
        userToken (``str``):
            User subscription token
            
        fullAddress (``str``):
            Full address of subscription server (e.g., "sub.example.com:2096")
            
        verify (``bool``, optional):
            Whether to use HTTPS. Defaults to False.
    
    Returns:
        `~str`: Generated subscription URL.
    """
    protocol = 'https' if verify else "http"
    address = fullAddress.rstrip('/')
    if not address.startswith(('http://', 'https://')):
        address = f"{protocol}://{address}"
    else:
        address = address
    
    return f"{address}/sub/{userToken}/"
