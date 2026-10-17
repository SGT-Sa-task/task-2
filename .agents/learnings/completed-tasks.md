**Ngay: 16/10/2026, Gio: 01:23**

- **Tong quan:** Implement class `FindContact` su dung HubSpot Batch Read API, chien luoc email-first voi phone fallback, tu dong chunking <=100 records/request.
- **Deliverables:**
  - `services/sync_service.py` -- Them hang `_HUBSPOT_BATCH_LIMIT`, class `FindContact` (voi `_chunked`, `_batch_read_by_email`, `_batch_read_by_phone`, `find`)
  - `core/hubspot_api.py` -- Them hang `BATCH_URL`, ham `batch_read_contacts(identifiers, id_property)`

**Ngay: 16/10/2026, Gio: 11:48**

- **Tong quan:** Tái cấu trúc class `FindContact` trong `services/sync_service.py` chuyển sang sử dụng `retrieve_contacts` (phân trang và lập chỉ mục in-memory); cập nhật `retrieve_contacts` trong `core/hubspot_api.py` hỗ trợ tham số `properties` cho email và phone; bổ sung unit tests trong `tests/test_sync_service.py`.
- **Deliverables (San pham giao nop):**
  - `core/hubspot_api.py` -- Cập nhật hàm `retrieve_contacts` hỗ trợ query parameters `properties` và cấu trúc `params` dict.
  - `services/sync_service.py` -- Viết lại class `FindContact` với `_load_all_contacts` (phân trang lấy toàn bộ contact vào in-memory map) và `find(records)` đối chiếu email-first / phone-fallback.
    **Ngay: 16/10/2026, Gio: 16:20**

- **Tong quan:** Hoan thien sync flow doc Google Sheet: chi xu ly dong status=NEW, validate du lieu tam pass, tra cuu contact theo email/phone qua FindContact, create/update HubSpot contact, cap nhat status (SUCCESS/UPDATED/ERROR) va ghi HubSpot ID ve Google Sheet bang batch update.
- **Deliverables (San pham giao nop):**
  - `core/gsheet_api.py` -- Them ham `get_worksheet`, `read_contact_rows` (lay so dong `_row_number`) va `batch_update_cells` ghi ket qua hang loat.
  - `services/sync_service.py` -- Cap nhat ham `run_sync` loc status=NEW, `_validate_contact_data`, goi `FindContact`, thuc hien upsert HubSpot va batch update tro lai Google Sheet.
  - `tests/test_sync_service.py` -- Bo sung unit test `test_run_sync_flow` kiem thu toan bo luong dong bo va kiem tra dinh dang batch update cells.

**Ngày: 17/10/2026, Giờ: 09:31**

- **Tổng quan:** Nâng cấp giao diện Streamlit: hiển thị thông tin email Service Account bot kèm cảnh báo hướng dẫn cấp quyền Editor, cho phép thêm mới Google Sheet từ liên kết (tự động lấy tên và ID sheet qua API), lưu trữ vào `storage/local-data.csv`, chọn sheet để đồng bộ và cập nhật thời gian truy cập lần cuối theo định dạng `[HH:mm] - [DD/MM/yyyy]`.
- **Deliverables (Sản phẩm giao nộp):**
  - `services/sheet_storage_service.py` -- Module quản lý đọc bot account email, lưu và cập nhật `local-data.csv`, trích xuất ID sheet và ghi nhận thời gian truy cập lần cuối.
  - `core/gsheet_api.py` -- Bổ sung hàm `get_spreadsheet_info` lấy tên và ID sheet từ URL.
  - `services/sync_service.py` -- Cập nhật hàm `run_sync` hỗ trợ truyền `sheet_url` tùy chọn.
  - `main.py` -- Cải tiến toàn diện giao diện Streamlit: hiển thị bot info, hướng dẫn cấp quyền, form thêm sheet qua link, danh sách sheet đã lưu, bộ chọn sheet và ghi nhận thời gian truy cập.
  - `storage/local-data.csv` -- Chuẩn hóa cấu trúc cột `Tên của sheet,Link,ID Sheet,Truy cập lần cuối`.
  - `tests/test_sheet_storage_service.py` -- Bộ unit tests kiểm thử module lưu trữ và xử lý CSV.
  - `tests/test_gsheet_api.py` -- Bổ sung unit test cho `get_spreadsheet_info`.

**Ngày: 17/10/2026, Giờ: 10:05**

- **Tổng quan:** Tái cấu trúc giao diện Streamlit sang layout 2 cột dạng rộng (`layout="wide"`): Cột trái (65%) chứa toàn bộ thông tin động (thêm sheet, danh sách sheet đã lưu, chọn sheet để đồng bộ, nút sync và metrics kết quả), Cột phải (35%) chứa thông tin tĩnh (thông tin tài khoản bot, hướng dẫn cấp quyền Editor và quy chuẩn dữ liệu sheet).
- **Deliverables (Sản phẩm giao nộp):**
  - `main.py` -- Tái cấu trúc giao diện sang bố cục 2 cột (wide layout) tách biệt rõ ràng giữa thông tin tương tác động và hướng dẫn tĩnh.

**Ngày: 17/10/2026, Giờ: 10:16**

- **Tổng quan:** Tách chức năng đồng bộ: chia rõ luồng đồng bộ dòng mới (status=NEW) và luồng thử lại dòng lỗi (status=ERROR), bổ sung nút mở trực tiếp Google Sheet trong tab trình duyệt mới, cập nhật giao diện và hướng dẫn quy chuẩn dữ liệu.
- **Deliverables (Sản phẩm giao nộp):**
  - `services/sync_service.py` -- Cập nhật hàm `run_sync` hỗ trợ tham số `sync_mode` ("NEW" hoặc "RETRY") để lọc chính xác tập dữ liệu cần xử lý.
  - `main.py` -- Thêm `st.link_button` mở sheet trong tab mới, chia thành 2 nút thao tác riêng biệt "▶ Bắt đầu đồng bộ (NEW)" và "🔁 Thử lại dòng lỗi (ERROR)", cập nhật thông tin hướng dẫn ở cột bên phải.
  - `tests/test_sync_service.py` -- Bổ sung unit test `test_run_sync_retry_mode` kiểm thử chế độ RETRY.

**Ngày: 17/10/2026, Giờ: 10:37**

- **Tổng quan:** Bổ sung tính năng Khôi phục (Restore): xóa các contact vừa tạo mới trên HubSpot CRM trong lần đồng bộ gần nhất, hiển thị tooltip cảnh báo rõ ràng khi hover chuột, hoàn toàn không chỉnh sửa lại file Google Sheet.
- **Deliverables (Sản phẩm giao nộp):**
  - `core/hubspot_api.py` -- Bổ sung hàm `delete_contact(contact_id)` gọi HTTP DELETE đến HubSpot CRM.
  - `services/sync_service.py` -- Bổ sung trường `created_contact_ids` vào `SyncResult` và xây dựng hàm `restore_created_contacts(contact_ids)`.
  - `main.py` -- Quản lý `recently_created_ids` qua Session State, tích hợp nút "⏪ Khôi phục (Restore)" với tooltip hover và xử lý phản hồi kết quả sau khi xóa.
  - `tests/test_hubpot_api.py` & `tests/test_sync_service.py` -- Bổ sung unit test cho `delete_contact` và `restore_created_contacts`.
