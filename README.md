
# Esqueleto
## _A Flask Template Project_

Esqueleto is a basic Flask app to serve as a template for other projects. It provides barebones functionality for configuration, model loading, and view registration.

#### What is it?
It's a foundation, but requires additional know-how. It has a great base db model (built on SQLAlchemy) and useful mixins, as well as a dynamic loader for additional models built anywhere in the application. The same applies for views/routes. 

#### What this isn't
This app does not provide "out-of-the-box" functionality, or a cookie-cutter template to merely tweak with a few customizations. It also does not include any design templates (html/css). It isn't very fleshed out. It is not a real boy!
### Dependencies
The project relies heavily on other useful plugins that are already configured. These are a few of the key plugins:
- [**Flask-Classful**](https://flask-classful.teracy.org/) - Class-based views (allows you to group similar views in a single class)
- [**Flask-SQLAlchemy**](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - db administration - SQL toolkit and Object Relational Mapper 
- [**python-dotenv**](https://pypi.org/project/python-dotenv/) - Reads key-value pairs from a `.env` file and can set them as environment variables

## Quick Start

1. Clone the Repo:
```sh
$ git clone https://github.com/tataraba/Esqueleto.git
$ cd Esqueleto
```
2. Initialize and activate a virtualenv:
```py
py -m venv .venv
```
3. Install the dependencies:
```py
pip install -r requirements.txt
```
4. Create a file in project root called ```.env``` and add these lines to the file:
```py
FLASK_APP='wsgi.py'
FLASK_ENV='development'
```
5. Run the application:
```py
flask run
```
When you navigate to localhost http://localhost:5000 you should see:
___
## Hola Cadaveres!
Bones!
___

## Project Structure
![esq_file_tree](https://user-images.githubusercontent.com/46942991/117201048-0b8c0e00-ada1-11eb-89a6-ebc60b63fd9b.jpg)

or

```
Esqueleto
├─ .gitignore
├─ config.py
├─ guni_config.py
├─ requirements.txt
├─ skeleton
│  ├─ db.py
│  ├─ models
│  │  ├─ base.py
│  │  ├─ mixins
│  │  │  └─ query.py
│  │  └─ __init__.py
│  ├─ static
│  │  ├─ css
│  │  └─ img
│  ├─ templates
│  │  ├─ errors
│  │  │  ├─ 404.jinja2
│  │  │  └─ 500.jinja2
│  │  ├─ main
│  │  │  └─ index.jinja2
│  │  └─ main-layout.jinja2
│  ├─ views
│  │  ├─ index.py
│  │  └─ __init__.py
│  └─ __init__.py
└─ wsgi.py

```

### Modules
###### ```wsgi.py```

Most flask apps have a top level module for creating the app. In this case, it is ```wsgi.py``` which is used by WSGI services (like Gunicorn, for example) for serving the application. It calls the ```create_app``` method from the application folder (skeleton).

###### ```skeleton/__init__.py```
This is where the magical ```create__app(config=None)``` method lives, the heart of a flask project. A few things to note here. The application will not load if it does not find a configuration file (either provided, or in default location). However, a configuration file is provided in root directory (```config.py```). The configuration file uses the ```python-dotenv``` plugin/module to bring in environment variables. Don't forget Step 4 in the Quick Start guide.

###### ```skeleton/db.py```
Here, we instantiate SQLAlchemy as the database model. This file contains the ```init_db``` method to handle database setup. Among other things, it includes the important ```load_models``` function that handles automatic model discovery (more on this later). Lastly, we call ```db.init_app(app)``` to use Flask's built in mechanism for database functionality.

###### ``` mylib/loaders.py```
The _key_ to automatic model/view discovery. Long story short, we search for all modules within a given directory, and we load modules if they pass certain checks. For example we use ```is_model``` to find any object of type ```Model``` and then use ```load_model``` for script and app availability. Same logic applies for views, wherein ```is_view``` searches for ```FlaskView``` objects--used by plugin ```Flask-Classful``` for class-based view handling.

###### ```views/__init__.py```
We use the ```get_views``` method from ```mylib/loaders.py``` to dynamically load views and register them within the ```init_views``` method (which is called in the ```creat_app``` method in ```__init__.py```).

###### ```models/base.py```
Custom base ```Model``` class (all application models will subclass) removes common repetition common in SQLAlchemy and adds a few common columns like primary key (id) and timestamp fields. But perhaps more importantly, it includes a ```QueryMixin``` in its class definition.

###### ```models/mixins/query.py```
Awesome helper functions that make common database operations easier to deal with, such as ```find_in```, ```find_not_in```, ```first```, or simpler CRUD methods like ```save``` or ```delete```.

## What Next?
You are going to want to flesh things out a little bit. Here are a couple of ideas, but these are just starting points, and hardly exhaustive of the directions you could go.
###### Session Management
I have not included a session management tool (yet), but this could be handled with plugins such as ```Flask-Login``` or ```Flask-User```. I may add that functionality in a future update.
###### Designing the Frontend
Under the ```templates``` directory, there is a barebones ```main-layout.jinja2``` file. This can be used as the underlying design for your web app. This could include header/footer/user elements that persist throughout your app. We already have basic 404 and 500 error pages could also use some help. From there, you could extend design with any number of templates. Some knowledge of the Jinja templating language is required.
###### Class-based View Handling
Flask already provides class-based view handling, but there are certain limitations. For this task, we use ```Flask-Classful```, which enables a powerful creation tool. One thing to keep in mind is that each view module must contain an ```__all__``` helper method that lists the views you want to register in your app. This list is used by the ```dynamic_loader``` in our ```mylib/loaders.py``` module. Everything else you need is in ```Flask-Classful``` documentation.
###### Models
Any additional models will be discovered by the ```dynamic_loader``` method. Here you can build database models to your heart's content.

## Resources
Most of _Esqueleto_ is structured after the [_"How I Use Flask"_](https://bobwaycott.com/blog/how-i-use-flask/) series by [Bob Waycott](https://bobwaycott.com/). I highly recommend it to get more background and details about dynamic loading and project structure.

I also recommend the [Hackers and Slackers](https://hackersandslackers.com/) website and their own series on how to [build Flask apps](https://hackersandslackers.com/series/build-flask-apps/).

## License
MIT
