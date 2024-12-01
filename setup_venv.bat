@echo off
echo Creating Python virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing requirements...
pip install -r requirements.txt

echo Setup complete! Your virtual environment is ready.
echo To activate the virtual environment, run: venv\Scripts\activate.bat
