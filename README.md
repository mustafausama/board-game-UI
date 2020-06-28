### %Projectname%
This project is an open-source web platform for tabletop games and creating bots for them.  
Developed by Innopolis University students during the 2020 summer internship
### How to run backend
1. Create a Python virtual environment:  
    1. create by typing `virtualenv venv` in cmd
    1. activate by typing  
    On Windows: `.\venv\Scripts\activate`  
    On macOS and Linux: `source venv/bin/activate`
1. Install dependencies: `pip install -r requirements.txt`
1. Type `python manage.py makemigrations` and `python manage.py migrate` to create a local database and migrate all changes there
1. Type `python manage.py runserver` from the __board-game-UI__ directory
1. Open `127.0.0.1:8000` or `localhost:8000` and use the backend API
### How to run frontend

### Database manipulations
1. Type `python manage.py init_chess_game` in cmd to fill the db with one new chess game
1. Type `python manage.py clear_db` in cmd to clear the database from all entities

### What to continue in the project and how
1. Implement the Settlers of Catan. There are library 'catan', it will help you a lot by providing a logic part.
1. 