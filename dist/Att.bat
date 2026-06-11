py -m PyInstaller --onefile --noconsole --add-data "templates;templates" --add-data "static;static" --name StockMaster app.py

move /Y dist\StockMaster.exe .

echo Build concluido!