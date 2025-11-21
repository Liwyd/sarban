# SARBAN

A comprehensive Python SDK for managing Marzban panel ([Gozargah/Marzban](https://github.com/Gozargah/Marzban)) through its REST API.

## 📚 Documentation

### Quick Reference
- [English Quick Reference](README_EN.md)
- [Persian Quick Reference (فارسی)](README_FA.md)
- [Chinese Quick Reference (中文)](README_ZH.md)

### Complete Documentation
- [Complete English Documentation](DOCUMENTATION_EN.md) - Full guide with examples and best practices
- [Complete Persian Documentation (فارسی)](DOCUMENTATION_FA.md) - راهنمای کامل با مثال‌ها و بهترین روش‌ها
- [Complete Chinese Documentation (中文)](DOCUMENTATION_ZH.md) - 完整指南，包含示例和最佳实践

## ✨ Features

- ✅ Complete API coverage for all Marzban endpoints
- ✅ Admin management (create, modify, remove admins)
- ✅ User management (CRUD operations, usage tracking)
- ✅ Node management (add, modify, remove, reconnect nodes)
- ✅ Core configuration and statistics
- ✅ System statistics and monitoring
- ✅ User template management
- ✅ Subscription management
- ✅ Comprehensive error handling
- ✅ Type hints for better IDE support

## 🚀 Installation

```bash
pip install sarban
```

## 📦 Quick Start

```python
from sarban import SARBAN
from sarban.errors import BadLogin

# Initialize the client
sb = SARBAN(
    full_address="https://your-marzban-panel.com:2087",
    https=True
)

# Login
try:
    sb.login("admin_username", "admin_password")
    print("Login successful!")
except BadLogin:
    print("Invalid credentials")
```

## 📖 API Categories

### Authentication
- `login()` - Authenticate and get access token

### Admin Management
- `get_current_admin()` - Get current authenticated admin
- `create_admin()` - Create a new admin
- `get_admins()` - Get list of admins
- `modify_admin()` - Modify admin details
- `remove_admin()` - Remove an admin
- `disable_all_active_users()` - Disable all active users under admin
- `activate_all_disabled_users()` - Activate all disabled users under admin
- `reset_admin_usage()` - Reset admin usage
- `get_admin_usage()` - Get admin usage statistics

### User Management
- `get_client()` - Get user by username
- `get_client_by_subLink()` - Get user by subscription token
- `add_client()` - Add a new user
- `edit_client()` - Modify existing user
- `delete_client()` - Remove a user
- `get_users()` - Get list of users with filters
- `reset_user_data_usage()` - Reset user data usage
- `revoke_user_subscription()` - Revoke user subscription
- `get_user_usage()` - Get user usage statistics
- `active_next_plan()` - Activate next plan for user
- `set_owner()` - Set owner (admin) for user
- `reset_users_data_usage()` - Reset all users data usage
- `get_users_usage()` - Get all users usage statistics
- `get_expired_users()` - Get expired users
- `delete_expired_users()` - Delete expired users

### Node Management
- `get_node_settings()` - Get node settings
- `add_node()` - Add a new node
- `get_node()` - Get node by ID
- `get_nodes()` - Get all nodes
- `modify_node()` - Modify node details
- `remove_node()` - Remove a node
- `reconnect_node()` - Reconnect a node
- `get_usage()` - Get nodes usage statistics

### Core Management
- `get_core_stats()` - Get core statistics
- `restart_core()` - Restart the core
- `get_core_config()` - Get core configuration
- `modify_core_config()` - Modify core configuration

### System Management
- `get_system_stats()` - Get system statistics
- `get_inbounds()` - Get inbound configurations
- `get_hosts()` - Get proxy hosts
- `modify_hosts()` - Modify proxy hosts

### User Template Management
- `add_user_template()` - Add a new user template
- `get_user_templates()` - Get list of user templates
- `get_user_template()` - Get user template by ID
- `modify_user_template()` - Modify user template
- `remove_user_template()` - Remove user template

### Subscription Management
- `user_subscription()` - Get user subscription
- `user_subscription_info()` - Get subscription info
- `user_get_usage()` - Get subscription usage
- `user_subscription_with_client_type()` - Get subscription by client type

## 🔧 Error Handling

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
```

## 🔗 Subscription Link Generator

```python
from sarban.sub_gen import sub_generator

subscription_link = sub_generator(
    userToken="token",
    fullAddress="sub.example.com:2096",
    verify=True
)
```

## 📝 Example Usage

```python
from sarban import SARBAN

sb = SARBAN(full_address="https://panel.example.com:2087", https=True)
sb.login("admin", "password")

# Get all users
users = sb.get_users(limit=10)

# Add a new user
new_user = sb.add_client(
    username="test_user",
    inboundTag=["VLESS_INBOUND"],
    total_gb=10,
    expire_time=1735689600
)

# Get system stats
stats = sb.get_system_stats()
print(f"Total users: {stats['total_user']}")
print(f"Online users: {stats['online_users']}")
```

## 📄 License

MIT License

## 👤 Author

liwyd

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🔗 Links

- [Marzban Project](https://github.com/Gozargah/Marzban)
- [PyPI Package](https://pypi.org/project/sarban/)
