@echo off
title ICLab Table
color 03
py --version >nul 2>nul
if NOT %ERRORLEVEL% == 0 goto E_python
goto S_table
:S_table
py Table.py
if NOT %ERRORLEVEL% == 0 goto debug
exit
:E_python
echo No Python environment detected, please go visit https://www.python.org/downloads/windows/ to download and install a Python3 environment
echo Starting local CMD shell
cmd
:debug
pause
goto S_table