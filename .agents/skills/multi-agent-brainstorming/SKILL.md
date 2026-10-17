---
name: multi-agent-brainstorming
description: "Mô phỏng quy trình đánh giá chéo có cấu trúc bằng cách sử dụng nhiều tác nhân chuyên biệt để xác thực thiết kế, làm rõ các giả định ngầm và xác định các điểm có thể gây lỗi trước khi triển khai."
risk: none
source: community
date_added: "2026-02-27"
---

# Lên Ý Tưởng Đa Tác Nhân (Đánh Giá Thiết Kế Có Cấu Trúc)

## Mục Đích

Chuyển đổi một thiết kế do một tác nhân (single-agent) tạo ra thành một **thiết kế mạnh mẽ, đã qua thẩm định** bằng cách mô phỏng quy trình đánh giá chéo (peer-review) chính thức sử dụng nhiều tác nhân bị giới hạn phạm vi.

Kỹ năng này tồn tại để:

- làm rõ các giả định ngầm định
- xác định sớm các trường hợp có thể gây lỗi (failure modes)
- xác thực các ràng buộc phi chức năng
- kiểm thử khả năng chịu đựng (stress-test) của các thiết kế trước khi triển khai
- ngăn chặn sự hỗn loạn khi có quá nhiều ý tưởng

Đây **không phải là quá trình lên ý tưởng song song**.
Đó là **quá trình đánh giá thiết kế tuần tự với các vai trò được phân công bắt buộc**.

---

## Mô Hình Hoạt Động

- Một tác nhân thiết kế.
- Các tác nhân khác đánh giá.
- Không tác nhân nào được vượt quá quyền hạn của mình.
- Sự sáng tạo được tập trung; sự phản biện được phân bổ.
- Các quyết định phải rõ ràng và được ghi lại.

Quy trình này **có các cửa ải (gated)** và **sẽ tự động kết thúc theo thiết kế**.

---

## Vai Trò Của Các Tác Nhân (Không Thể Thương Lượng)

Mỗi tác nhân hoạt động dưới một **giới hạn phạm vi nghiêm ngặt**.

### 1️⃣ Nhà Thiết Kế Chính (Tác Nhân Dẫn Dắt - Lead Agent)

**Vai trò:**

- Làm chủ thiết kế
- Chạy kỹ năng `brainstorming` tiêu chuẩn
- Duy trì Nhật Ký Quyết Định (Decision Log)

**Được phép:**

- Đặt câu hỏi làm rõ
- Đề xuất thiết kế và các phương án thay thế
- Chỉnh sửa thiết kế dựa trên phản hồi

**KHÔNG được phép:**

- Tự phê duyệt thiết kế cuối cùng
- Bỏ qua các ý kiến phản đối của người đánh giá
- Tự bịa ra các yêu cầu sau khi đã chốt (post-lock)

---

### 2️⃣ Tác Nhân Hoài Nghi / Thách Thức (Skeptic / Challenger)

**Vai trò:**

- Giả định rằng thiết kế sẽ thất bại
- Nhận diện các điểm yếu và rủi ro

**Được phép:**

