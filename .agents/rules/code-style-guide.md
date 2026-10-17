---
trigger: model_decision
description: This rule dictates how the agent should write, format, and execute Python code in this workspace.
---

# Project Rules: HubSpot Sync App

**Tech Stack File Path:** `.agents/learnings/tech-stack.md`
**Directory Structure File Path:** `.agents/learnings/folder-structure.md`

## 1. Ngôn ngữ & Khung làm việc

- Sử dụng Python 3.x làm ngôn ngữ chính.
- Phát triển giao diện người dùng bằng thư viện Streamlit.
- Quản lý các gói phụ thuộc (dependencies) bằng `pip` thông qua file `requirements.txt` và `requirements-dev.txt`. Sử dụng đúng phiên bản thư việ.

## 2. Code Formatting & Linter

- **KHÔNG ĐƯỢC CHẠY SCRIPT KIỂM TRA FORMAT GÂY TỐN TOKEN, MÌNH TỰ KI**
- Tuân thủ tiêu chuẩn PEP 8 cho toàn bộ mã nguồn Python.
- Sử dụng formatter `Black` với cấu hình giới hạn độ dài dòng (line-length) là 88 ký tự.
- Sử dụng linter `Flake8`. Cấu hình bỏ qua các lỗi `E203` và `W503` để tránh xung đột với Black.
- Bắt buộc bật tính năng Format on Save trên IDE thông qua Language Server Protocol.
- Viết docstring bằng tiếng Anh.

## 3. Quy ước Đặt tên (Naming Conventions)

- Tên biến và hàm: Sử dụng `snake_case`.
- Tên lớp (Class): Sử dụng `PascalCase`.
- Hằng số: Sử dụng `UPPER_SNAKE_CASE`.

## 4. Quản lý Bảo mật

- Tuyệt đối không hard-code thông tin nhạy cảm (API keys, tokens, mật khẩu) trong mã nguồn.
- Các file chứa thông tin xác thực như `.env` và `credentials.json` phải được liệt kê vào `.gitignore`.
