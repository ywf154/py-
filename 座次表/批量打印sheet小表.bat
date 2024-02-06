@echo off
setlocal enabledelayedexpansion

REM 弹出对话框并获取文件路径
for /F "tokens=*" %%A in ('powershell -ExecutionPolicy Bypass -Command "Add-Type -AssemblyName System.Windows.Forms; $dialog = New-Object System.Windows.Forms.OpenFileDialog; $dialog.Filter = 'Excel 文件 (*.xlsx;*.xls)|*.xlsx;*.xls|所有文件 (*.*)|*.*'; $dialog.InitialDirectory = [Environment]::GetFolderPath('Desktop'); $dialog.Title = '选择要打印的 Excel 文件'; $result = $dialog.ShowDialog(); if ($result -eq 'OK') { $dialog.FileName }"') do set "excelPath=%%A"

if "%excelPath%"=="" (
    echo 文件路径为空，无法继续打印。
    exit /b
)

REM 检查文件是否存在
if not exist "%excelPath%" (
    echo 文件路径不存在或文件不存在，无法继续打印。
    exit /b
)

REM 获取 Excel 文件中的所有工作表名称
for /F "tokens=*" %%A in ('powershell -Command "(New-Object -ComObject Excel.Application).Workbooks.Open('%excelPath%').Sheets | ForEach-Object {$_.Name}"') do (
    set "sheetName=%%A"
    echo Printing !sheetName!

    REM 使用 Excel 程序打印指定工作表并设置不保存更改
    powershell -Command "$excel = New-Object -ComObject Excel.Application; $excel.DisplayAlerts = $false; $workbook = $excel.Workbooks.Open('%excelPath%'); $sheet = $workbook.Worksheets | Where-Object {$_.Name -eq '!sheetName!'}; $sheet.PrintOut(); $excel.Quit();"
)

endlocal
exit /b