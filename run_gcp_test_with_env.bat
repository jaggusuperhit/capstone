@echo off
call d:\ML-Ops\capstone\capstone\Scripts\activate.bat
set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\Admin\Downloads\rag-youtube-457803-5f107bcfa28f.json
echo Environment variable set: %GOOGLE_APPLICATION_CREDENTIALS%
python test_gcp_connection.py
pause
