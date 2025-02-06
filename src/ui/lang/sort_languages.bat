@echo off
setlocal enabledelayedexpansion

:: Path to the JSON file
set JSON_FILE=.\lang\languages.json

:: Check if jq is installed
where jq >nul 2>&1
if %errorlevel% neq 0 (
    echo jq could not be found. Please install jq to sort JSON files.
    exit /b 1
)

:: Sort the JSON using jq
jq "sort_by(.id)" "%JSON_FILE%" > temp.json
move /y temp.json "%JSON_FILE%"

echo JSON file has been sorted alphabetically by 'id'.