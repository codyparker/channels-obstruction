# channels-obstruction
A simple game of Obstruction created to explore Django + Django Channels + ReactJS
Blog Post and Tutorial at: [http://www.codyparker.com/django-channels-with-react](http://www.codyparker.com/django-channels-with-react)


## Synopsis

I started this project to explore the [Django Channels](https://github.com/django/channels), which is an upcoming core app that adds asynchronous WebSocket support to the wonderful [Django Framework](http://www.djangoproject.com). Channels makes it very easy to build "real-time" apps in pure Django and Python, providing a great way to develop applications that require features such as "real-time" collaboration or chat for example.  

[Obstruction](http://www.papg.com/show?2XMX) is a 2-player pen and paper game which involves players taking turns claiming free spots on a grid. The spot they choose, and all surrounding spots are then claimed for that player and can no longer be claimed by another player. The play continues back-and-forth until there are no free spots to claim. The last player to successfully claim a spot, wins the game.

This project also uses [React](https://facebook.github.io/react/) to handle the reactive, client-side components. I picked React because I like it, but it could be swapped out with Angular/Vue/Knockout/etc....

## Features

* Full game functionality:
    * Authentication - Signup / Login
    * Game Lobby with live updating list of available games
    * Ability to create a game that will show up in other users' availiable games list
    * Gameboard that enforces Obstruction rules and allows players to take turns and see the results in real-time
    * Game log that tracks all moves and reports them live as they occur
    * Players can chat in the game log
* Lobby and Gameboard are made up of ReactJS components on the client-side
* Examples of how to mix standard Django templating with ReactJS
* Webpack integration to create separate bundles needed for different parts of the application
* Django Rest Framework used to help serialize data needed by React as well as provides API endpoints for client-side data calls
* Mixed use of DRF, standard Django context sent from the view, as well as communication through channels to demostrate multiple ways to interact with data and the Django backend

## Requirements

* Django >= 1.9
* [Django Channels](https://github.com/django/channels)
* [Django Rest Framework](http://www.django-rest-framework.org/)
* [Django Webpack Loader](https://github.com/owais/django-webpack-loader)
* Node & Node Package Manager

## Installation

* Fork and clone this repository
* Create a Python virtual environemnt
* In that environment, run ```pip install -r requirements.txt``` inside your project
* Install node modules with ```npm install```
* Create the local database with ```python manage.py migrate```
* Run webpack to build the components with ```webpack``` 
* Run Django development server on port 8080 - ```python manage.py runserver 8080```

## License

MIT License
