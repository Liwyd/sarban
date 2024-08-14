def sub_generator(userToken: str, fullAddress:str, verify: bool = False) -> str:

    ssl = 'https' if verify else "http"
    string = f"{ssl}://{fullAddress}/sus/{userToken}"
    
    return string
