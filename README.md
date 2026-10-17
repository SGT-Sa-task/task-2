# HubSpot Contact Sync — Bài 2

Ứng dụng Streamlit đọc dữ liệu contact từ Google Sheets rồi đồng bộ lên HubSpot (Create/Update).

---

## Yêu cầu hệ thống

- Python 3.10+
- Tài khoản Google Cloud với Service Account đã bật Google Sheets API
- HubSpot Private App token

---

## Cài đặt

```bash
# 1. Tạo và kích hoạt môi trường ảo
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 2. Cài runtime dependencies
pip install -r requirements.txt

# 3. (Tuỳ chọn) Cài dev dependencies
pip install -r requirements-dev.txt
```

---

## Cấu hình

### 1. Biến môi trường — `.env`

Tạo file `.env` tại root dự án (không commit lên Git):

```dotenv
HUBSPOT_API_KEY=your_private_app_token_here
GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit
```

### 2. Google Service Account — `credentials.json`

- Tải file JSON key của Service Account từ Google Cloud Console.
- Đặt tại root dự án với tên `credentials.json` (không commit lên Git).
- Chia sẻ Google Sheet với email Service Account (quyền **Viewer** là đủ để đọc).

---

## Chạy ứng dụng

```bash
streamlit run main.py
```

---

## Cấu trúc thư mục

```
bai2_import_hubspot/
├── .env                  # Biến môi trường (ẩn khỏi Git)
├── credentials.json      # Khóa Service Account (ẩn khỏi Git)
├── config.py             # Nạp biến môi trường
├── main.py               # Entry point — giao diện Streamlit
├── core/
│   ├── gsheet_api.py     # Đọc dữ liệu từ Google Sheets
│   └── hubspot_api.py    # Tìm kiếm và Create/Update Contact HubSpot
└── services/
    └── sync_service.py   # Điều phối luồng đồng bộ
```
