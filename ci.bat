@echo off

set "PACKAGE=gridpet"
set "TARGET=%~1"

if not exist "%TARGET%" (set "TARGET=.")

if "%TARGET%"=="." (
    echo Running Ruff on entire repo.
    pause
)

ruff format "%TARGET%"
ruff check "%TARGET%"
ruff check --fix "%TARGET%"

pytest -v
