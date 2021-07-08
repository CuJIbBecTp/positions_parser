# Positions Parser

A python program that go through gog.com/work job offers, extract them and store in a DB

## The following job features are extracted and stored:

    - title
    - department
    - tags
    - description
    - responsibilities
    - requirements

## How to install and run:

1. Clone the directory on your device
```
$ git clone https://github.com/CuJIbBecTp/positions_parser.git
```
2. Install Python 3 if you don't have it (https://www.python.org/downloads/
3. Create the virtual environment inside the project folder
```
$ python -m venv \path\to\project
```
4. activate the created environment
```
$ cd \venv\Scripts
$ activate
```
5. Install all the required libraries mentioned at the requirements.txt
```
$ pip install -r requirements.txt
```
6. At this step you are able to run the program
```
$ python run.py
```
   
## The example of program output:
```
$ python run.py
The program will go through gog.com/work job offers, extract them and store in a DB
Press 'y' if you want to drop the current database, otherwise press any other button 
$ y
The DB is empty
The new position of Software Engineer (Python) will be added to the database
The new position of Scrum Master will be added to the database
The new position of Senior Software Engineer (Backend) will be added to the database
The new position of Software Engineer (Fullstack) will be added to the database
Currently the following positions are available:
id=1, title=Software Engineer (Python), department=Engineering team
id=2, title=Scrum Master, department=Engineering team
id=3, title=Senior Software Engineer (Backend), department=Engineering team
id=4, title=Software Engineer (Fullstack), department=Engineering team
```
