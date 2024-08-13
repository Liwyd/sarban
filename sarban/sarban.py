from sarban.methods import Methods

class SARBAN(Methods):
    def __init__(
        self,
        full_address: str,
        https: bool = True,
    ) -> None:
        super().__init__()

        self.full_address = full_address
        self.https = https
        self.session_string = None
        self.token = None
