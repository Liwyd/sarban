from sarban.methods.base import Base
from sarban.methods.login import Login
from sarban.methods.inbounds import Inbounds
from sarban.methods.clients import Clients
from sarban.methods.admin import Admin
from sarban.methods.core import Core
from sarban.methods.node import Node
from sarban.methods.system import System
from sarban.methods.user_template import UserTemplate
from sarban.methods.subscription import Subscription


class Methods(
    Base,
    Login,
    Inbounds,
    Clients,
    Admin,
    Core,
    Node,
    System,
    UserTemplate,
    Subscription
):
    pass
