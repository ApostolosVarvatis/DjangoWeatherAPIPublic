# PROJECT TITLE: WeatherAPI
## Github Repo: https://github.com/ApostolosVarvatis/DjangoWeatherAPIPublic
## Description
WeatherAPI is a REST API tool for weather data with four endpoints, created with Django and the Django-Rest-Framework, and uploaded online using Git and GitHub.

More thoroughly the tech stack consists of:
- **Django** for the backend.
- **Django-Rest-Framework** for the API.
- **SQLite** as a relational database management system.
- **JavaScript** for interactive behavior.
- **Bootstrap** for the front end.
- **Github** and **Git** for CI/CD.


## Contents

This Django project contains multiple files and folders:

(Two apps exist under the project name "weather". One is "base" where the backend functionality and logic are, and "api" where the API endpoint logic is.)

- Inside the weather folder exists the basic structure of every Django project with the default SQLite3 database and the settings.py file that stores all of the important information about how the app runs.

- Inside the api folder, the basic structure of a Django app is again followed with urls.py containing endpoint routes, views.py containing the logic of the endpoints, and serializers.py containing the serialization for the models defined in base.models.

- Inside the base folder is another Django app with urls.py containing web app routes, views.py containing the logic of the web app, admin.py which registers the models in the admin panel for easy CRUD operations, and models.py containing all required database models. Lastly, the templates/base folder contains the index page of the web app.

- The requirements.txt file that lists all the needed dependencies to install and successfully run the Django app.

- To conclude, this README.md file tries to best explain the project.


## Instruction / How To Run

- Firstly you have to run pip install -r requirements.txt to install all required libraries. 

- Secondly to run the application you have two options:
    - 1. Quality > Time. On every call to the app's API, new data are being retrieved from the meteomatics API so that each endpoint is always as up-to-date as possible ignoring the slow response. This option is the default and uses the load_data function on each call. This is found under api/views.py at the start of each function.
    - 2. Time > Quality. Store the data once and then run API queries on that data. This option is more API-call efficient because it does only one call for the data and then works on that. To use this option you can comment out the call of the load_data function, which is located under api/views.py, at the start of each endpoint function. Then to reload data you can use the yellow button at the index of the app.

- Thirdly, if you want to run the application on debug mode, on settings.py turn debug mode to True. Otherwise, if you want to run with debug set to False run "python3 manage.py runserver --insecure", so that Django serves static files, even in a non-debug mode.

## Things to Note / Disclaimers:

- I defined "latest forecast" to be, depending on what time you made the API call, from that time I took the hour (ex: Current Time: 5:35 PM, Extracted Time: 5 PM) and defined it as the latest possible hour to get a forecast. So my database consists of hourly, as well as daily data for 3 locations.
    - For "List the latest forecast for each location for every day", I took the current hour of the call and extracted data from all locations and all days at that hour.
    - For "List the average the_temp of the last 3 forecasts for each location for every day", I took the current hour of the call, the previous hour, and the hour before (ex: Current Time: 5:35 PM, Extracted Time: 3+4+5PM). I took the average temperature from those and I did that for every day, for every location, for the same hour-frame.
    - For "Get the top n locations based on each available metric where n is a parameter given to the API call", I took all comparable metrics ('temp_max', 'temp_min', 'wind_gust', 'precipitation', 'weather_symbol', 'sea_pressure', 'uv_index') and calculated the average value for that metric for each location. I then ordered them in descending order and took the **n** first.

- Due to a free subscription to the metetomatics API data from 2 days ago cannot be accessed. Also, it is limited to 1 location and 10 parameters per call (that is why multiple calls exist in the load_data function) as well as limited to 500 calls per day with only 15 basic parameters to choose from.

- Used the meteomatics python connector for its usability and simplicity to extract data from their weather API.

- The project is using UTC for its date-time timezone for convenience purposes. Depending on your location there will be conversions needed to see your time on the timestamps of the API.

- The project is deployed on pythonanywhere.com and uploaded on Git Hub with the required security measures taken.

- For the REST Framework to work as intended on pythonanywhere.com, the whitenoise library and middleware are used to serve static files as intended.
