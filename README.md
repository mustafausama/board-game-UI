## WebTabletop
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
1. open directory __room_frontend__, and type in cmd next lines:
    1. `npm install` if it's first time
    1. `npm start` to run the frontend. `localhost:3000`should be opened automatically
### Database manipulations
1. Type `python manage.py init_chess_game` in cmd to fill the db with one new chess game. Message with game id should be returned
1. Type `python manage.py clear_db` in cmd to clear the database from all entities
### What to improve in the project
1. Implement the Chess completely by providing next features:
    1. Castling
    1. Promotion
    1. En passant
    1. Check
    1. Checkmate
    1. Draw
1. Implement the Settlers of Catan. There are library 'catan', it will help you a lot by providing a logic part.
1. Implement rooms system
1. Implement spectators logic
### First development team (the ones you should hate if you work on this project after us)
1. Vyacheslav Vasilev, B17-SE-02 – Backend
1. Evgeniy Trantsev, B18-SNE – Frontend
1. Mustafa Abdelrahman, B19-05 – Frontend
