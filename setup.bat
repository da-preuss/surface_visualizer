:: creates and activates the virtual environment to install packages
python -m venv env
call .\env\Scripts\activate
:: upgrade pip
python -m pip install --upgrade pip
:: install required packages
pip install -r requirments.txt