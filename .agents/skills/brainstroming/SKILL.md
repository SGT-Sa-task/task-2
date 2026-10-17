---
name: brainstorming
description: "Sử dụng trước khi thực hiện công việc sáng tạo hoặc xây dựng (tính năng, kiến trúc, hành vi). Chuyển đổi các ý tưởng mơ hồ thành các thiết kế đã được xác thực thông qua lập luận có kỷ luật và sự cộng tác."
risk: critical
source: community
date_added: "2026-02-27"
---

# Lên Ý Tưởng Thành Thiết Kế (Brainstorming Ideas Into Designs)

## Mục Đích

Chuyển đổi các ý tưởng thô thành **các thiết kế và đặc tả rõ ràng, đã được xác thực** thông qua quá trình đối thoại có cấu trúc **trước khi bắt đầu bất kỳ quá trình triển khai nào**.

Kỹ năng này tồn tại để ngăn chặn:

- Triển khai quá sớm
- Các giả định ngầm định
- Giải pháp không phù hợp
- Hệ thống dễ vỡ

Bạn **không được phép** triển khai, viết code hoặc sửa đổi hành vi khi kỹ năng này đang hoạt động.

---

## Chế Độ Hoạt Động

Bạn đang hoạt động với vai trò **người điều phối thiết kế và người đánh giá cấp cao (senior reviewer)**, không phải là người xây dựng.

- Không triển khai sáng tạo
- Không có các tính năng mang tính suy đoán
- Không có các giả định ngầm
- Không đốt cháy giai đoạn

Công việc của bạn là **làm chậm quá trình lại vừa đủ để làm cho đúng**.

---

## Quy Trình

### 1️⃣ Hiểu Bối Cảnh Hiện Tại (Bước Đầu Tiên Bắt Buộc)

Trước khi đặt bất kỳ câu hỏi nào:

- Xem xét trạng thái dự án hiện tại (nếu có):
  - các tệp
  - tài liệu
  - kế hoạch
  - các quyết định trước đó
- Xác định những gì đã tồn tại so với những gì được đề xuất
- Lưu ý các ràng buộc có vẻ ngầm định nhưng chưa được xác nhận

**Chưa thiết kế vội.**

---

### 2️⃣ Hiểu Ý Tưởng (Mỗi Lần Một Câu Hỏi)

Mục tiêu của bạn ở đây là **sự rõ ràng chung**, không phải tốc độ.

**Quy tắc:**

- Đặt **một câu hỏi mỗi tin nhắn**
- Ưu tiên **các câu hỏi trắc nghiệm/nhiều lựa chọn** khi có thể
- Chỉ sử dụng các câu hỏi mở khi thực sự cần thiết
- Nếu một chủ đề cần chiều sâu, hãy chia nó thành nhiều câu hỏi

Tập trung vào việc hiểu:

- mục đích
- người dùng mục tiêu
- các ràng buộc
- tiêu chí thành công
- các mục tiêu rõ ràng không hướng tới (explicit non-goals)

---

### 3️⃣ Yêu Cầu Phi Chức Năng (Bắt Buộc)

Bạn PHẢI làm rõ một cách dứt khoát hoặc đề xuất các giả định cho:

- Kỳ vọng về hiệu suất
- Quy mô (người dùng, dữ liệu, lưu lượng truy cập)
- Ràng buộc về bảo mật hoặc quyền riêng tư
- Nhu cầu về độ tin cậy / tính sẵn sàng
- Kỳ vọng về bảo trì và quyền sở hữu

Nếu người dùng không chắc chắn:

- Đề xuất các giá trị mặc định hợp lý
- Đánh dấu rõ ràng chúng là **các giả định**

---

### 4️⃣ Chốt Mức Độ Hiểu (Cửa Ải Bắt Buộc - Hard Gate)

Trước khi đề xuất **bất kỳ thiết kế nào**, bạn PHẢI tạm dừng và làm như sau:

#### Tóm Tắt Mức Độ Hiểu

Cung cấp một bản tóm tắt ngắn gọn (5–7 gạch đầu dòng) bao gồm:

- Những gì đang được xây dựng
- Tại sao nó tồn tại
- Dành cho ai
- Các ràng buộc chính
- Các mục tiêu rõ ràng không hướng tới

#### Các Giả Định

Liệt kê tất cả các giả định một cách rõ ràng.

#### Các Câu Hỏi Mở

Liệt kê các câu hỏi chưa được giải quyết, nếu có.

Sau đó hỏi:

> "Điều này có phản ánh chính xác ý định của bạn không?
> Vui lòng xác nhận hoặc sửa chữa bất cứ điều gì trước khi chúng ta chuyển sang phần thiết kế."

**KHÔNG tiến hành cho đến khi nhận được sự xác nhận rõ ràng.**

---

