# SARBAN - 完整文档

SARBAN 是一个强大的 Python 库，为管理您的 Marzban 面板提供了简单直观的接口。无论您是要自动化用户管理、监控系统资源还是构建自定义集成，SARBAN 都能让与 Marzban API 的交互变得简单。

## 目录

1. [安装](#安装)
2. [快速开始](#快速开始)
3. [身份验证](#身份验证)
4. [管理员管理](#管理员管理)
5. [用户管理](#用户管理)
6. [节点管理](#节点管理)
7. [核心管理](#核心管理)
8. [系统管理](#系统管理)
9. [用户模板](#用户模板)
10. [订阅管理](#订阅管理)
11. [错误处理](#错误处理)
12. [高级用法](#高级用法)
13. [最佳实践](#最佳实践)
14. [故障排除](#故障排除)

## 安装

使用 pip 安装 SARBAN：

```bash
pip install sarban
```

开发版本：

```bash
pip install git+https://github.com/liwyd/sarban.git
```

### 要求

- Python 3.6 或更高版本
- requests 库（自动安装）

## 快速开始

### 基本设置

首先，导入 SARBAN 类并创建实例：

```python
from sarban import SARBAN

# 创建 SARBAN 实例
sb = SARBAN(
    full_address="https://your-panel.com:2087",
    https=True
)
```

`full_address` 参数可以是：
- 完整 URL：`"https://panel.example.com:2087"`
- 仅域名：`"panel.example.com:2087"`（协议会自动添加）

`https` 参数决定是否使用 HTTPS（默认：True）。

### 您的第一个请求

创建实例后，需要身份验证：

```python
try:
    sb.login("your_username", "your_password")
    print("登录成功！")
except Exception as e:
    print(f"登录失败: {e}")
```

登录后，您可以开始进行 API 调用。身份验证令牌会自动存储并用于所有后续请求。

## 身份验证

### 登录

`login()` 方法与 Marzban 面板进行身份验证并获取访问令牌：

```python
sb.login(username="admin", password="secure_password")
```

**重要提示：**
- 在进行任何 API 调用之前必须登录（订阅端点除外）
- 令牌在内部存储并自动使用
- 如果已经登录，再次调用 `login()` 会引发 `AlreadyLogin` 错误

### 检查身份验证状态

虽然没有明确的"检查身份验证"方法，但您可以通过进行简单的 API 调用来验证身份验证：

```python
try:
    admin = sb.get_current_admin()
    print(f"已身份验证为: {admin['username']}")
except Unauthorized:
    print("未身份验证")
```

## 管理员管理

### 获取当前管理员

获取当前已身份验证的管理员信息：

```python
admin = sb.get_current_admin()
print(f"用户名: {admin['username']}")
print(f"是否 Sudo: {admin['is_sudo']}")
print(f"Telegram ID: {admin.get('telegram_id')}")
```

### 创建管理员

创建新的管理员账户。只有 sudo 管理员可以创建其他管理员：

```python
new_admin = sb.create_admin(
    username="new_admin",
    password="strong_password_123",
    is_sudo=False,
    telegram_id=123456789,
    discord_webhook="https://discord.com/api/webhooks/..."
)
```

**参数：**
- `username`（必需）：管理员用户名
- `password`（必需）：管理员密码
- `is_sudo`（可选）：管理员是否具有 sudo 权限（默认：False）
- `telegram_id`（可选）：用于通知的 Telegram ID
- `discord_webhook`（可选）：Discord webhook URL
- `users_usage`（可选）：此管理员下用户的使用限制

### 获取所有管理员

使用可选过滤获取所有管理员的列表：

```python
# 获取所有管理员
all_admins = sb.get_admins()

# 分页获取
admins = sb.get_admins(offset=0, limit=10)

# 按用户名搜索
admin = sb.get_admins(username="specific_admin")
```

### 修改管理员

更新现有管理员的详细信息：

```python
updated = sb.modify_admin(
    username="admin",
    password="new_password",
    is_sudo=True,
    telegram_id=987654321
)
```

您只需要提供要更新的字段。省略的字段保持不变。

### 删除管理员

删除管理员账户：

```python
sb.remove_admin(username="admin_to_remove")
```

**警告：** 此操作无法撤销。确保至少保留一个 sudo 管理员。

### 管理员用户管理

禁用特定管理员下的所有活跃用户：

```python
sb.disable_all_active_users(username="admin")
```

激活所有禁用的用户：

```python
sb.activate_all_disabled_users(username="admin")
```

### 管理员使用量

获取管理员的使用统计：

```python
usage_bytes = sb.get_admin_usage(username="admin")
usage_gb = usage_bytes / (1024 ** 3)
print(f"管理员使用量: {usage_gb:.2f} GB")
```

重置管理员使用量：

```python
sb.reset_admin_usage(username="admin")
```

## 用户管理

### 获取用户

按用户名获取单个用户：

```python
user = sb.get_client(username="user123")
print(f"状态: {user['status']}")
print(f"已用流量: {user['used_traffic']} 字节")
print(f"数据限制: {user.get('data_limit')}")
```

### 通过订阅令牌获取用户

如果您有订阅令牌，可以在不进行身份验证的情况下获取用户信息：

```python
user = sb.get_client_by_subLink(token="subscription_token_here")
```

### 添加用户

创建新的用户账户：

```python
import time

new_user = sb.add_client(
    username="newuser",
    inboundTag=["VLESS_TCP", "VLESS_GRPC"],
    note="来自网站的客户",
    enable="active",
    flow="xtls-rprx-vision",
    total_gb=50,
    expire_time=int(time.time()) + (30 * 24 * 60 * 60)  # 从现在起 30 天
)
```

**参数说明：**
- `username`：3-32 个字符，仅字母数字和下划线
- `inboundTag`：用户可以访问的入站标签列表
- `note`：可选备注
- `enable`：用户状态（"active" 或 "on_hold"）
- `flow`：VLESS 的流设置（通常为 "xtls-rprx-vision"）
- `total_gb`：数据限制（GB）（0 = 无限制）
- `expire_time`：过期的 Unix 时间戳（0 = 永不过期）

**代理配置：**

对于不同的代理类型，需要以不同方式配置代理：

```python
# 对于 VMESS
user = sb.add_client(
    username="vmess_user",
    inboundTag=["VMESS_WS"],
    proxies={
        "vmess": {
            "id": "auto-generated-uuid"
        }
    }
)

# 对于 VLESS
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

### 修改用户

更新现有用户：

```python
updated = sb.edit_client(
    username="user123",
    inboundTag=["VLESS_TCP", "VMESS_WS"],
    note="更新的备注",
    enable="active",
    total_gb=100,
    expire_time=0  # 移除过期
)
```

**重要：** 只提供要更改的参数。该方法只会更新指定的字段。

### 删除用户

删除用户账户：

```python
sb.delete_client(username="user123")
```

### 获取用户列表

使用高级过滤获取多个用户：

```python
# 获取所有用户（分页）
users_response = sb.get_users(offset=0, limit=50)
print(f"总用户数: {users_response['total']}")
for user in users_response['users']:
    print(f"  - {user['username']}: {user['status']}")

# 按状态过滤
active_users = sb.get_users(status="active", limit=100)

# 按用户名搜索
specific_users = sb.get_users(username=["user1", "user2", "user3"])

# 按管理员搜索
admin_users = sb.get_users(admin=["admin1", "admin2"])

# 文本搜索
search_results = sb.get_users(search="keyword")

# 排序结果
sorted_users = sb.get_users(sort="created_at", limit=20)
```

### 用户使用量管理

重置单个用户的数据使用量：

```python
sb.reset_user_data_usage(username="user123")
```

重置所有用户的数据使用量：

```python
sb.reset_users_data_usage()
```

获取用户的使用统计：

```python
from datetime import datetime, timedelta

# 获取过去 30 天的使用量
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

usage = sb.get_user_usage(
    username="user123",
    start=start_date.isoformat(),
    end=end_date.isoformat()
)

for usage_entry in usage['usages']:
    print(f"节点: {usage_entry['node_name']}")
    print(f"已用: {usage_entry['used_traffic'] / (1024**3):.2f} GB")
```

获取所有用户的使用量：

```python
usage = sb.get_users_usage(
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59",
    admin=["admin1"]  # 可选：按管理员过滤
)
```

### 订阅管理

撤销用户的订阅（重新生成令牌）：

```python
user = sb.revoke_user_subscription(username="user123")
print(f"新订阅 URL: {user['subscription_url']}")
```

### 用户所有权

更改用户的所有者（管理员）：

```python
sb.set_owner(username="user123", admin_username="new_admin")
```

### 下一个计划功能

为用户激活下一个计划（如果已配置）：

```python
user = sb.active_next_plan(username="user123")
```

### 过期用户

查找在日期范围内过期的用户：

```python
expired = sb.get_expired_users(
    expired_after="2024-01-01T00:00:00",
    expired_before="2024-01-31T23:59:59"
)
print(f"找到 {len(expired)} 个过期用户")
```

删除过期用户：

```python
deleted = sb.delete_expired_users(
    expired_after="2024-01-01T00:00:00",
    expired_before="2024-01-31T23:59:59"
)
print(f"删除了 {len(deleted)} 个用户")
```

## 节点管理

### 获取节点设置

获取节点配置设置：

```python
settings = sb.get_node_settings()
print(f"最小节点版本: {settings['min_node_version']}")
print(f"证书: {settings['certificate'][:50]}...")
```

### 添加节点

向您的 Marzban 设置添加新节点：

```python
node = sb.add_node(
    name="美国节点 1",
    address="192.168.1.100",
    port=62050,
    api_port=62051,
    usage_coefficient=1.0,
    add_as_new_host=True
)
```

**参数：**
- `name`：节点的友好名称
- `address`：IP 地址或主机名
- `port`：节点通信端口（默认：62050）
- `api_port`：API 端口（默认：62051）
- `usage_coefficient`：使用跟踪的乘数（默认：1.0）
- `add_as_new_host`：是否添加为新主机（默认：True）

### 获取节点

获取特定节点的信息：

```python
node = sb.get_node(node_id=1)
print(f"名称: {node['name']}")
print(f"状态: {node['status']}")
print(f"Xray 版本: {node.get('xray_version')}")
```

### 获取所有节点

列出所有节点：

```python
nodes = sb.get_nodes()
for node in nodes:
    print(f"{node['id']}: {node['name']} - {node['status']}")
```

### 修改节点

更新节点配置：

```python
updated = sb.modify_node(
    node_id=1,
    name="更新的节点名称",
    address="192.168.1.200",
    status="disabled"  # 可以是：connected, connecting, error, disabled
)
```

### 删除节点

删除节点：

```python
sb.remove_node(node_id=1)
```

### 重新连接节点

强制节点重新连接：

```python
sb.reconnect_node(node_id=1)
```

### 节点使用统计

获取所有节点的使用统计：

```python
usage = sb.get_usage(
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59"
)

for node_usage in usage['usages']:
    print(f"节点: {node_usage['node_name']}")
    print(f"  上行: {node_usage['uplink'] / (1024**3):.2f} GB")
    print(f"  下行: {node_usage['downlink'] / (1024**3):.2f} GB")
```

## 核心管理

### 获取核心统计

获取核心系统信息：

```python
stats = sb.get_core_stats()
print(f"版本: {stats['version']}")
print(f"已启动: {stats['started']}")
print(f"日志 WebSocket: {stats['logs_websocket']}")
```

### 重启核心

重启 Marzban 核心和所有连接的节点：

```python
sb.restart_core()
print("核心重启已启动")
```

**注意：** 这将暂时断开所有用户的连接。

### 获取核心配置

获取当前核心配置：

```python
config = sb.get_core_config()
# config 是包含核心设置的字典
```

### 修改核心配置

更新核心配置（需要 sudo）：

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

**警告：** 不正确的配置可能会破坏您的 Marzban 安装。在进行更改之前始终备份。

## 系统管理

### 获取系统统计

获取全面的系统统计：

```python
stats = sb.get_system_stats()
print(f"版本: {stats['version']}")
print(f"内存: {stats['mem_used']}/{stats['mem_total']} MB")
print(f"CPU 使用率: {stats['cpu_usage']}%")
print(f"总用户数: {stats['total_user']}")
print(f"在线用户: {stats['online_users']}")
print(f"活跃用户: {stats['users_active']}")
print(f"入站带宽: {stats['incoming_bandwidth'] / (1024**3):.2f} GB")
print(f"出站带宽: {stats['outgoing_bandwidth'] / (1024**3):.2f} GB")
```

### 获取入站

按协议分组获取所有入站配置：

```python
inbounds = sb.get_inbounds()

for protocol, inbound_list in inbounds.items():
    print(f"\n{protocol.upper()}:")
    for inbound in inbound_list:
        print(f"  标签: {inbound['tag']}")
        print(f"  网络: {inbound['network']}")
        print(f"  端口: {inbound['port']}")
```

### 获取主机

按入站标签分组获取代理主机：

```python
hosts = sb.get_hosts()

for inbound_tag, host_list in hosts.items():
    print(f"\n{inbound_tag}:")
    for host in host_list:
        print(f"  备注: {host['remark']}")
        print(f"  地址: {host['address']}")
        print(f"  端口: {host.get('port')}")
```

### 修改主机

更新代理主机配置：

```python
new_hosts = {
    "inbound_tag_1": [
        {
            "remark": "CDN 主机 1",
            "address": "cdn.example.com",
            "port": 443,
            "sni": "cdn.example.com",
            "host": "cdn.example.com"
        }
    ],
    "inbound_tag_2": [
        {
            "remark": "直连主机",
            "address": "direct.example.com",
            "port": 443
        }
    ]
}

updated = sb.modify_hosts(new_hosts)
```

## 用户模板

用户模板允许您为用户创建可重用的配置。

### 添加模板

创建新的用户模板：

```python
template = sb.add_user_template(
    name="高级计划",
    data_limit=107374182400,  # 100 GB（字节）
    expire_duration=2592000,  # 30 天（秒）
    username_prefix="prem_",
    username_suffix="",
    inbounds={
        "vless": ["VLESS_TCP", "VLESS_GRPC"],
        "vmess": ["VMESS_WS"]
    }
)
```

### 获取模板

列出所有模板：

```python
templates = sb.get_user_templates(offset=0, limit=10)
for template in templates:
    print(f"ID: {template['id']}, 名称: {template.get('name')}")
```

### 获取模板

获取特定模板：

```python
template = sb.get_user_template(template_id=1)
```

### 修改模板

更新模板：

```python
updated = sb.modify_user_template(
    template_id=1,
    name="更新的高级计划",
    data_limit=214748364800  # 200 GB
)
```

### 删除模板

删除模板：

```python
sb.remove_user_template(template_id=1)
```

## 订阅管理

订阅端点允许用户检索其订阅链接和信息。

### 获取订阅

根据用户代理获取订阅内容：

```python
subscription = sb.user_subscription(
    token="user_subscription_token",
    user_agent="Clash"
)
# 以适当的格式返回订阅内容
```

### 获取订阅信息

检索详细的订阅信息：

```python
info = sb.user_subscription_info(token="user_subscription_token")
print(f"用户名: {info['username']}")
print(f"状态: {info['status']}")
print(f"已用流量: {info['used_traffic'] / (1024**3):.2f} GB")
print(f"数据限制: {info.get('data_limit')}")
```

### 获取订阅使用量

获取订阅的使用统计：

```python
usage = sb.user_get_usage(
    token="user_subscription_token",
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59"
)
```

### 按客户端类型获取订阅

以特定格式获取订阅：

```python
# 可用的客户端类型：
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

## 错误处理

SARBAN 提供全面的错误处理。始终将 API 调用包装在 try-except 块中：

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
    print("未找到用户")
except Unauthorized:
    print("请先登录")
    sb.login("admin", "password")
except Forbidden:
    print("您没有执行此操作的权限")
except ValidationError as e:
    print(f"无效输入: {e}")
except HTTPException as e:
    print(f"HTTP 错误 {e.status_code}: {e}")
```

### 常见错误场景

**401 Unauthorized：**
- 令牌过期或无效
- 未登录
- 解决方案：再次调用 `login()`

**403 Forbidden：**
- 权限不足
- 不是 sudo 管理员尝试访问仅 sudo 的端点
- 解决方案：使用 sudo 管理员账户

**404 Not Found：**
- 资源不存在
- 无效的用户名、node_id 等
- 解决方案：验证资源是否存在

**409 Conflict：**
- 资源已存在（例如，用户名已被占用）
- 解决方案：使用不同的标识符

**422 Validation Error：**
- 无效的输入参数
- 解决方案：检查参数格式和要求

## 高级用法

### 批量操作

处理多个用户：

```python
usernames = ["user1", "user2", "user3"]
for username in usernames:
    try:
        sb.reset_user_data_usage(username)
        print(f"已重置 {username}")
    except Exception as e:
        print(f"重置 {username} 失败: {e}")
```

### 监控脚本

创建监控脚本：

```python
import time
from datetime import datetime

while True:
    try:
        stats = sb.get_system_stats()
        print(f"[{datetime.now()}] 在线: {stats['online_users']}/{stats['total_user']}")
        time.sleep(60)  # 每分钟检查
    except Exception as e:
        print(f"错误: {e}")
        time.sleep(60)
```

### 带验证的用户创建

```python
def create_user_safe(username, inbound_tag, total_gb):
    try:
        # 检查用户是否存在
        existing = sb.get_client(username)
        print(f"用户 {username} 已存在")
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
        print(f"已创建用户: {username}")
        return True
    except Conflict:
        print(f"用户 {username} 已存在")
        return False
    except ValidationError as e:
        print(f"验证错误: {e}")
        return False
```

### 使用量报告生成器

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
            print(f"获取 {user['username']} 的使用量时出错: {e}")
    
    return sorted(report, key=lambda x: x['usage_gb'], reverse=True)
```

## 最佳实践

1. **始终处理错误：** 将 API 调用包装在 try-except 块中
2. **重用连接：** 创建一个 SARBAN 实例并重用
3. **速率限制：** 不要过快发送太多请求
4. **验证输入：** 在进行 API 调用之前检查参数
5. **使用分页：** 获取大列表时使用 offset/limit
6. **记录操作：** 保留重要操作的日志
7. **更改前备份：** 特别是核心配置修改
8. **在开发中测试：** 在生产环境运行之前在开发环境中测试脚本

## 故障排除

### 连接问题

**问题：** 无法连接到面板
```python
# 检查地址是否正确
sb = SARBAN(full_address="https://panel.example.com:2087", https=True)

# 如果有 SSL 问题，尝试 verify=False
sb = SARBAN(full_address="https://panel.example.com:2087", https=False)
```

### 身份验证问题

**问题：** 登录失败
- 验证用户名和密码
- 检查面板是否可访问
- 确保使用正确的管理员账户

### 权限错误

**问题：** 403 Forbidden 错误
- 验证您使用的是 sudo 管理员账户
- 在 Marzban 面板中检查管理员权限

### 超时问题

**问题：** 请求超时
- 检查网络连接
- 验证面板是否正在运行
- 如需要，在 base.py 中增加超时（默认：30 秒）

## 订阅链接生成器

轻松生成订阅链接：

```python
from sarban.sub_gen import sub_generator

link = sub_generator(
    userToken="user_token_here",
    fullAddress="sub.example.com:2096",
    verify=True
)
print(link)  # https://sub.example.com:2096/sub/user_token_here/
```

## 支持和贡献

如有问题、功能请求或贡献，请访问 GitHub 仓库。

## 许可证

MIT 许可证 - 详细信息请参阅 LICENSE 文件。

