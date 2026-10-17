---
name: task-retrospective
description: "Kích hoạt để trích xuất bài học và lưu vào bộ nhớ dự án khi một tác vụ đã hoàn thành nhưng Agent bỏ quên Giai đoạn 4 (Learning) trong SOP."
risk: low
source: user
date_added: "2026-10-05"
---

# Truy xuất Bài học & Đúc kết (Task Retrospective)

## Mục Đích

Đóng vai trò như một lưới an toàn (safety net) đảm bảo không có kiến thức hay sai lầm nào bị lãng quên nếu Agent vô tình bỏ qua bước Đúc kết (Learning) sau khi hoàn thành công việc. Kỹ năng này ép Agent quét lại toàn bộ quá trình gỡ lỗi và các quyết định kiến trúc của tác vụ vừa thực hiện để tổng hợp thành bài học lưu trữ dài hạn.

## Điều Kiện Kích Hoạt

Sử dụng kỹ năng này khi tác vụ đã hoàn thành (mã nguồn đã chạy, Unit Test đã pass, hoặc cấu hình hoàn tất) nhưng chưa có dữ liệu nào được ghi nhận vào `.agents/learning/lessons_learned.md`.

## Quy Trình Thực Thi Bắt Buộc

### 1. Quét Lịch Sử Tác Vụ (Context Scan)

Agent rà soát lại toàn bộ chuỗi hội thoại từ lúc Lên kế hoạch (Planning) đến lúc Thực thi (Execution & Testing), đặc biệt chú ý đến:

- Các lỗi phát sinh trong quá trình chạy (ví dụ: Playwright bị timeout khi quét fanpage, cấu hình Supabase Upsert bị lỗi duplicate key).
- Các thay đổi mã nguồn so với kế hoạch ban đầu (ví dụ: điều chỉnh Regex bóc tách thời gian do định dạng bài viết TDTU không chuẩn).
- Các Test Case bị fail ở lần chạy đầu tiên.

### 2. Phân Tích Nguyên Nhân Gốc Rễ (Root Cause Analysis)

Đối với mỗi vấn đề hoặc sự điều chỉnh phát hiện được, Agent phải làm rõ:

- Nguyên nhân kỹ thuật sâu xa (bản chất vấn đề, không phải hiện tượng).
- Giải pháp chính xác đã được áp dụng để hệ thống hoạt động ổn định trở lại.

### 3. Trích Xuất & Lưu Trữ (Extraction & Formating)

Định dạng thông tin thu thập được thành các gạch đầu dòng chuẩn xác. Agent tự động chuẩn bị nội dung để ghi nối (append) vào tệp `.agents/learning/lessons_learned.md`.

**Định dạng chuẩn:**
`- [YYYY-MM-DD] - [Tên Tác Vụ/Module] - [Vấn đề/Lỗi gặp phải] -> [Giải pháp/Bài học rút ra]`

## Tiêu Chí Hoàn Thành (DoD)

Kỹ năng này chỉ kết thúc khi xuất ra màn hình danh sách bài học đúng định dạng chuẩn và yêu cầu xác nhận để lưu vào hệ thống tệp.

## Ví Dụ

- [2026-10-05] - Cấu hình GitHub Actions Cronjob - Lỗi script Playwright treo vô thời hạn làm cạn quota 2000 phút -> Cần thiết lập `timeout: 10000` (10s) cho mọi lệnh `page.wait_for_selector()`.
- [2026-10-05] - Cấu hình Tauri Push Notification - Nhiều client đồng loạt gọi Supabase ngay khi có event báo bài viết mới gây quá tải CSDL -> Áp dụng hàm tính độ trễ ngẫu nhiên Jitter (100ms - 2000ms) trước khi client pull dữ liệu delta.
