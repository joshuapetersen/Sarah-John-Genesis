# Python Virtual Environment Setup Guide

## Steps to Create and Activate a Virtual Environment

1. Open a terminal in your project directory (e.g., C:\SarahCore).
2. Run the following command to create a new virtual environment:

    python -m venv .venv

3. Activate the virtual environment:
   - On Windows (PowerShell):

        & .venv\Scripts\Activate.ps1

   - On Windows (Command Prompt):

        .venv\Scripts\activate.bat

   - On Linux/macOS:

        source .venv/bin/activate

4. Install required packages (example):

    pip install -r requirements.txt

5. To deactivate the environment:

    deactivate

## Notes
- All Python packages installed while the environment is active will be isolated from the global Python installation.
- Use the activated environment for all project-related commands and scripts.
