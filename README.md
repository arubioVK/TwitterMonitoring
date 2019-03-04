# TwitterMonitoring
Many users have suffered a theft of Twitter account. 
The hackers have supplanted their identity and have Tweets, embarrassing the company.

With this tool we can configure our Twitter account and if we put a Tweet that does not comply with the parameters the tweet will be erased and will alert the user through an email.
In this way, we will minimize the repercussion of having suffered an account theft.

The configuration parameters are as follows:
* Suspicious links
* The tweet must be in a certain language
* It must not contain offensive language
* Send tweets in a certain time
* Send tweets in a certain country

All these parameters are configurable. 
There is a thread for each account that is being monitored.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
### Prerequisities
The first thing to do is install python 
```
sudo apt install python3.6
```
The second step
```
pip install -r requirements.txt
```
### Configuration
In the file /app/local_setting.py:
* Change SECRET_KEY.
* Set the settings of your email. 

In the file /app/extras/emails.py:
* Again, set the settings of your email. 


## Running
### Create a Database
It's necessary to create a database in case of not existing.
```
python manage.py init_db
```
A user with admin role will be created.
```
username: admin@admin.com
password: 1
```
### Starting the web application
```
python manage.py runserver
```
You can now point your browser to: http://localhost:5000/