- Đặt câu hỏi về các giả định
- Xác định các trường hợp ngoại lệ (edge cases)
- Làm nổi bật sự mơ hồ hoặc sự tự tin thái quá
- Cảnh báo các vi phạm nguyên tắc YAGNI (You Aren't Gonna Need It)

**KHÔNG được phép:**

- Đề xuất các tính năng mới
- Thiết kế lại hệ thống
- Đưa ra các kiến trúc thay thế

_Hướng dẫn Prompt:_

> "Giả sử thiết kế này thất bại trên môi trường thực tế (production). Tại sao?"

---

### 3️⃣ Tác Nhân Bảo Vệ Ràng Buộc (Constraint Guardian)

**Vai trò:**

- Thực thi các ràng buộc phi chức năng và ràng buộc thực tế

_Các lĩnh vực trọng tâm:_

- hiệu suất
- khả năng mở rộng
- độ tin cậy
- bảo mật & quyền riêng tư
- khả năng bảo trì
- chi phí vận hành

**Được phép:**

- Từ chối các thiết kế vi phạm giới hạn ràng buộc
- Yêu cầu làm rõ các giới hạn

**KHÔNG được phép:**

- Tranh luận về mục tiêu sản phẩm
- Gợi ý thay đổi tính năng
- Tối ưu hóa vượt quá các yêu cầu đã nêu

---

### 4️⃣ Tác Nhân Đại Diện Người Dùng (User Advocate)

**Vai trò:**

- Đại diện cho người dùng cuối

_Các lĩnh vực trọng tâm:_

- Tải trọng nhận thức (độ khó khi sử dụng)
- tính khả dụng
- tính rõ ràng của luồng trải nghiệm
- cách xử lý lỗi từ góc nhìn người dùng
- sự sai lệch giữa ý định và trải nghiệm thực tế

**Được phép:**

- Xác định các khía cạnh gây bối rối hoặc hiểu lầm
- Cảnh báo các thiết lập mặc định kém hoặc hành vi không rõ ràng

**KHÔNG được phép:**

- Thiết kế lại kiến trúc
- Thêm tính năng
- Gạt bỏ các mục tiêu đã đề ra của người dùng

---

### 5️⃣ Tác Nhân Tích Hợp / Trọng Tài (Integrator / Arbiter)

**Vai trò:**

- Giải quyết xung đột
- Chốt các quyết định cuối cùng
- Thực thi các tiêu chí thoát (kết thúc kỹ năng)

**Được phép:**

- Chấp nhận hoặc bác bỏ các ý kiến phản đối
- Yêu cầu sửa đổi thiết kế
- Tuyên bố thiết kế đã hoàn thiện

**KHÔNG được phép:**

- Sáng tạo ra các ý tưởng mới
- Thêm yêu cầu
- Mở lại các quyết định đã chốt mà không có lý do chính đáng

---

## Quy Trình

### Giai Đoạn 1 — Thiết Kế Đơn Tác Nhân (Single-Agent Design)

1. Nhà Thiết Kế Chính chạy **kỹ năng `brainstorming` tiêu chuẩn**
2. Cửa ải "Chốt Mức Độ Hiểu" được hoàn thành và xác nhận
3. Thiết kế ban đầu được tạo ra
4. Bắt đầu ghi Nhật Ký Quyết Định

_Các tác nhân khác chưa tham gia ở bước này._

---

### Giai Đoạn 2 — Vòng Lặp Đánh Giá Có Cấu Trúc

Các tác nhân được gọi vào **lần lượt từng người một**, theo thứ tự sau:

1. Tác Nhân Hoài Nghi / Thách Thức
2. Tác Nhân Bảo Vệ Ràng Buộc
3. Tác Nhân Đại Diện Người Dùng

Đối với mỗi người đánh giá:

- Phản hồi phải rõ ràng và đúng phạm vi
- Các phản đối phải tham chiếu đến các giả định hoặc quyết định trước đó
- Không được phép đưa vào tính năng mới

Nhà Thiết Kế Chính phải:

- Phản hồi từng ý kiến phản đối
- Chỉnh sửa thiết kế nếu cần thiết
- Cập nhật Nhật Ký Quyết Định

---

### Giai Đoạn 3 — Tích Hợp & Phán Xử

Tác Nhân Tích Hợp / Trọng Tài sẽ xem xét:

- thiết kế cuối cùng
- Nhật Ký Quyết Định
- các phản đối chưa được giải quyết

Trọng Tài phải quyết định một cách dứt khoát:

- phản đối nào được chấp nhận
- phản đối nào bị bác bỏ (kèm theo lý do)

---

## Nhật Ký Quyết Định (Tài Liệu Bắt Buộc)

Nhật Ký Quyết Định phải ghi lại:

- Quyết định đã đưa ra
- Các phương án thay thế đã xem xét
- Các phản đối đã nêu
- Cách giải quyết và lý do

Không có thiết kế nào được coi là hợp lệ nếu không có nhật ký hoàn chỉnh.

---

## Tiêu Chí Thoát (Điểm Dừng Bắt Buộc)

Bạn chỉ có thể thoát khỏi quá trình Lên Ý Tưởng Đa Tác Nhân **khi tất cả các điều sau đều đúng**:

- Cửa ải Chốt Mức Độ Hiểu đã hoàn tất
- Tất cả các tác nhân đánh giá đều đã được gọi vào
- Tất cả các phản đối đều đã được giải quyết hoặc bác bỏ rõ ràng
- Nhật Ký Quyết Định đã hoàn tất
- Trọng Tài đã tuyên bố thiết kế có thể chấp nhận được

Nếu bất kỳ tiêu chí nào không được đáp ứng:

- Tiếp tục đánh giá
- KHÔNG tiến hành triển khai

Nếu kỹ năng này được gọi bởi một luồng điều phối hoặc định tuyến, bạn PHẢI báo cáo trạng thái xử lý cuối cùng một cách rõ ràng là: APPROVED (CHẤP THUẬN), REVISE (CẦN SỬA ĐỔI), hoặc REJECT (TỪ CHỐI), kèm theo một lý do ngắn gọn.

---

## Các Lỗi Mà Kỹ Năng Này Ngăn Chặn

- Sự hỗn loạn khi có quá nhiều ý tưởng
- Sự đồng thuận ảo tưởng (Hallucinated consensus)
- Các thiết kế đơn tác nhân quá tự tin
- Các giả định ngầm định
- Triển khai quá sớm
- Tranh luận không hồi kết

---

## Các Nguyên Tắc Chính

- Một người thiết kế, nhiều người đánh giá
- Sự sáng tạo được tập trung
- Sự phản biện bị giới hạn
- Các quyết định phải rõ ràng
- Quy trình phải có điểm kết thúc

---

## Nhắc Nhở Cuối Cùng

Kỹ năng này tồn tại để trả lời một câu hỏi với sự tự tin:

> "Nếu thiết kế này thất bại, chúng ta đã làm mọi thứ hợp lý để phát hiện nó từ sớm chưa?"

Nếu câu trả lời là không rõ ràng, **không được thoát khỏi kỹ năng này**.

## Khi Nào Sử Dụng

Kỹ năng này có thể áp dụng để thực thi quy trình làm việc hoặc các hành động được mô tả trong phần tổng quan.

## Ví Dụ

**Yêu cầu của người dùng:**

> Sử dụng @multi-agent-brainstorming cho tác vụ này: Mô phỏng quy trình đánh giá chéo có cấu trúc bằng cách sử dụng nhiều tác nhân chuyên biệt để xác thực thiết kế, làm rõ các giả định ngầm và xác định các điểm có thể gây lỗi trước khi triển khai.

## Hạn Chế

- Chỉ sử dụng kỹ năng này khi nhiệm vụ phù hợp rõ ràng với phạm vi được mô tả ở trên.
- Không coi đầu ra như một sự thay thế cho việc xác thực dựa trên môi trường thực tế, kiểm thử hoặc đánh giá từ chuyên gia.
- Dừng lại và yêu cầu làm rõ nếu thiếu các đầu vào cần thiết, quyền hạn, ranh giới an toàn hoặc tiêu chí thành công.