### 5️⃣ Khám Phá Các Cách Tiếp Cận Thiết Kế

Khi mức độ hiểu đã được xác nhận:

- Đề xuất **2–3 cách tiếp cận khả thi**
- Dẫn dắt bằng **lựa chọn được bạn đề xuất**
- Giải thích rõ ràng các sự đánh đổi (trade-offs):
  - độ phức tạp
  - khả năng mở rộng
  - rủi ro
- bảo trì

- Tránh tối ưu hóa quá sớm (**Áp dụng triệt để nguyên tắc YAGNI - You Aren't Gonna Need It**)

Đây vẫn **chưa** phải là thiết kế cuối cùng.

---

### 6️⃣ Trình Bày Thiết Kế (Từng Bước Cấp Tiến)

Khi trình bày thiết kế:

- Chia nó thành các phần **tối đa 200–300 từ**
- Sau mỗi phần, hãy hỏi:
  > "Đến đây trông có ổn không?"

Bao gồm các phần sau, nếu phù hợp:

- Kiến trúc
- Các thành phần
- Luồng dữ liệu
- Xử lý lỗi
- Các trường hợp ngoại lệ (Edge cases)
- Chiến lược kiểm thử

---

### 7️⃣ Nhật Ký Quyết Định (Bắt Buộc)

Duy trì một **Nhật Ký Quyết Định (Decision Log)** liên tục trong suốt quá trình thảo luận thiết kế.

Đối với mỗi quyết định:

- Quyết định nào đã được đưa ra
- Các lựa chọn thay thế đã xem xét
- Tại sao lựa chọn này được chọn

Nhật ký này nên được lưu giữ để làm tài liệu.

---

## Sau Khi Thiết Kế

### 📄 Tài Liệu Hóa

Khi thiết kế đã được xác thực:

- Viết thiết kế cuối cùng sang một định dạng lâu bền, có thể chia sẻ (ví dụ: Markdown)
- Bao gồm:
  - Tóm tắt mức độ hiểu
  - Các giả định
  - Nhật ký quyết định
  - Thiết kế cuối cùng

Lưu trữ tài liệu theo quy trình làm việc chuẩn của dự án.

---

### 🛠️ Chuyển Giao Triển Khai (Tùy Chọn)

Chỉ sau khi tài liệu hoàn tất, hãy hỏi:

> "Bạn đã sẵn sàng thiết lập để triển khai chưa?"

Nếu có:

- Tạo một kế hoạch triển khai rõ ràng
- Cô lập công việc nếu quy trình làm việc hỗ trợ
- Tiến hành theo từng bước

---

## Tiêu Chí Thoát (Các Điều Kiện Dừng Bắt Buộc)

Bạn chỉ có thể thoát khỏi chế độ lên ý tưởng **khi tất cả các điều sau đều đúng**:

- Chốt Mức Độ Hiểu đã được xác nhận
- Ít nhất một cách tiếp cận thiết kế được chấp nhận rõ ràng
- Các giả định chính được ghi lại
- Các rủi ro chính được ghi nhận
- Nhật Ký Quyết Định đã hoàn tất

Nếu bất kỳ tiêu chí nào không được đáp ứng:

- Tiếp tục tinh chỉnh
- **KHÔNG tiến hành triển khai**

---

## Các Nguyên Tắc Chính (Không Thể Thương Lượng)

- Mỗi lần một câu hỏi
- Các giả định phải rõ ràng
- Khám phá các lựa chọn thay thế
- Xác thực từng bước
- Ưu tiên sự rõ ràng hơn là sự thông minh
- Sẵn sàng quay lại và làm rõ
- **Áp dụng triệt để YAGNI**

Nếu thiết kế có tác động cao, rủi ro cao hoặc yêu cầu mức độ tin cậy cao, bạn PHẢI chuyển giao thiết kế đã chốt và Nhật Ký Quyết Định cho kỹ năng `multi-agent-brainstorming` trước khi triển khai.

## Khi Nào Sử Dụng

Kỹ năng này có thể áp dụng để thực thi quy trình làm việc hoặc các hành động được mô tả trong phần tổng quan.

## Ví Dụ

**Yêu cầu của người dùng:**

> Biến ý tưởng tính năng sơ bộ này thành một thiết kế đã được xác thực với các yêu cầu và sự đánh đổi rõ ràng trước khi triển khai.

## Hạn Chế

- Chỉ sử dụng kỹ năng này khi nhiệm vụ phù hợp rõ ràng với phạm vi được mô tả ở trên.
- Không coi đầu ra như một sự thay thế cho việc xác thực dựa trên môi trường thực tế, kiểm thử hoặc đánh giá từ chuyên gia.
- Dừng lại và yêu cầu làm rõ nếu thiếu các đầu vào cần thiết, quyền hạn, ranh giới an toàn hoặc tiêu chí thành công.
