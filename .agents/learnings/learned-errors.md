**Ngay: 16/10/2026, Gio: 01:24**

- **Mo ta loi:** Import test fail vi thieu dependencies (dotenv, gspread, pandas) trong venv.
- **Nguyen nhan:** .venv moi duoc tao chua duoc pip install -r requirements.txt, nen cac module phu thuoc chua co san.
- **Cach khac phuc:** Chay `pip install -r requirements.txt` trong venv truoc khi chay bat ky import test nao.
- **Bai hoc rut ra:** Luon chay `pip install -r requirements.txt` de khoi tao venv truoc khi test. Dung sys.path trick thay vi import truc tiep neu chi can test logic doc lap.

**Ngay: 16/10/2026, Gio: 11:46**

- **Mo ta loi:** Chạy test bằng lệnh `pytest` toàn cục bị lỗi `ModuleNotFoundError: No module named 'pandas'`.
- **Nguyen nhan:** Gọi `pytest` từ hệ thống môi trường ngoài thay vì dùng interpreter/script trong môi trường ảo `.venv` của dự án.
- **Cach khac phuc:** Sử dụng `.venv\Scripts\pytest` (hoặc `.venv\Scripts\python -m pytest`) để đảm bảo nạp đúng virtual environment.
- **Bai hoc rut ra:** Luôn sử dụng runner từ `.venv\Scripts\` khi chạy test, flake8, black trên môi trường Windows.
**Ngày: 17/10/2026, Giờ: 10:15**

- **Mô tả lỗi:** Lỗi `NameError: name 'run_sync' is not defined` khi chạy test mới `test_run_sync_retry_mode`.
- **Nguyên nhân:** Hàm `run_sync` trước đó chỉ được import cục bộ bên trong test case cũ `test_run_sync_flow` thay vì import ở cấp module (top-level).
- **Cách khắc phục:** Chuyển `run_sync` lên import ở đầu file `tests/test_sync_service.py` để tất cả các test case đều có thể sử dụng.
- **Bài học rút ra:** Luôn khai báo đầy đủ các function/class cần kiểm thử ở đầu file test, tránh import cục bộ ngầm bên trong một hàm test duy nhất.
