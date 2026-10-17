@echo off
title Kich hoat Virtual Environment
echo Dang kich hoat .venv...

:: Kích hoạt môi trường ảo
call .venv\Scripts\activate.bat

:: Giữ cửa sổ CMD mở ở trạng thái đã kích hoạt .venv
cmd /k
