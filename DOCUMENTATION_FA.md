# مستندات کامل SARBAN

SARBAN یک کتابخانه قدرتمند پایتون است که رابطی ساده و کاربردی برای مدیریت پنل Marzban شما فراهم می‌کند. چه بخواهید مدیریت کاربران را خودکار کنید، منابع سیستم را مانیتور کنید یا یکپارچه‌سازی‌های سفارشی بسازید، SARBAN کار با API مارزبان را آسان می‌کند.

## فهرست مطالب

1. [نصب](#نصب)
2. [شروع کار](#شروع-کار)
3. [احراز هویت](#احراز-هویت)
4. [مدیریت ادمین](#مدیریت-ادمین)
5. [مدیریت کاربر](#مدیریت-کاربر)
6. [مدیریت نود](#مدیریت-نود)
7. [مدیریت هسته](#مدیریت-هسته)
8. [مدیریت سیستم](#مدیریت-سیستم)
9. [قالب‌های کاربر](#قالب‌های-کاربر)
10. [اشتراک‌ها](#اشتراک‌ها)
11. [مدیریت خطا](#مدیریت-خطا)
12. [استفاده پیشرفته](#استفاده-پیشرفته)
13. [بهترین روش‌ها](#بهترین-روش‌ها)
14. [عیب‌یابی](#عیب‌یابی)

## نصب

SARBAN را با استفاده از pip نصب کنید:

```bash
pip install sarban
```

برای نسخه توسعه:

```bash
pip install git+https://github.com/liwyd/sarban.git
```

### نیازمندی‌ها

- پایتون 3.6 یا بالاتر
- کتابخانه requests (به صورت خودکار نصب می‌شود)

## شروع کار

### تنظیمات اولیه

ابتدا کلاس SARBAN را import کنید و یک نمونه ایجاد کنید:

```python
from sarban import SARBAN

# ایجاد یک نمونه SARBAN
sb = SARBAN(
    full_address="https://your-panel.com:2087",
    https=True
)
```

پارامتر `full_address` می‌تواند:
- یک URL کامل باشد: `"https://panel.example.com:2087"`
- فقط دامنه باشد: `"panel.example.com:2087"` (پروتکل به صورت خودکار اضافه می‌شود)

پارامتر `https` تعیین می‌کند که آیا از HTTPS استفاده شود یا خیر (پیش‌فرض: True).

### اولین درخواست شما

پس از ایجاد نمونه، باید احراز هویت کنید:

```python
try:
    sb.login("your_username", "your_password")
    print("ورود با موفقیت انجام شد!")
except Exception as e:
    print(f"ورود ناموفق: {e}")
```

پس از ورود، می‌توانید شروع به ارسال درخواست‌های API کنید. توکن احراز هویت به صورت خودکار ذخیره می‌شود و برای تمام درخواست‌های بعدی استفاده می‌شود.

## احراز هویت

### ورود

متد `login()` با پنل Marzban احراز هویت می‌کند و یک توکن دسترسی دریافت می‌کند:

```python
sb.login(username="admin", password="secure_password")
```

**نکات مهم:**
- قبل از ارسال هر درخواست API باید وارد شوید (به جز endpoint های اشتراک)
- توکن به صورت داخلی ذخیره می‌شود و به صورت خودکار استفاده می‌شود
- اگر قبلاً وارد شده‌اید، فراخوانی مجدد `login()` خطای `AlreadyLogin` ایجاد می‌کند

### بررسی وضعیت احراز هویت

در حالی که متد صریحی برای "بررسی احراز هویت" وجود ندارد، می‌توانید با ارسال یک درخواست API ساده احراز هویت خود را تأیید کنید:

```python
try:
    admin = sb.get_current_admin()
    print(f"احراز هویت شده به عنوان: {admin['username']}")
except Unauthorized:
    print("احراز هویت نشده")
```

## مدیریت ادمین

### دریافت ادمین فعلی

دریافت اطلاعات درباره ادمین فعلی که احراز هویت شده:

```python
admin = sb.get_current_admin()
print(f"نام کاربری: {admin['username']}")
print(f"سودو است: {admin['is_sudo']}")
print(f"آیدی تلگرام: {admin.get('telegram_id')}")
```

### ایجاد ادمین

ایجاد یک حساب ادمین جدید. فقط ادمین‌های سودو می‌توانند ادمین‌های دیگر ایجاد کنند:

```python
new_admin = sb.create_admin(
    username="new_admin",
    password="strong_password_123",
    is_sudo=False,
    telegram_id=123456789,
    discord_webhook="https://discord.com/api/webhooks/..."
)
```

**پارامترها:**
- `username` (الزامی): نام کاربری ادمین
- `password` (الزامی): رمز عبور ادمین
- `is_sudo` (اختیاری): آیا ادمین دسترسی سودو دارد (پیش‌فرض: False)
- `telegram_id` (اختیاری): آیدی تلگرام برای اعلان‌ها
- `discord_webhook` (اختیاری): URL وب‌هوک دیسکورد
- `users_usage` (اختیاری): محدودیت استفاده برای کاربران تحت این ادمین

### دریافت تمام ادمین‌ها

دریافت لیست تمام ادمین‌ها با فیلتر اختیاری:

```python
# دریافت تمام ادمین‌ها
all_admins = sb.get_admins()

# دریافت با صفحه‌بندی
admins = sb.get_admins(offset=0, limit=10)

# جستجو بر اساس نام کاربری
admin = sb.get_admins(username="specific_admin")
```

### ویرایش ادمین

به‌روزرسانی جزئیات یک ادمین موجود:

```python
updated = sb.modify_admin(
    username="admin",
    password="new_password",
    is_sudo=True,
    telegram_id=987654321
)
```

فقط باید فیلدهایی که می‌خواهید به‌روزرسانی کنید را ارائه دهید. فیلدهای حذف شده بدون تغییر باقی می‌مانند.

### حذف ادمین

حذف یک حساب ادمین:

```python
sb.remove_admin(username="admin_to_remove")
```

**هشدار:** این عمل قابل بازگشت نیست. مطمئن شوید حداقل یک ادمین سودو باقی مانده است.

### مدیریت کاربران ادمین

غیرفعال کردن تمام کاربران فعال تحت یک ادمین خاص:

```python
sb.disable_all_active_users(username="admin")
```

فعال کردن تمام کاربران غیرفعال:

```python
sb.activate_all_disabled_users(username="admin")
```

### استفاده ادمین

دریافت آمار استفاده برای یک ادمین:

```python
usage_bytes = sb.get_admin_usage(username="admin")
usage_gb = usage_bytes / (1024 ** 3)
print(f"استفاده ادمین: {usage_gb:.2f} GB")
```

بازنشانی استفاده ادمین:

```python
sb.reset_admin_usage(username="admin")
```

## مدیریت کاربر

### دریافت کاربر

دریافت یک کاربر با نام کاربری:

```python
user = sb.get_client(username="user123")
print(f"وضعیت: {user['status']}")
print(f"ترافیک استفاده شده: {user['used_traffic']} بایت")
print(f"محدودیت داده: {user.get('data_limit')}")
```

### دریافت کاربر با توکن اشتراک

اگر توکن اشتراک دارید، می‌توانید بدون احراز هویت اطلاعات کاربر را دریافت کنید:

```python
user = sb.get_client_by_subLink(token="subscription_token_here")
```

### افزودن کاربر

ایجاد یک حساب کاربری جدید:

```python
import time

new_user = sb.add_client(
    username="newuser",
    inboundTag=["VLESS_TCP", "VLESS_GRPC"],
    note="مشتری از وب‌سایت",
    enable="active",
    flow="xtls-rprx-vision",
    total_gb=50,
    expire_time=int(time.time()) + (30 * 24 * 60 * 60)  # 30 روز از الان
)
```

**توضیح پارامترها:**
- `username`: 3-32 کاراکتر، فقط حروف، اعداد و زیرخط
- `inboundTag`: لیست تگ‌های inbound که کاربر می‌تواند به آن‌ها دسترسی داشته باشد
- `note`: یادداشت اختیاری برای سوابق شما
- `enable`: وضعیت کاربر ("active" یا "on_hold")
- `flow`: تنظیم Flow برای VLESS (معمولاً "xtls-rprx-vision")
- `total_gb`: محدودیت داده به گیگابایت (0 = نامحدود)
- `expire_time`: تایم‌استمپ یونیکس برای انقضا (0 = هرگز منقضی نمی‌شود)

**پیکربندی پروکسی‌ها:**

برای انواع مختلف پروکسی، باید پروکسی‌ها را متفاوت پیکربندی کنید:

```python
# برای VMESS
user = sb.add_client(
    username="vmess_user",
    inboundTag=["VMESS_WS"],
    proxies={
        "vmess": {
            "id": "auto-generated-uuid"
        }
    }
)

# برای VLESS
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

### ویرایش کاربر

به‌روزرسانی یک کاربر موجود:

```python
updated = sb.edit_client(
    username="user123",
    inboundTag=["VLESS_TCP", "VMESS_WS"],
    note="یادداشت به‌روز شده",
    enable="active",
    total_gb=100,
    expire_time=0  # حذف انقضا
)
```

**مهم:** فقط پارامترهایی که می‌خواهید تغییر دهید را ارائه دهید. متد فقط فیلدهای مشخص شده را به‌روزرسانی می‌کند.

### حذف کاربر

حذف یک حساب کاربری:

```python
sb.delete_client(username="user123")
```

### دریافت لیست کاربران

دریافت چندین کاربر با فیلتر پیشرفته:

```python
# دریافت تمام کاربران (صفحه‌بندی شده)
users_response = sb.get_users(offset=0, limit=50)
print(f"کل کاربران: {users_response['total']}")
for user in users_response['users']:
    print(f"  - {user['username']}: {user['status']}")

# فیلتر بر اساس وضعیت
active_users = sb.get_users(status="active", limit=100)

# جستجو بر اساس نام کاربری
specific_users = sb.get_users(username=["user1", "user2", "user3"])

# جستجو بر اساس ادمین
admin_users = sb.get_users(admin=["admin1", "admin2"])

# جستجوی متنی
search_results = sb.get_users(search="keyword")

# مرتب‌سازی نتایج
sorted_users = sb.get_users(sort="created_at", limit=20)
```

### مدیریت استفاده کاربر

بازنشانی استفاده داده یک کاربر:

```python
sb.reset_user_data_usage(username="user123")
```

بازنشانی استفاده داده تمام کاربران:

```python
sb.reset_users_data_usage()
```

دریافت آمار استفاده برای یک کاربر:

```python
from datetime import datetime, timedelta

# دریافت استفاده برای 30 روز گذشته
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

usage = sb.get_user_usage(
    username="user123",
    start=start_date.isoformat(),
    end=end_date.isoformat()
)

for usage_entry in usage['usages']:
    print(f"نود: {usage_entry['node_name']}")
    print(f"استفاده شده: {usage_entry['used_traffic'] / (1024**3):.2f} GB")
```

دریافت استفاده برای تمام کاربران:

```python
usage = sb.get_users_usage(
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59",
    admin=["admin1"]  # اختیاری: فیلتر بر اساس ادمین
)
```

### مدیریت اشتراک

لغو اشتراک کاربر (تولید مجدد توکن):

```python
user = sb.revoke_user_subscription(username="user123")
print(f"URL اشتراک جدید: {user['subscription_url']}")
```

### مالکیت کاربر

تغییر مالک (ادمین) یک کاربر:

```python
sb.set_owner(username="user123", admin_username="new_admin")
```

### ویژگی پلان بعدی

فعال‌سازی پلان بعدی برای یک کاربر (در صورت پیکربندی):

```python
user = sb.active_next_plan(username="user123")
```

### کاربران منقضی شده

یافتن کاربرانی که در یک بازه زمانی منقضی شده‌اند:

```python
expired = sb.get_expired_users(
    expired_after="2024-01-01T00:00:00",
    expired_before="2024-01-31T23:59:59"
)
print(f"{len(expired)} کاربر منقضی شده یافت شد")
```

حذف کاربران منقضی شده:

```python
deleted = sb.delete_expired_users(
    expired_after="2024-01-01T00:00:00",
    expired_before="2024-01-31T23:59:59"
)
print(f"{len(deleted)} کاربر حذف شد")
```

## مدیریت نود

### دریافت تنظیمات نود

دریافت تنظیمات پیکربندی نود:

```python
settings = sb.get_node_settings()
print(f"حداقل نسخه نود: {settings['min_node_version']}")
print(f"گواهینامه: {settings['certificate'][:50]}...")
```

### افزودن نود

افزودن یک نود جدید به تنظیمات Marzban شما:

```python
node = sb.add_node(
    name="نود آمریکا 1",
    address="192.168.1.100",
    port=62050,
    api_port=62051,
    usage_coefficient=1.0,
    add_as_new_host=True
)
```

**پارامترها:**
- `name`: نام دوستانه برای نود
- `address`: آدرس IP یا hostname
- `port`: پورت ارتباطی نود (پیش‌فرض: 62050)
- `api_port`: پورت API (پیش‌فرض: 62051)
- `usage_coefficient`: ضریب برای ردیابی استفاده (پیش‌فرض: 1.0)
- `add_as_new_host`: آیا به عنوان هاست جدید اضافه شود (پیش‌فرض: True)

### دریافت نود

دریافت اطلاعات درباره یک نود خاص:

```python
node = sb.get_node(node_id=1)
print(f"نام: {node['name']}")
print(f"وضعیت: {node['status']}")
print(f"نسخه Xray: {node.get('xray_version')}")
```

### دریافت تمام نودها

لیست تمام نودها:

```python
nodes = sb.get_nodes()
for node in nodes:
    print(f"{node['id']}: {node['name']} - {node['status']}")
```

### ویرایش نود

به‌روزرسانی پیکربندی نود:

```python
updated = sb.modify_node(
    node_id=1,
    name="نام نود به‌روز شده",
    address="192.168.1.200",
    status="disabled"  # می‌تواند باشد: connected, connecting, error, disabled
)
```

### حذف نود

حذف یک نود:

```python
sb.remove_node(node_id=1)
```

### اتصال مجدد نود

اجبار یک نود به اتصال مجدد:

```python
sb.reconnect_node(node_id=1)
```

### آمار استفاده نود

دریافت آمار استفاده برای تمام نودها:

```python
usage = sb.get_usage(
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59"
)

for node_usage in usage['usages']:
    print(f"نود: {node_usage['node_name']}")
    print(f"  آپلینک: {node_usage['uplink'] / (1024**3):.2f} GB")
    print(f"  دانلینک: {node_usage['downlink'] / (1024**3):.2f} GB")
```

## مدیریت هسته

### دریافت آمار هسته

دریافت اطلاعات سیستم هسته:

```python
stats = sb.get_core_stats()
print(f"نسخه: {stats['version']}")
print(f"شروع شده: {stats['started']}")
print(f"WebSocket لاگ‌ها: {stats['logs_websocket']}")
```

### راه‌اندازی مجدد هسته

راه‌اندازی مجدد هسته Marzban و تمام نودهای متصل:

```python
sb.restart_core()
print("راه‌اندازی مجدد هسته آغاز شد")
```

**نکته:** این کار به طور موقت تمام کاربران را قطع می‌کند.

### دریافت پیکربندی هسته

دریافت پیکربندی فعلی هسته:

```python
config = sb.get_core_config()
# config یک دیکشنری با تنظیمات هسته است
```

### ویرایش پیکربندی هسته

به‌روزرسانی پیکربندی هسته (نیاز به سودو):

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

**هشدار:** پیکربندی نادرست می‌تواند نصب Marzban شما را خراب کند. همیشه قبل از تغییرات بکاپ بگیرید.

## مدیریت سیستم

### دریافت آمار سیستم

دریافت آمار جامع سیستم:

```python
stats = sb.get_system_stats()
print(f"نسخه: {stats['version']}")
print(f"حافظه: {stats['mem_used']}/{stats['mem_total']} MB")
print(f"استفاده CPU: {stats['cpu_usage']}%")
print(f"کل کاربران: {stats['total_user']}")
print(f"کاربران آنلاین: {stats['online_users']}")
print(f"کاربران فعال: {stats['users_active']}")
print(f"پهنای باند ورودی: {stats['incoming_bandwidth'] / (1024**3):.2f} GB")
print(f"پهنای باند خروجی: {stats['outgoing_bandwidth'] / (1024**3):.2f} GB")
```

### دریافت Inbound ها

دریافت تمام پیکربندی‌های inbound گروه‌بندی شده بر اساس پروتکل:

```python
inbounds = sb.get_inbounds()

for protocol, inbound_list in inbounds.items():
    print(f"\n{protocol.upper()}:")
    for inbound in inbound_list:
        print(f"  تگ: {inbound['tag']}")
        print(f"  شبکه: {inbound['network']}")
        print(f"  پورت: {inbound['port']}")
```

### دریافت Host ها

دریافت هاست‌های پروکسی گروه‌بندی شده بر اساس تگ inbound:

```python
hosts = sb.get_hosts()

for inbound_tag, host_list in hosts.items():
    print(f"\n{inbound_tag}:")
    for host in host_list:
        print(f"  یادداشت: {host['remark']}")
        print(f"  آدرس: {host['address']}")
        print(f"  پورت: {host.get('port')}")
```

### ویرایش Host ها

به‌روزرسانی پیکربندی‌های هاست پروکسی:

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

## قالب‌های کاربر

قالب‌های کاربر به شما امکان ایجاد پیکربندی‌های قابل استفاده مجدد برای کاربران را می‌دهند.

### افزودن قالب

ایجاد یک قالب کاربر جدید:

```python
template = sb.add_user_template(
    name="پلان پریمیوم",
    data_limit=107374182400,  # 100 GB به بایت
    expire_duration=2592000,  # 30 روز به ثانیه
    username_prefix="prem_",
    username_suffix="",
    inbounds={
        "vless": ["VLESS_TCP", "VLESS_GRPC"],
        "vmess": ["VMESS_WS"]
    }
)
```

### دریافت قالب‌ها

لیست تمام قالب‌ها:

```python
templates = sb.get_user_templates(offset=0, limit=10)
for template in templates:
    print(f"ID: {template['id']}, نام: {template.get('name')}")
```

### دریافت قالب

دریافت یک قالب خاص:

```python
template = sb.get_user_template(template_id=1)
```

### ویرایش قالب

به‌روزرسانی یک قالب:

```python
updated = sb.modify_user_template(
    template_id=1,
    name="پلان پریمیوم به‌روز شده",
    data_limit=214748364800  # 200 GB
)
```

### حذف قالب

حذف یک قالب:

```python
sb.remove_user_template(template_id=1)
```

## اشتراک‌ها

Endpoint های اشتراک به کاربران امکان دریافت لینک‌ها و اطلاعات اشتراک خود را می‌دهند.

### دریافت اشتراک

دریافت محتوای اشتراک بر اساس user agent:

```python
subscription = sb.user_subscription(
    token="user_subscription_token",
    user_agent="Clash"
)
# محتوای اشتراک را در فرمت مناسب برمی‌گرداند
```

### دریافت اطلاعات اشتراک

دریافت اطلاعات جزئی اشتراک:

```python
info = sb.user_subscription_info(token="user_subscription_token")
print(f"نام کاربری: {info['username']}")
print(f"وضعیت: {info['status']}")
print(f"ترافیک استفاده شده: {info['used_traffic'] / (1024**3):.2f} GB")
print(f"محدودیت داده: {info.get('data_limit')}")
```

### دریافت استفاده اشتراک

دریافت آمار استفاده برای اشتراک:

```python
usage = sb.user_get_usage(
    token="user_subscription_token",
    start="2024-01-01T00:00:00",
    end="2024-01-31T23:59:59"
)
```

### دریافت اشتراک بر اساس نوع کلاینت

دریافت اشتراک در یک فرمت خاص:

```python
# انواع کلاینت موجود:
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

## مدیریت خطا

SARBAN مدیریت خطای جامعی ارائه می‌دهد. همیشه فراخوانی‌های API را در بلوک‌های try-except بپیچید:

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
    print("کاربر یافت نشد")
except Unauthorized:
    print("لطفاً ابتدا وارد شوید")
    sb.login("admin", "password")
except Forbidden:
    print("شما اجازه این عمل را ندارید")
except ValidationError as e:
    print(f"ورودی نامعتبر: {e}")
except HTTPException as e:
    print(f"خطای HTTP {e.status_code}: {e}")
```

### سناریوهای خطای رایج

**401 Unauthorized:**
- توکن منقضی شده یا نامعتبر
- وارد نشده
- راه حل: دوباره `login()` را فراخوانی کنید

**403 Forbidden:**
- دسترسی ناکافی
- ادمین سودو نیست که سعی می‌کند به endpoint های فقط سودو دسترسی پیدا کند
- راه حل: از یک حساب ادمین سودو استفاده کنید

**404 Not Found:**
- منبع وجود ندارد
- نام کاربری نامعتبر، node_id و غیره
- راه حل: بررسی کنید که منبع وجود دارد

**409 Conflict:**
- منبع از قبل وجود دارد (مثلاً نام کاربری گرفته شده)
- راه حل: از شناسه دیگری استفاده کنید

**422 Validation Error:**
- پارامترهای ورودی نامعتبر
- راه حل: فرمت و نیازمندی‌های پارامتر را بررسی کنید

## استفاده پیشرفته

### عملیات دسته‌ای

پردازش چندین کاربر:

```python
usernames = ["user1", "user2", "user3"]
for username in usernames:
    try:
        sb.reset_user_data_usage(username)
        print(f"بازنشانی {username}")
    except Exception as e:
        print(f"شکست در بازنشانی {username}: {e}")
```

### اسکریپت مانیتورینگ

ایجاد یک اسکریپت مانیتورینگ:

```python
import time
from datetime import datetime

while True:
    try:
        stats = sb.get_system_stats()
        print(f"[{datetime.now()}] آنلاین: {stats['online_users']}/{stats['total_user']}")
        time.sleep(60)  # بررسی هر دقیقه
    except Exception as e:
        print(f"خطا: {e}")
        time.sleep(60)
```

### ایجاد کاربر با اعتبارسنجی

```python
def create_user_safe(username, inbound_tag, total_gb):
    try:
        # بررسی وجود کاربر
        existing = sb.get_client(username)
        print(f"کاربر {username} از قبل وجود دارد")
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
        print(f"کاربر ایجاد شد: {username}")
        return True
    except Conflict:
        print(f"کاربر {username} از قبل وجود دارد")
        return False
    except ValidationError as e:
        print(f"خطای اعتبارسنجی: {e}")
        return False
```

### تولیدکننده گزارش استفاده

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
            print(f"خطا در دریافت استفاده برای {user['username']}: {e}")
    
    return sorted(report, key=lambda x: x['usage_gb'], reverse=True)
```

## بهترین روش‌ها

1. **همیشه خطاها را مدیریت کنید:** فراخوانی‌های API را در بلوک‌های try-except بپیچید
2. **اتصالات را دوباره استفاده کنید:** یک نمونه SARBAN ایجاد کنید و دوباره استفاده کنید
3. **محدودیت نرخ:** درخواست‌های زیادی خیلی سریع ارسال نکنید
4. **اعتبارسنجی ورودی:** پارامترها را قبل از ارسال درخواست‌های API بررسی کنید
5. **استفاده از صفحه‌بندی:** هنگام دریافت لیست‌های بزرگ، از offset/limit استفاده کنید
6. **ثبت عملیات:** لاگ عملیات مهم را نگه دارید
7. **بکاپ قبل از تغییرات:** به خصوص برای تغییرات پیکربندی هسته
8. **تست در توسعه:** اسکریپت‌ها را قبل از اجرا در production تست کنید

## عیب‌یابی

### مشکلات اتصال

**مشکل:** نمی‌تواند به پنل متصل شود
```python
# بررسی کنید که آدرس درست است
sb = SARBAN(full_address="https://panel.example.com:2087", https=True)

# در صورت مشکل SSL با verify=False امتحان کنید
sb = SARBAN(full_address="https://panel.example.com:2087", https=False)
```

### مشکلات احراز هویت

**مشکل:** ورود ناموفق است
- نام کاربری و رمز عبور را بررسی کنید
- بررسی کنید که پنل در دسترس است
- مطمئن شوید که از حساب ادمین صحیح استفاده می‌کنید

### خطاهای مجوز

**مشکل:** خطاهای 403 Forbidden
- بررسی کنید که از حساب ادمین سودو استفاده می‌کنید
- مجوزهای ادمین را در پنل Marzban بررسی کنید

### مشکلات تایم‌اوت

**مشکل:** درخواست‌ها تایم‌اوت می‌شوند
- اتصال شبکه را بررسی کنید
- بررسی کنید که پنل در حال اجرا است
- در صورت نیاز timeout را در base.py افزایش دهید (پیش‌فرض: 30 ثانیه)

## تولیدکننده لینک اشتراک

به راحتی لینک‌های اشتراک ایجاد کنید:

```python
from sarban.sub_gen import sub_generator

link = sub_generator(
    userToken="user_token_here",
    fullAddress="sub.example.com:2096",
    verify=True
)
print(link)  # https://sub.example.com:2096/sub/user_token_here/
```

## پشتیبانی و مشارکت

برای مشکلات، درخواست‌های ویژگی یا مشارکت‌ها، لطفاً به مخزن GitHub مراجعه کنید.

## مجوز

MIT License - برای جزئیات فایل LICENSE را ببینید.

