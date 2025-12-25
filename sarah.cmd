@echo off
REM Sarah Sovereign Shorthand Wrapper
REM Usage: sarah [command]

IF "%1"=="" (
    echo [SARAH]: Please specify a command (status, push, wake, log, 133)
    GOTO End
)

"%~dp0.venv\Scripts\python.exe" "%~dp0python\sarah_suite.py" %*

:End
