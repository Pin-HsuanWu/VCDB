# DBMS-VersionControl

## 開發使用
1. 安裝 XQuartz (macos)、Xming (windows): 使terminal可以連接到X11服務器軟體
2. run docker
- docker-compose up

## 實際運作
1. construct virtual venv (macos)
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt

2. 依照.env-example 撰寫.env檔

3. run app
- python3 ./app/GUI.py

4. 參考 test_doc.txt 測試功能