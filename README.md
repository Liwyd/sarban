# SAR-BAN

An application with python that allows you to modify your marzban panel ([Gozargah/Marzban](https://github.com/Gozargah/Marzban))

- Special thanks to ([meta-syfu](https://github.com/meta-syfu))

## How To Install

```
pip install sarban
```

## How To Use

- Import sarban in your .py file

```python
from sarban import SARBAN


sb = SARBAN(
    full_address="https://liwyd.site:2087",
    https=True
)
```

- Login in your panel

```python
from sarban.errors import BadLogin

try:
  sb.login(USERNAME, PASSWORD)
except BadLogin:
  ...
```

- Get users list

```python
users = sb.get_users()

# a part of Result
{
  "proxies": {
    "vless": {
      "id": "4f5b7542-72b4-4d14-8dd6-7dea537c64a1",
      "flow": ""
    }
  },
  "expire": null,
  "data_limit": null,
  "data_limit_reset_strategy": "no_reset",
  "inbounds": {
    "vless": [
      "England",
    ]
  },
  "note": "sarban",
  "sub_updated_at": null,
  "sub_last_user_agent": null,
  "online_at": null,
  "on_hold_expire_duration": null,
  "on_hold_timeout": "2023-11-03T20:30:00",
  "auto_delete_in_days": null,
  "username": "sarban",
  "status": "active",
  "used_traffic": 0,
  "lifetime_used_traffic": 0,
  "created_at": "2024-08-11T13:29:15",
  "links": [
    "vless://..."
  ],
  "subscription_url": "https://sub.liwyd.com:2096/sus/...",
  "excluded_inbounds": {
    "vless": [
      "Spain",
      "Germany",
      "Netherlands",
      "France",
      "Finland",
    ]
  },
  "admin": {
    "username": "liwyd",
    "is_sudo": true,
    "telegram_id": 1451599691,
    "discord_webhook": null
  }
}
```

- Add client

```python
result = sb.add_client(
    username = "sarban",
    inboundTag = ["England"],
    note= "",
    enable= "active",
    flow= "",
    total_gb= 5, #GB
    expire_time= 1725522433, #UTC timestamp
)
```

- Edit the existing client

```python
result = sb.edit_client(
    username = "sarban",
    inboundTag = ["England"],
    note= "",
    enable= "active",
    flow= "",
    total_gb= 15, #GB
    expire_time= 0, #UTC timestamp
)
```

- Get client's information:

```python
# get client by username
client = sb.get_client(
    username="sarban",
)

# get client by subscription token
client = sb.get_client_by_subLink(
    token="dGVzdGluZ0hvbGRlcjUsMTcyMzU0NTk1MgSZOThncjMi",
)


# Result
{
  "proxies": {
    "vless": {
      "id": "4f7991aa-8813-4074-ae66-1c681a8a49aa",
      "flow": "xtls-rprx-vision"
    }
  },
  "expire": null,
  "data_limit": 5465454564,
  "data_limit_reset_strategy": "no_reset",
  "sub_updated_at": "2024-08-13T10:46:04",
  "online_at": null,
  "username": "sarban",
  "status": "active",
  "used_traffic": 0,
  "lifetime_used_traffic": 0,
  "created_at": "2024-08-11T14:10:43",
  "links": [
    "vless://.."
  ],
  "subscription_url": "https://sub.liwyd.com:2096/sus/..."
}
```

- Delete existing client:

```python
get_client = sb.delete_client(
    username="sarban",
)
```

# Create subscription-link string

- Import sub_generator

```python
from sarban.sub_gen import sub_generator
```

- TEST:

```python

generated_sub = sub_generator()

#result:

'
https://sub.liwyd.com:2096/sus/dGVzdGluZ0hvbGRlcjUsMTcyMzU0NTk1MgSZOThncjMi
'
```
