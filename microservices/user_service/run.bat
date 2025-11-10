@echo off
echo Compiling User Service...
call mvn clean compile
if %ERRORLEVEL% neq 0 (
    echo Compilation failed!
    pause
    exit /b 1
)

echo Starting User Service...
call mvn spring-boot:run
pause

