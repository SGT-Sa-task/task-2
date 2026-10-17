
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


