# Pkoics
Python program generating icalendar file from schedule of Politechnika Krakowska. Program is using pulling data from API written by [Przemysław Wacek](https://github.com/Przem0s84).

# Requirements
- Python 3
  
# Usage
## Clone the repository
```bash
git clone https://github.com/Gromate/pkoics.git
cd pkoics
```
## Install required packages in virtual enviroment
```bash
python3 -m venv .
./bin/pip install -r requirements.txt
```

## Change config file and run the project
Change contents of `config.ini` in your favourite text editor and then run:
```bash
./bin/python run.py
```
Program should generate .ics file in ./output directory. Then you can import file into your calendar.

