---
description:
---

# Agent Execution Workflow

Mỗi khi nhận một tác vụ mới, Agent bắt buộc phải thực hiện tuần tự qua 7 bước dưới đây. Tuyệt đối không bỏ qua bước Brainstorming trước khi lên kế hoạch.

## Bước 1: Nạp Learning (Khởi tạo & Nạp Ngữ Cảnh)

- **Hành động:** Đọc các file cần thiết (ví dụ: `tech-stack.md`, `folder-structure.md`) trong `.agents/learnings/`. Nếu muốn đọc hết phải hỏi.
- **Mục tiêu:** Nắm vững bối cảnh, ngôn ngữ lập trình, thư viện cho phép và các giới hạn hệ thống để định hình không gian làm việc.

## Bước 2: Brainstorming (Phân Tích & Mở Rộng)

- **Hành động:** **BẮT BUỘC** sử dụng Skill brainstorming có sẵn (nếu hệ thống có công cụ/skill này) để phân tích yêu cầu.

## Bước 3: Planning (Lên Kế Hoạch Chi Tiết)

- **Hành động:** Dựa trên kết quả từ Bước 2, khởi tạo một Bảng Tiến Độ (Markdown Task List) rõ ràng, có UI để mình theo dõi.
- **Định dạng bảng:**
  | Task | Mô tả công việc | Trạng thái |
  | :--- | :--- | :---: |
  | 1 | Phân tích và thiết kế API | [ ] |
  | 2 | Code module xử lý logic | [ ] |
  | 3 | ... | [ ] |
- **Yêu cầu:** Hiển thị kế hoạch này cho người dùng duyệt hoặc trực tiếp chuyển sang bước thực thi.

## Bước 4: Execute (Thực Thi)

- **Hành động:** Viết mã nguồn, tạo tài liệu hoặc cấu hình hệ thống theo đúng Bảng Kế Hoạch ở Bước 3, khi hoàn thành mỗi task hãy check vào Bảng Tiến Độ.
- **Yêu cầu:** Code phải có comment rõ ràng và không được chứa thông tin nhạy cảm (hard-code token, password).

## Bước 5: Test (Kiểm Thử)

- **Hành động:**
  - Tự rà soát lại mã nguồn để tìm các lỗi cú pháp hoặc logic (vòng lặp vô hạn, xử lý edge cases).
  - Viết script test hoặc mô phỏng luồng chạy (Mental Walkthrough).
- **Mục tiêu:** Đảm bảo mã nguồn hoạt động đúng với thiết kế ở Bước 3. Nếu có lỗi, lập tức chuyển sang Bước 6.

## Bước 6: Learning (Đúc Kết - Áp dụng khi có lỗi)

- **Hành động:** Nếu quá trình Test hoặc Execute gặp lỗi, Agent phải phân tích nguyên nhân gốc rễ (Root Cause) và ghi nhận lại bài học, và lưu lại trong `.agents/learnings/learned-errors.md`.
- **Định dạng bắt buộc (Ghi rõ ngày tháng):**
  > **Ngày: [DD/MM/YYYY], Giờ: [HH:mm]**
  >
  > - **Mô tả lỗi:** (Ghi ngắn gọn lỗi gặp phải, ví dụ: Thiếu quyền đọc file JSON).
  > - **Nguyên nhân:** (Tại sao xảy ra lỗi này?).
  > - **Cách khắc phục:** (Đã làm gì để vá lỗi?).
  > - **Bài học rút ra:** (Ghi chú để không lặp lại lỗi này ở các task sau).

## Bước 7: Tóm Tắt & Lưu Lại (Hoàn Tất Tác Vụ)

- **Hành động:** Tóm tắt ngắn gọn task đã hoàn hành và lưu lại trong `.agents/learnings/completed-tasks.md`.
- **Định dạng bắt buộc (Ghi rõ ngày tháng):**
  > **Ngày: [DD/MM/YYYY], Giờ: [HH:mm]**
  >
  > - **Tổng quan:** Hoàn thành module/task gì.
  > - **Deliverables (Sản phẩm giao nộp):** Danh sách các file đã tạo/chỉnh sửa.

## Bước 8: Cập nhật cấu trúc thư mục và tech stack

- - **Hành động:** Cập nhật lại cấu trúc thư mục `folder-structure.md`. Cập `tech-stack.md` nếu có thêm thư viện mới.
