# SARBAN

一个用于通过 REST API 管理 Marzban 面板 ([Gozargah/Marzban](https://github.com/Gozargah/Marzban)) 的完整 Python SDK。

## 功能

- 完整的 Marzban API 端点覆盖
- 管理员管理（创建、修改、删除管理员）
- 用户管理（CRUD 操作、使用跟踪）
- 节点管理（添加、修改、删除、重连节点）
- 核心配置和统计
- 系统统计和监控
- 用户模板管理
- 订阅管理
- 全面的错误处理
- 类型提示以更好地支持 IDE

## 安装

```bash
pip install sarban
```

## 快速开始

```python
from sarban import SARBAN
from sarban.errors import BadLogin, Unauthorized

# 初始化客户端
sb = SARBAN(
    full_address="https://your-marzban-panel.com:2087",
    https=True
)

# 登录
try:
    sb.login("admin_username", "admin_password")
except BadLogin:
    print("凭据无效")
```

## API 参考

### 身份验证

#### 登录
```python
sb.login(username: str, password: str) -> bool
```

### 管理员管理

#### 获取当前管理员
```python
admin = sb.get_current_admin()
```

#### 创建管理员
```python
admin = sb.create_admin(
    username="new_admin",
    password="secure_password",
    is_sudo=False,
    telegram_id=123456789,
    discord_webhook="https://discord.com/webhook/..."
)
```

#### 获取管理员列表
```python
admins = sb.get_admins(offset=0, limit=10, username="admin")
```

#### 修改管理员
```python
admin = sb.modify_admin(
    username="admin",
    password="new_password",
    is_sudo=True
)
```

#### 删除管理员
```python
sb.remove_admin(username="admin")
```

#### 禁用所有活跃用户
```python
sb.disable_all_active_users(username="admin")
```

#### 激活所有禁用用户
```python
sb.activate_all_disabled_users(username="admin")
```

#### 重置管理员使用量
```python
admin = sb.reset_admin_usage(username="admin")
```

#### 获取管理员使用量
```python
usage = sb.get_admin_usage(username="admin")  # 返回字节
```

### 用户管理

#### 获取用户
```python
user = sb.get_client(username="user123")
```

#### 通过订阅令牌获取用户
```python
user = sb.get_client_by_subLink(token="subscription_token")
```

#### 添加用户
```python
user = sb.add_client(
    username="user123",
    inboundTag=["VLESS_INBOUND"],
    note="用户备注",
    enable="active",
    flow="xtls-rprx-vision",
    total_gb=10,
    expire_time=1735689600
)
```

#### 修改用户
```python
user = sb.edit_client(
    username="user123",
    inboundTag=["VLESS_INBOUND", "VMESS_INBOUND"],
    note="更新的备注",
    enable="active",
    flow="xtls-rprx-vision",
    total_gb=20,
    expire_time=0
)
```

#### 删除用户
```python
sb.delete_client(username="user123")
```

#### 获取用户列表
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

#### 重置用户数据使用量
```python
user = sb.reset_user_data_usage(username="user123")
```

#### 撤销用户订阅
```python
user = sb.revoke_user_subscription(username="user123")
```

#### 获取用户使用量
```python
usage = sb.get_user_usage(
    username="user123",
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59"
)
```

#### 激活下一个计划
```python
user = sb.active_next_plan(username="user123")
```

#### 设置所有者
```python
user = sb.set_owner(username="user123", admin_username="admin")
```

#### 重置所有用户数据使用量
```python
sb.reset_users_data_usage()
```

#### 获取用户使用量
```python
usage = sb.get_users_usage(
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59",
    admin=["admin1"]
)
```

#### 获取过期用户
```python
expired = sb.get_expired_users(
    expired_after="2024-01-01T00:00:00",
    expired_before="2024-01-31T23:59:59"
)
```

#### 删除过期用户
```python
deleted = sb.delete_expired_users(
    expired_after="2024-01-01T00:00:00",
    expired_before="2024-01-31T23:59:59"
)
```

### 节点管理

#### 获取节点设置
```python
settings = sb.get_node_settings()
```

#### 添加节点
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

#### 获取节点
```python
node = sb.get_node(node_id=1)
```

#### 获取节点列表
```python
nodes = sb.get_nodes()
```

#### 修改节点
```python
node = sb.modify_node(
    node_id=1,
    name="Updated Node",
    address="192.168.1.2",
    status="connected"
)
```

#### 删除节点
```python
sb.remove_node(node_id=1)
```

#### 重连节点
```python
sb.reconnect_node(node_id=1)
```

#### 获取节点使用量
```python
usage = sb.get_usage(
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59"
)
```

### 核心管理

#### 获取核心统计
```python
stats = sb.get_core_stats()
```

#### 重启核心
```python
sb.restart_core()
```

#### 获取核心配置
```python
config = sb.get_core_config()
```

#### 修改核心配置
```python
config = sb.modify_core_config({"key": "value"})
```

### 系统管理

#### 获取系统统计
```python
stats = sb.get_system_stats()
```

#### 获取入站
```python
inbounds = sb.get_inbounds()
```

#### 获取主机
```python
hosts = sb.get_hosts()
```

#### 修改主机
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

### 用户模板管理

#### 添加用户模板
```python
template = sb.add_user_template(
    name="Template 1",
    data_limit=10737418240,  # 10GB 字节
    expire_duration=2592000,  # 30 天秒
    username_prefix="user_",
    username_suffix="_suffix",
    inbounds={
        "vless": ["VLESS_INBOUND"],
        "vmess": ["VMESS_INBOUND"]
    }
)
```

#### 获取用户模板列表
```python
templates = sb.get_user_templates(offset=0, limit=10)
```

#### 获取用户模板
```python
template = sb.get_user_template(template_id=1)
```

#### 修改用户模板
```python
template = sb.modify_user_template(
    template_id=1,
    name="Updated Template",
    data_limit=21474836480  # 20GB
)
```

#### 删除用户模板
```python
sb.remove_user_template(template_id=1)
```

### 订阅管理

#### 获取用户订阅
```python
subscription = sb.user_subscription(
    token="subscription_token",
    user_agent="Clash"
)
```

#### 获取用户订阅信息
```python
info = sb.user_subscription_info(token="subscription_token")
```

#### 获取用户订阅使用量
```python
usage = sb.user_get_usage(
    token="subscription_token",
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59"
)
```

#### 通过客户端类型获取用户订阅
```python
subscription = sb.user_subscription_with_client_type(
    token="subscription_token",
    client_type="clash",  # sing-box, clash-meta, clash, outline, v2ray, v2ray-json
    user_agent="Clash"
)
```

## 错误处理

SDK 提供全面的错误处理：

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
    print("未找到用户")
except Unauthorized:
    print("未认证")
except Forbidden:
    print("访问被拒绝")
except ValidationError as e:
    print(f"验证错误: {e}")
```

## 订阅链接生成器

```python
from sarban.sub_gen import sub_generator

subscription_link = sub_generator(
    userToken="token",
    fullAddress="sub.example.com:2096",
    verify=True
)
```

## 许可证

MIT License

## 作者

liwyd

## 贡献

欢迎贡献！请随时提交 Pull Request。
