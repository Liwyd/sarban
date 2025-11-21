# SARBAN

یک SDK کامل پایتون برای مدیریت پنل Marzban ([Gozargah/Marzban](https://github.com/Gozargah/Marzban)) از طریق REST API.

## ویژگی‌ها

- پوشش کامل تمام endpoint های Marzban
- مدیریت ادمین (ایجاد، ویرایش، حذف ادمین)
- مدیریت کاربر (عملیات CRUD، ردیابی استفاده)
- مدیریت نود (افزودن، ویرایش، حذف، اتصال مجدد نود)
- تنظیمات و آمار هسته
- آمار و نظارت سیستم
- مدیریت قالب کاربر
- مدیریت اشتراک
- مدیریت خطای جامع
- Type hints برای پشتیبانی بهتر IDE

## نصب

```bash
pip install sarban
```

## شروع سریع

```python
from sarban import SARBAN
from sarban.errors import BadLogin, Unauthorized

# راه‌اندازی کلاینت
sb = SARBAN(
    full_address="https://your-marzban-panel.com:2087",
    https=True
)

# ورود
try:
    sb.login("admin_username", "admin_password")
except BadLogin:
    print("اعتبارنامه نامعتبر است")
```

## مرجع API

### احراز هویت

#### ورود
```python
sb.login(username: str, password: str) -> bool
```

### مدیریت ادمین

#### دریافت ادمین فعلی
```python
admin = sb.get_current_admin()
```

#### ایجاد ادمین
```python
admin = sb.create_admin(
    username="new_admin",
    password="secure_password",
    is_sudo=False,
    telegram_id=123456789,
    discord_webhook="https://discord.com/webhook/..."
)
```

#### دریافت لیست ادمین‌ها
```python
admins = sb.get_admins(offset=0, limit=10, username="admin")
```

#### ویرایش ادمین
```python
admin = sb.modify_admin(
    username="admin",
    password="new_password",
    is_sudo=True
)
```

#### حذف ادمین
```python
sb.remove_admin(username="admin")
```

#### غیرفعال کردن تمام کاربران فعال
```python
sb.disable_all_active_users(username="admin")
```

#### فعال کردن تمام کاربران غیرفعال
```python
sb.activate_all_disabled_users(username="admin")
```

#### بازنشانی استفاده ادمین
```python
admin = sb.reset_admin_usage(username="admin")
```

#### دریافت استفاده ادمین
```python
usage = sb.get_admin_usage(username="admin")  # برمی‌گرداند بایت
```

### مدیریت کاربر

#### دریافت کاربر
```python
user = sb.get_client(username="user123")
```

#### دریافت کاربر با توکن اشتراک
```python
user = sb.get_client_by_subLink(token="subscription_token")
```

#### افزودن کاربر
```python
user = sb.add_client(
    username="user123",
    inboundTag=["VLESS_INBOUND"],
    note="یادداشت کاربر",
    enable="active",
    flow="xtls-rprx-vision",
    total_gb=10,
    expire_time=1735689600
)
```

#### ویرایش کاربر
```python
user = sb.edit_client(
    username="user123",
    inboundTag=["VLESS_INBOUND", "VMESS_INBOUND"],
    note="یادداشت به‌روز شده",
    enable="active",
    flow="xtls-rprx-vision",
    total_gb=20,
    expire_time=0
)
```

#### حذف کاربر
```python
sb.delete_client(username="user123")
```

#### دریافت لیست کاربران
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

#### بازنشانی استفاده داده کاربر
```python
user = sb.reset_user_data_usage(username="user123")
```

#### لغو اشتراک کاربر
```python
user = sb.revoke_user_subscription(username="user123")
```

#### دریافت استفاده کاربر
```python
usage = sb.get_user_usage(
    username="user123",
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59"
)
```

#### فعال‌سازی پلان بعدی
```python
user = sb.active_next_plan(username="user123")
```

#### تنظیم مالک
```python
user = sb.set_owner(username="user123", admin_username="admin")
```

#### بازنشانی استفاده داده تمام کاربران
```python
sb.reset_users_data_usage()
```

#### دریافت استفاده کاربران
```python
usage = sb.get_users_usage(
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59",
    admin=["admin1"]
)
```

#### دریافت کاربران منقضی شده
```python
expired = sb.get_expired_users(
    expired_after="2024-01-01T00:00:00",
    expired_before="2024-01-31T23:59:59"
)
```

#### حذف کاربران منقضی شده
```python
deleted = sb.delete_expired_users(
    expired_after="2024-01-01T00:00:00",
    expired_before="2024-01-31T23:59:59"
)
```

### مدیریت نود

#### دریافت تنظیمات نود
```python
settings = sb.get_node_settings()
```

#### افزودن نود
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

#### دریافت نود
```python
node = sb.get_node(node_id=1)
```

#### دریافت لیست نودها
```python
nodes = sb.get_nodes()
```

#### ویرایش نود
```python
node = sb.modify_node(
    node_id=1,
    name="Updated Node",
    address="192.168.1.2",
    status="connected"
)
```

#### حذف نود
```python
sb.remove_node(node_id=1)
```

#### اتصال مجدد نود
```python
sb.reconnect_node(node_id=1)
```

#### دریافت استفاده نودها
```python
usage = sb.get_usage(
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59"
)
```

### مدیریت هسته

#### دریافت آمار هسته
```python
stats = sb.get_core_stats()
```

#### راه‌اندازی مجدد هسته
```python
sb.restart_core()
```

#### دریافت تنظیمات هسته
```python
config = sb.get_core_config()
```

#### ویرایش تنظیمات هسته
```python
config = sb.modify_core_config({"key": "value"})
```

### مدیریت سیستم

#### دریافت آمار سیستم
```python
stats = sb.get_system_stats()
```

#### دریافت Inbound ها
```python
inbounds = sb.get_inbounds()
```

#### دریافت Host ها
```python
hosts = sb.get_hosts()
```

#### ویرایش Host ها
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

### مدیریت قالب کاربر

#### افزودن قالب کاربر
```python
template = sb.add_user_template(
    name="Template 1",
    data_limit=10737418240,  # 10GB به بایت
    expire_duration=2592000,  # 30 روز به ثانیه
    username_prefix="user_",
    username_suffix="_suffix",
    inbounds={
        "vless": ["VLESS_INBOUND"],
        "vmess": ["VMESS_INBOUND"]
    }
)
```

#### دریافت لیست قالب‌های کاربر
```python
templates = sb.get_user_templates(offset=0, limit=10)
```

#### دریافت قالب کاربر
```python
template = sb.get_user_template(template_id=1)
```

#### ویرایش قالب کاربر
```python
template = sb.modify_user_template(
    template_id=1,
    name="Updated Template",
    data_limit=21474836480  # 20GB
)
```

#### حذف قالب کاربر
```python
sb.remove_user_template(template_id=1)
```

### مدیریت اشتراک

#### دریافت اشتراک کاربر
```python
subscription = sb.user_subscription(
    token="subscription_token",
    user_agent="Clash"
)
```

#### دریافت اطلاعات اشتراک کاربر
```python
info = sb.user_subscription_info(token="subscription_token")
```

#### دریافت استفاده اشتراک کاربر
```python
usage = sb.user_get_usage(
    token="subscription_token",
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59"
)
```

#### دریافت اشتراک کاربر با نوع کلاینت
```python
subscription = sb.user_subscription_with_client_type(
    token="subscription_token",
    client_type="clash",  # sing-box, clash-meta, clash, outline, v2ray, v2ray-json
    user_agent="Clash"
)
```

## مدیریت خطا

SDK مدیریت خطای جامعی ارائه می‌دهد:

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
    print("کاربر یافت نشد")
except Unauthorized:
    print("احراز هویت نشده")
except Forbidden:
    print("دسترسی رد شد")
except ValidationError as e:
    print(f"خطای اعتبارسنجی: {e}")
```

## تولیدکننده لینک اشتراک

```python
from sarban.sub_gen import sub_generator

subscription_link = sub_generator(
    userToken="token",
    fullAddress="sub.example.com:2096",
    verify=True
)
```

## مجوز

MIT License

## نویسنده

liwyd

## مشارکت

مشارکت‌ها خوش‌آمد هستند! لطفاً Pull Request ارسال کنید.
