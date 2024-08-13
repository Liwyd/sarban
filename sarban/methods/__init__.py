from sarban.methods.base import Base
from sarban.methods.login import Login
from sarban.methods.inbounds import Inbounds
from sarban.methods.clients import Clients

class Methods(
    Base,
    Login,
    Inbounds,
    Clients
):
    pass
