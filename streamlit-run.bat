@echo off
title Chay du an Python
echo Dang kich hoat .venv va chay script...

:: Kích hoạt môi trường ảo
call .venv\Scripts\activate.bat

:: Chạy file script của bạn (thay main.py bằng file của bạn)
streamlit run main.py

:: Tạm dừng để bạn đọc log/lỗi nếu có, bấm phím bất kỳ để tắt cửa sổ
pause
