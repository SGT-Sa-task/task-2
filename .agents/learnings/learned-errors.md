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

