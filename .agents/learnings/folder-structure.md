# Directory Structure

```text
.
├── .venv/                      # Môi trường ảo Python
├── .agents/
│   ├── learnings/              # Thư mục chứa các file rules và tài liệu IDE
│   │   ├── completed-tasks.md
│   │   ├── folder-structure.md
│   │   ├── learned-errors.md
│   │   └── tech-stack.md
│   └── rules/
│       └── code-style-guide.md
├── tests/                      # Thư mục chứa unit tests (pytest)
│   ├── __init__.py             # Biến tests/ thành Python package
│   ├── conftest.py             # Fixtures dùng chung (mock env vars, dữ liệu mẫu)
│   ├── test_gsheet_api.py      # Kiểm thử Google Sheets API
│   ├── test_hubpot_api.py      # Kiểm thử HubSpot API
│   ├── test_sheet_storage_service.py # Kiểm thử module lưu trữ sheet và bot
│   └── test_sync_service.py    # Kiểm thử logic đồng bộ và FindContact
├── core/                       # Module giao tiếp API bên ngoài
│   ├── __init__.py
│   ├── gsheet_api.py           # Đọc/ghi dữ liệu Google Sheets
│   └── hubspot_api.py          # Tìm kiếm và Create/Update Contact
├── services/                   # Module chứa logic nghiệp vụ
│   ├── __init__.py
│   ├── sheet_storage_service.py # Quản lý đọc/ghi local-data.csv và bot-account.txt
│   └── sync_service.py         # Điều phối luồng xử lý đồng bộ
├── storage/                   # Thư mục lưu trữ tài khoản bot và dữ liệu sheet cục bộ
│   ├── bot-account.txt         # Email tài khoản Google Service Account của Bot
│   └── local-data.csv          # Danh sách Google Sheets đã lưu (Tên, Link, ID, Thời gian truy cập)
├── .env                        # Chứa các biến môi trường (ẩn khỏi Git)
├── .gitignore                  # Bỏ qua file rác, cache, thư mục môi trường ảo và key
├── .flake8                     # Cấu hình chuẩn PEP 8
├── pytest.ini                  # Cấu hình pytest (testpaths, addopts)
├── requirements.txt            # Danh sách thư viện phụ thuộc
├── requirements-dev.txt        # Thư viện dev (black, flake8, pytest, pytest-mock)
├── README.md                   # Hướng dẫn cài đặt và chạy ứng dụng
├── sample_data.xlsx            # File Sheet mẫu
├── credentials.json            # Khóa Service Account của Google (ẩn khỏi Git)
├── config.py                   # Module nạp biến môi trường
└── main.py                     # Entry point (Giao diện Streamlit)
```
