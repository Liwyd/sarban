# SARBAN - Complete Documentation

SARBAN is a powerful Python library that provides a simple and intuitive interface for managing your Marzban panel. Whether you're automating user management, monitoring system resources, or building custom integrations, SARBAN makes it easy to interact with the Marzban API.

## Table of Contents

1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Authentication](#authentication)
4. [Admin Management](#admin-management)
5. [User Management](#user-management)
6. [Node Management](#node-management)
7. [Core Management](#core-management)
8. [System Management](#system-management)
9. [User Templates](#user-templates)
10. [Subscriptions](#subscriptions)
11. [Error Handling](#error-handling)
12. [Advanced Usage](#advanced-usage)
13. [Best Practices](#best-practices)
14. [Troubleshooting](#troubleshooting)

## Installation

Install SARBAN using pip:

```bash
pip install sarban
```

For the latest development version:

```bash
pip install git+https://github.com/liwyd/sarban.git
```

### Requirements

- Python 3.6 or higher
- requests library (automatically installed)

## Getting Started

### Basic Setup

First, import the SARBAN class and create an instance:

```python
from sarban import SARBAN

# Create a SARBAN instance
sb = SARBAN(
    full_address="https://your-panel.com:2087",
    https=True
)
```

The `full_address` parameter can be:
- A full URL: `"https://panel.example.com:2087"`
- Just the domain: `"panel.example.com:2087"` (protocol will be added automatically)

The `https` parameter determines whether to use HTTPS (default: True).

### Your First Request

After creating an instance, you need to authenticate:

```python
try:
    sb.login("your_username", "your_password")
    print("Successfully logged in!")
except Exception as e:
    print(f"Login failed: {e}")
```

Once logged in, you can start making API calls. The authentication token is stored automatically and used for all subsequent requests.

## Authentication

### Login

The `login()` method authenticates with the Marzban panel and retrieves an access token:

```python
sb.login(username="admin", password="secure_password")
```

**Important Notes:**
- You must login before making any API calls (except subscription endpoints)
- The token is stored internally and used automatically
- If you're already logged in, calling `login()` again will raise an `AlreadyLogin` error

### Checking Authentication Status

While there's no explicit "check auth" method, you can verify your authentication by making a simple API call:

```python
try:
    admin = sb.get_current_admin()
    print(f"Authenticated as: {admin['username']}")
except Unauthorized:
    print("Not authenticated")
```

## Admin Management

### Get Current Admin

Retrieve information about the currently authenticated admin:

```python
admin = sb.get_current_admin()
print(f"Username: {admin['username']}")
print(f"Is Sudo: {admin['is_sudo']}")
print(f"Telegram ID: {admin.get('telegram_id')}")
```

### Create Admin

Create a new admin account. Only sudo admins can create other admins:

```python
new_admin = sb.create_admin(
    username="new_admin",
    password="strong_password_123",
    is_sudo=False,
    telegram_id=123456789,
    discord_webhook="https://discord.com/api/webhooks/..."
)
```

**Parameters:**
- `username` (required): Admin username
- `password` (required): Admin password
- `is_sudo` (optional): Whether admin has sudo privileges (default: False)
- `telegram_id` (optional): Telegram ID for notifications
- `discord_webhook` (optional): Discord webhook URL
- `users_usage` (optional): Usage limit for users under this admin

### Get All Admins

Retrieve a list of all admins with optional filtering:

```python
# Get all admins
all_admins = sb.get_admins()

# Get with pagination
admins = sb.get_admins(offset=0, limit=10)

# Search by username
admin = sb.get_admins(username="specific_admin")
```

### Modify Admin

Update an existing admin's details:

```python
updated = sb.modify_admin(
    username="admin",
    password="new_password",
    is_sudo=True,
    telegram_id=987654321
)
```

You only need to provide the fields you want to update. Omitted fields remain unchanged.

### Remove Admin

Delete an admin account:

```python
sb.remove_admin(username="admin_to_remove")
```

**Warning:** This action cannot be undone. Make sure you have at least one sudo admin remaining.

### Admin User Management

Disable all active users under a specific admin:

```python
sb.disable_all_active_users(username="admin")
```

Activate all disabled users:

```python
sb.activate_all_disabled_users(username="admin")
```

### Admin Usage

Get usage statistics for an admin:

```python
usage_bytes = sb.get_admin_usage(username="admin")
usage_gb = usage_bytes / (1024 ** 3)
print(f"Admin usage: {usage_gb:.2f} GB")
```

Reset admin usage:

```python
sb.reset_admin_usage(username="admin")
```

## User Management

### Get User

Retrieve a single user by username:

```python
user = sb.get_client(username="user123")
print(f"Status: {user['status']}")
print(f"Used traffic: {user['used_traffic']} bytes")
print(f"Data limit: {user.get('data_limit')}")
```

### Get User by Subscription Token

If you have a subscription token, you can retrieve user information without authentication:

```python
user = sb.get_client_by_subLink(token="subscription_token_here")
```

### Add User

Create a new user account:

```python
import time

new_user = sb.add_client(
    username="newuser",
    inboundTag=["VLESS_TCP", "VLESS_GRPC"],
    note="Customer from website",
    enable="active",
    flow="xtls-rprx-vision",
    total_gb=50,
    expire_time=int(time.time()) + (30 * 24 * 60 * 60)  # 30 days from now
)
```

**Parameters Explained:**
- `username`: 3-32 characters, alphanumeric and underscores only
- `inboundTag`: List of inbound tags the user can access
- `note`: Optional note for your records
- `enable`: User status ("active" or "on_hold")
- `flow`: Flow setting for VLESS (usually "xtls-rprx-vision")
- `total_gb`: Data limit in gigabytes (0 = unlimited)
- `expire_time`: Unix timestamp for expiration (0 = never expires)

**Proxies Configuration:**

For different proxy types, you need to configure proxies differently:

```python
# For VMESS
user = sb.add_client(
    username="vmess_user",
    inboundTag=["VMESS_WS"],
    proxies={
        "vmess": {
            "id": "auto-generated-uuid"
        }
    }
)

# For VLESS
user = sb.add_client(
    username="vless_user",
    inboundTag=["VLESS_TCP"],
    proxies={
        "vless": {
            "flow": "xtls-rprx-vision"
        }
    }
)
```

### Modify User

Update an existing user:

```python
updated = sb.edit_client(
    username="user123",
    inboundTag=["VLESS_TCP", "VMESS_WS"],
    note="Updated note",
    enable="active",
    total_gb=100,
    expire_time=0  # Remove expiration
)
```

**Important:** Only provide parameters you want to change. The method will update only the specified fields.

### Delete User

Remove a user account:

```python
sb.delete_client(username="user123")
```

### Get Users List

Retrieve multiple users with advanced filtering:

```python
# Get all users (paginated)
users_response = sb.get_users(offset=0, limit=50)
print(f"Total users: {users_response['total']}")
for user in users_response['users']:
    print(f"  - {user['username']}: {user['status']}")

# Filter by status
active_users = sb.get_users(status="active", limit=100)

# Search by username
specific_users = sb.get_users(username=["user1", "user2", "user3"])

# Search by admin
admin_users = sb.get_users(admin=["admin1", "admin2"])

# Text search
search_results = sb.get_users(search="keyword")

# Sort results
sorted_users = sb.get_users(sort="created_at", limit=20)
```

### User Usage Management

Reset a single user's data usage:

```python
sb.reset_user_data_usage(username="user123")
```

Reset all users' data usage:

```python
sb.reset_users_data_usage()
```

Get usage statistics for a user:

```python
from datetime import datetime, timedelta

# Get usage for last 30 days
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

usage = sb.get_user_usage(
    username="user123",
    start=start_date.isoformat(),
    end=end_date.isoformat()
)

for usage_entry in usage['usages']:
    print(f"Node: {usage_entry['node_name']}")
    print(f"Used: {usage_entry['used_traffic'] / (1024**3):.2f} GB")
```

Get usage for all users:

```python
usage = sb.get_users_usage(
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59",
    admin=["admin1"]  # Optional: filter by admin
)
```

### Subscription Management

Revoke a user's subscription (regenerates token):

```python
user = sb.revoke_user_subscription(username="user123")
print(f"New subscription URL: {user['subscription_url']}")
```

### User Ownership

Change the owner (admin) of a user:

```python
sb.set_owner(username="user123", admin_username="new_admin")
```

### Next Plan Feature

Activate the next plan for a user (if configured):

```python
user = sb.active_next_plan(username="user123")
```

### Expired Users

Find users who expired in a date range:

```python
expired = sb.get_expired_users(
    expired_after="2024-01-01T00:00:00",
    expired_before="2024-01-31T23:59:59"
)
print(f"Found {len(expired)} expired users")
```

Delete expired users:

```python
deleted = sb.delete_expired_users(
    expired_after="2024-01-01T00:00:00",
    expired_before="2024-01-31T23:59:59"
)
print(f"Deleted {len(deleted)} users")
```

## Node Management

### Get Node Settings

Retrieve node configuration settings:

```python
settings = sb.get_node_settings()
print(f"Min node version: {settings['min_node_version']}")
print(f"Certificate: {settings['certificate'][:50]}...")
```

### Add Node

Add a new node to your Marzban setup:

```python
node = sb.add_node(
    name="US Node 1",
    address="192.168.1.100",
    port=62050,
    api_port=62051,
    usage_coefficient=1.0,
    add_as_new_host=True
)
```

**Parameters:**
- `name`: Friendly name for the node
- `address`: IP address or hostname
- `port`: Node communication port (default: 62050)
- `api_port`: API port (default: 62051)
- `usage_coefficient`: Multiplier for usage tracking (default: 1.0)
- `add_as_new_host`: Whether to add as a new host (default: True)

### Get Node

Retrieve information about a specific node:

```python
node = sb.get_node(node_id=1)
print(f"Name: {node['name']}")
print(f"Status: {node['status']}")
print(f"Xray version: {node.get('xray_version')}")
```

### Get All Nodes

List all nodes:

```python
nodes = sb.get_nodes()
for node in nodes:
    print(f"{node['id']}: {node['name']} - {node['status']}")
```

### Modify Node

Update node configuration:

```python
updated = sb.modify_node(
    node_id=1,
    name="Updated Node Name",
    address="192.168.1.200",
    status="disabled"  # Can be: connected, connecting, error, disabled
)
```

### Remove Node

Delete a node:

```python
sb.remove_node(node_id=1)
```

### Reconnect Node

Force a node to reconnect:

```python
sb.reconnect_node(node_id=1)
```

### Node Usage Statistics

Get usage statistics for all nodes:

```python
usage = sb.get_usage(
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59"
)

for node_usage in usage['usages']:
    print(f"Node: {node_usage['node_name']}")
    print(f"  Uplink: {node_usage['uplink'] / (1024**3):.2f} GB")
    print(f"  Downlink: {node_usage['downlink'] / (1024**3):.2f} GB")
```

## Core Management

### Get Core Statistics

Retrieve core system information:

```python
stats = sb.get_core_stats()
print(f"Version: {stats['version']}")
print(f"Started: {stats['started']}")
print(f"Logs WebSocket: {stats['logs_websocket']}")
```

### Restart Core

Restart the Marzban core and all connected nodes:

```python
sb.restart_core()
print("Core restart initiated")
```

**Note:** This will temporarily disconnect all users.

### Get Core Configuration

Retrieve the current core configuration:

```python
config = sb.get_core_config()
# config is a dictionary with core settings
```

### Modify Core Configuration

Update core configuration (requires sudo):

```python
new_config = {
    "log_level": "warning",
    "xray_api": {
        "listen": "127.0.0.1",
        "port": 8080
    }
}

updated = sb.modify_core_config(new_config)
```

**Warning:** Incorrect configuration can break your Marzban installation. Always backup before making changes.

## System Management

### Get System Statistics

Get comprehensive system statistics:

```python
stats = sb.get_system_stats()
print(f"Version: {stats['version']}")
print(f"Memory: {stats['mem_used']}/{stats['mem_total']} MB")
print(f"CPU Usage: {stats['cpu_usage']}%")
print(f"Total Users: {stats['total_user']}")
print(f"Online Users: {stats['online_users']}")
print(f"Active Users: {stats['users_active']}")
print(f"Incoming Bandwidth: {stats['incoming_bandwidth'] / (1024**3):.2f} GB")
print(f"Outgoing Bandwidth: {stats['outgoing_bandwidth'] / (1024**3):.2f} GB")
```

### Get Inbounds

Retrieve all inbound configurations grouped by protocol:

```python
inbounds = sb.get_inbounds()

for protocol, inbound_list in inbounds.items():
    print(f"\n{protocol.upper()}:")
    for inbound in inbound_list:
        print(f"  Tag: {inbound['tag']}")
        print(f"  Network: {inbound['network']}")
        print(f"  Port: {inbound['port']}")
```

### Get Hosts

Get proxy hosts grouped by inbound tag:

```python
hosts = sb.get_hosts()

for inbound_tag, host_list in hosts.items():
    print(f"\n{inbound_tag}:")
    for host in host_list:
        print(f"  Remark: {host['remark']}")
        print(f"  Address: {host['address']}")
        print(f"  Port: {host.get('port')}")
```

### Modify Hosts

Update proxy host configurations:

```python
new_hosts = {
    "inbound_tag_1": [
        {
            "remark": "CDN Host 1",
            "address": "cdn.example.com",
            "port": 443,
            "sni": "cdn.example.com",
            "host": "cdn.example.com"
        }
    ],
    "inbound_tag_2": [
        {
            "remark": "Direct Host",
            "address": "direct.example.com",
            "port": 443
        }
    ]
}

updated = sb.modify_hosts(new_hosts)
```

## User Templates

User templates allow you to create reusable configurations for users.

### Add Template

Create a new user template:

```python
template = sb.add_user_template(
    name="Premium Plan",
    data_limit=107374182400,  # 100 GB in bytes
    expire_duration=2592000,  # 30 days in seconds
    username_prefix="prem_",
    username_suffix="",
    inbounds={
        "vless": ["VLESS_TCP", "VLESS_GRPC"],
        "vmess": ["VMESS_WS"]
    }
)
```

### Get Templates

List all templates:

```python
templates = sb.get_user_templates(offset=0, limit=10)
for template in templates:
    print(f"ID: {template['id']}, Name: {template.get('name')}")
```

### Get Template

Retrieve a specific template:

```python
template = sb.get_user_template(template_id=1)
```

### Modify Template

Update a template:

```python
updated = sb.modify_user_template(
    template_id=1,
    name="Updated Premium Plan",
    data_limit=214748364800  # 200 GB
)
```

### Remove Template

Delete a template:

```python
sb.remove_user_template(template_id=1)
```

## Subscriptions

Subscription endpoints allow users to retrieve their subscription links and information.

### Get Subscription

Get subscription content based on user agent:

```python
subscription = sb.user_subscription(
    token="user_subscription_token",
    user_agent="Clash"
)
# Returns subscription content in appropriate format
```

### Get Subscription Info

Retrieve detailed subscription information:

```python
info = sb.user_subscription_info(token="user_subscription_token")
print(f"Username: {info['username']}")
print(f"Status: {info['status']}")
print(f"Used Traffic: {info['used_traffic'] / (1024**3):.2f} GB")
print(f"Data Limit: {info.get('data_limit')}")
```

### Get Subscription Usage

Get usage statistics for subscription:

```python
usage = sb.user_get_usage(
    token="user_subscription_token",
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59"
)
```

### Get Subscription by Client Type

Get subscription in a specific format:

```python
# Available client types:
# - sing-box
# - clash-meta
# - clash
# - outline
# - v2ray
# - v2ray-json

subscription = sb.user_subscription_with_client_type(
    token="user_subscription_token",
    client_type="clash",
    user_agent="Clash"
)
```

## Error Handling

SARBAN provides comprehensive error handling. Always wrap API calls in try-except blocks:

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
    user = sb.get_client(username="user123")
except NotFound:
    print("User not found")
except Unauthorized:
    print("Please login first")
    sb.login("admin", "password")
except Forbidden:
    print("You don't have permission for this action")
except ValidationError as e:
    print(f"Invalid input: {e}")
except HTTPException as e:
    print(f"HTTP error {e.status_code}: {e}")
```

### Common Error Scenarios

**401 Unauthorized:**
- Token expired or invalid
- Not logged in
- Solution: Call `login()` again

**403 Forbidden:**
- Insufficient permissions
- Not a sudo admin trying to access sudo-only endpoints
- Solution: Use a sudo admin account

**404 Not Found:**
- Resource doesn't exist
- Invalid username, node_id, etc.
- Solution: Verify the resource exists

**409 Conflict:**
- Resource already exists (e.g., username taken)
- Solution: Use a different identifier

**422 Validation Error:**
- Invalid input parameters
- Solution: Check parameter format and requirements

## Advanced Usage

### Batch Operations

Process multiple users:

```python
usernames = ["user1", "user2", "user3"]
for username in usernames:
    try:
        sb.reset_user_data_usage(username)
        print(f"Reset {username}")
    except Exception as e:
        print(f"Failed to reset {username}: {e}")
```

### Monitoring Script

Create a monitoring script:

```python
import time
from datetime import datetime

while True:
    try:
        stats = sb.get_system_stats()
        print(f"[{datetime.now()}] Online: {stats['online_users']}/{stats['total_user']}")
        time.sleep(60)  # Check every minute
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(60)
```

### User Creation with Validation

```python
def create_user_safe(username, inbound_tag, total_gb):
    try:
        # Check if user exists
        existing = sb.get_client(username)
        print(f"User {username} already exists")
        return False
    except NotFound:
        pass
    
    try:
        user = sb.add_client(
            username=username,
            inboundTag=inbound_tag,
            total_gb=total_gb,
            expire_time=0
        )
        print(f"Created user: {username}")
        return True
    except Conflict:
        print(f"User {username} already exists")
        return False
    except ValidationError as e:
        print(f"Validation error: {e}")
        return False
```

### Usage Report Generator

```python
def generate_usage_report(start_date, end_date):
    users = sb.get_users(limit=1000)
    report = []
    
    for user in users['users']:
        try:
            usage = sb.get_user_usage(
                username=user['username'],
                start=start_date,
                end=end_date
            )
            total_usage = sum(u['used_traffic'] for u in usage['usages'])
            report.append({
                'username': user['username'],
                'usage_gb': total_usage / (1024**3)
            })
        except Exception as e:
            print(f"Error getting usage for {user['username']}: {e}")
    
    return sorted(report, key=lambda x: x['usage_gb'], reverse=True)
```

## Best Practices

1. **Always handle errors:** Wrap API calls in try-except blocks
2. **Reuse connections:** Create one SARBAN instance and reuse it
3. **Rate limiting:** Don't make too many requests too quickly
4. **Validate input:** Check parameters before making API calls
5. **Use pagination:** When fetching large lists, use offset/limit
6. **Log operations:** Keep logs of important operations
7. **Backup before changes:** Especially for core config modifications
8. **Test in development:** Test scripts before running in production

## Troubleshooting

### Connection Issues

**Problem:** Can't connect to panel
```python
# Check if address is correct
sb = SARBAN(full_address="https://panel.example.com:2087", https=True)

# Try with verify=False if SSL issues
sb = SARBAN(full_address="https://panel.example.com:2087", https=False)
```

### Authentication Problems

**Problem:** Login fails
- Verify username and password
- Check if panel is accessible
- Ensure you're using the correct admin account

### Permission Errors

**Problem:** 403 Forbidden errors
- Verify you're using a sudo admin account
- Check admin permissions in Marzban panel

### Timeout Issues

**Problem:** Requests timeout
- Check network connection
- Verify panel is running
- Increase timeout in base.py if needed (default: 30 seconds)

## Subscription Link Generator

Generate subscription links easily:

```python
from sarban.sub_gen import sub_generator

link = sub_generator(
    userToken="user_token_here",
    fullAddress="sub.example.com:2096",
    verify=True
)
print(link)  # https://sub.example.com:2096/sub/user_token_here/
```

## Support and Contributing

For issues, feature requests, or contributions, please visit the GitHub repository.

## License

MIT License - See LICENSE file for details.

