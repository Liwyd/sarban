# SARBAN

A comprehensive Python SDK for managing Marzban panel ([Gozargah/Marzban](https://github.com/Gozargah/Marzban)) through its REST API.

## Features

- Complete API coverage for all Marzban endpoints
- Admin management (create, modify, remove admins)
- User management (CRUD operations, usage tracking)
- Node management (add, modify, remove, reconnect nodes)
- Core configuration and statistics
- System statistics and monitoring
- User template management
- Subscription management
- Comprehensive error handling
- Type hints for better IDE support

## Installation

```bash
pip install sarban
```

## Quick Start

```python
from sarban import SARBAN
from sarban.errors import BadLogin, Unauthorized

# Initialize the client
sb = SARBAN(
    full_address="https://your-marzban-panel.com:2087",
    https=True
)

# Login
try:
    sb.login("admin_username", "admin_password")
except BadLogin:
    print("Invalid credentials")
```

## API Reference

### Authentication

#### Login
```python
sb.login(username: str, password: str) -> bool
```

### Admin Management

#### Get Current Admin
```python
admin = sb.get_current_admin()
```

#### Create Admin
```python
admin = sb.create_admin(
    username="new_admin",
    password="secure_password",
    is_sudo=False,
    telegram_id=123456789,
    discord_webhook="https://discord.com/webhook/..."
)
```

#### Get Admins
```python
admins = sb.get_admins(offset=0, limit=10, username="admin")
```

#### Modify Admin
```python
admin = sb.modify_admin(
    username="admin",
    password="new_password",
    is_sudo=True
)
```

#### Remove Admin
```python
sb.remove_admin(username="admin")
```

#### Disable All Active Users
```python
sb.disable_all_active_users(username="admin")
```

#### Activate All Disabled Users
```python
sb.activate_all_disabled_users(username="admin")
```

#### Reset Admin Usage
```python
admin = sb.reset_admin_usage(username="admin")
```

#### Get Admin Usage
```python
usage = sb.get_admin_usage(username="admin")  # Returns bytes
```

### User Management

#### Get User
```python
user = sb.get_client(username="user123")
```

#### Get User by Subscription Token
```python
user = sb.get_client_by_subLink(token="subscription_token")
```

#### Add User
```python
user = sb.add_client(
    username="user123",
    inboundTag=["VLESS_INBOUND"],
    note="User note",
    enable="active",
    flow="xtls-rprx-vision",
    total_gb=10,
    expire_time=1735689600
)
```

#### Modify User
```python
user = sb.edit_client(
    username="user123",
    inboundTag=["VLESS_INBOUND", "VMESS_INBOUND"],
    note="Updated note",
    enable="active",
    flow="xtls-rprx-vision",
    total_gb=20,
    expire_time=0
)
```

#### Delete User
```python
sb.delete_client(username="user123")
```

#### Get Users
```python
users = sb.get_users(
    offset=0,
    limit=10,
    username=["user1", "user2"],
    search="query",
    admin=["admin1"],
    status="active",
    sort="created_at"
)
```

#### Reset User Data Usage
```python
user = sb.reset_user_data_usage(username="user123")
```

#### Revoke User Subscription
```python
user = sb.revoke_user_subscription(username="user123")
```

#### Get User Usage
```python
usage = sb.get_user_usage(
    username="user123",
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59"
)
```

#### Active Next Plan
```python
user = sb.active_next_plan(username="user123")
```

#### Set Owner
```python
user = sb.set_owner(username="user123", admin_username="admin")
```

#### Reset All Users Data Usage
```python
sb.reset_users_data_usage()
```

#### Get Users Usage
```python
usage = sb.get_users_usage(
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59",
    admin=["admin1"]
)
```

#### Get Expired Users
```python
expired = sb.get_expired_users(
    expired_after="2024-01-01T00:00:00",
    expired_before="2024-01-31T23:59:59"
)
```

#### Delete Expired Users
```python
deleted = sb.delete_expired_users(
    expired_after="2024-01-01T00:00:00",
    expired_before="2024-01-31T23:59:59"
)
```

### Node Management

#### Get Node Settings
```python
settings = sb.get_node_settings()
```

#### Add Node
```python
node = sb.add_node(
    name="Node 1",
    address="192.168.1.1",
    port=62050,
    api_port=62051,
    usage_coefficient=1.0,
    add_as_new_host=True
)
```

#### Get Node
```python
node = sb.get_node(node_id=1)
```

#### Get Nodes
```python
nodes = sb.get_nodes()
```

#### Modify Node
```python
node = sb.modify_node(
    node_id=1,
    name="Updated Node",
    address="192.168.1.2",
    status="connected"
)
```

#### Remove Node
```python
sb.remove_node(node_id=1)
```

#### Reconnect Node
```python
sb.reconnect_node(node_id=1)
```

#### Get Nodes Usage
```python
usage = sb.get_usage(
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59"
)
```

### Core Management

#### Get Core Stats
```python
stats = sb.get_core_stats()
```

#### Restart Core
```python
sb.restart_core()
```

#### Get Core Config
```python
config = sb.get_core_config()
```

#### Modify Core Config
```python
config = sb.modify_core_config({"key": "value"})
```

### System Management

#### Get System Stats
```python
stats = sb.get_system_stats()
```

#### Get Inbounds
```python
inbounds = sb.get_inbounds()
```

#### Get Hosts
```python
hosts = sb.get_hosts()
```

#### Modify Hosts
```python
hosts = sb.modify_hosts({
    "inbound_tag": [
        {
            "remark": "Host 1",
            "address": "example.com",
            "port": 443
        }
    ]
})
```

### User Template Management

#### Add User Template
```python
template = sb.add_user_template(
    name="Template 1",
    data_limit=10737418240,  # 10GB in bytes
    expire_duration=2592000,  # 30 days in seconds
    username_prefix="user_",
    username_suffix="_suffix",
    inbounds={
        "vless": ["VLESS_INBOUND"],
        "vmess": ["VMESS_INBOUND"]
    }
)
```

#### Get User Templates
```python
templates = sb.get_user_templates(offset=0, limit=10)
```

#### Get User Template
```python
template = sb.get_user_template(template_id=1)
```

#### Modify User Template
```python
template = sb.modify_user_template(
    template_id=1,
    name="Updated Template",
    data_limit=21474836480  # 20GB
)
```

#### Remove User Template
```python
sb.remove_user_template(template_id=1)
```

### Subscription Management

#### Get User Subscription
```python
subscription = sb.user_subscription(
    token="subscription_token",
    user_agent="Clash"
)
```

#### Get User Subscription Info
```python
info = sb.user_subscription_info(token="subscription_token")
```

#### Get User Subscription Usage
```python
usage = sb.user_get_usage(
    token="subscription_token",
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59"
)
```

#### Get User Subscription with Client Type
```python
subscription = sb.user_subscription_with_client_type(
    token="subscription_token",
    client_type="clash",  # sing-box, clash-meta, clash, outline, v2ray, v2ray-json
    user_agent="Clash"
)
```

## Error Handling

The SDK provides comprehensive error handling:

```python
from sarban.errors import (
    BadLogin,
    Unauthorized,
    Forbidden,
    NotFound,
    Conflict,
    BadRequest,
    ValidationError,
    HTTPException
)

try:
    user = sb.get_client(username="nonexistent")
except NotFound:
    print("User not found")
except Unauthorized:
    print("Not authenticated")
except Forbidden:
    print("Access denied")
except ValidationError as e:
    print(f"Validation error: {e}")
```

## Subscription Link Generator

```python
from sarban.sub_gen import sub_generator

subscription_link = sub_generator(
    userToken="token",
    fullAddress="sub.example.com:2096",
    verify=True
)
```

## License

MIT License

## Author

liwyd

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
