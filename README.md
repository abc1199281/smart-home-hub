# Smart Home Hub

統一控制不同品牌智慧家電的 Python library。

## 支援設備

| 設備 | 協定 | 狀態 |
|------|------|------|
| Tapo P100 智慧插座 | LAN (PyP100) | 實機測試中 |
| ProBreeze 除濕機 | Midea/Tuya | 規劃中 |
| LG 洗脫烘 | ThinQ Cloud API | 規劃中 |
| SwitchBot Bot | BLE | 規劃中 |

## 安裝

```bash
uv sync
```

## 設定

複製範例設定檔，填入你的設備資訊：

```bash
cp config.sample.yaml config.yaml
```

編輯 `config.yaml`：

```yaml
devices:
  - name: living_room_plug
    type: tapo
    host: 192.168.1.100          # Tapo 插座的 LAN IP
    email: your_tapo_email@example.com   # Tapo app 登入帳號
    password: your_tapo_password         # Tapo app 登入密碼
```

## 使用方式

```bash
# 開啟設備
uv run python -m smart_home_hub tapo on

# 關閉設備
uv run python -m smart_home_hub tapo off

# 查詢設備狀態
uv run python -m smart_home_hub tapo status
```

也可以用設備名稱來指定：

```bash
uv run python -m smart_home_hub living_room_plug status
```

## 測試

```bash
uv run pytest tests/ -v
```

## 專案結構

```
smart_home_hub/
├── __init__.py
├── __main__.py            # CLI 進入點
└── devices/
    ├── __init__.py
    ├── base.py            # Device 抽象基底類別 (on, off, status)
    └── tapo.py            # Tapo P100 實作
config.sample.yaml         # 設定檔範例（納入版控）
config.yaml                # 實際設定檔（已 gitignore）
tests/
└── test_tapo.py           # 單元測試
```

## 新增設備

1. 在 `smart_home_hub/devices/` 建立新模組，繼承 `Device`
2. 實作 `on()`、`off()`、`status()` 三個方法
3. 在 `__main__.py` 的 `DEVICE_TYPES` 註冊新的 type
4. 在 `config.yaml` 加入設備設定
