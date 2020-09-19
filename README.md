# SPEED Website

**To set up the Django project after cloning this repo, please install MySQL on your computers and proceed to the virtualenv section of this README first before anything. For the MySQL installation, look it up on the [website](https://dev.mysql.com/)**. If you use XAMPP for your MySQL, you will probably encounter problems in installing the necessary Django dependencies (i.e. mysqlclient), so I recommend you install MySQL in your devices.

## Initial Set-up

The .env file sent to you MUST BE PRESENT in the project root folder (i.e. the same folder as the manage.py). Without this .env, the website will return some errors when you try to run the server.

Whenever you run manage.py commands, remember also that your virtual environment must be activated. Read more about virtual environments below.

## Commands to Remember
### virtualenv
[Read more about python virtual environments here](https://www.geeksforgeeks.org/python-virtual-environment/)

A virtual environment is a tool that helps to keep dependencies required by different projects separate by creating isolated python virtual environments for them.

What are the commands you need to remember?
```
python -m venv ~/.virtualenvs/speed
```
This creates a virtual environment named tanongdb in a folder entitled .virtualenvs. 

```
source ~/.virtualenvs/speed/bin/activate
```
```
~\.virtualenvs\speed\Scripts\activate
```
This activates your virtualenv in your Terminal window, which means you can now use the dependencies installed in your venv.

```
pip install -r requirements.txt
```
After cloning this repository, `cd` into that repository. Run the command above to install all the dependencies listed in the requirements.txt of this repo to your virtualenv. Make sure your Terminal is at the same directory as the requirements.txt. **This command should be done when setting up the Django project.**

```
pip install [package_name]
```
If you find an external Python library which you think you can use for this project, you can install it in your virtualenv using this command. Don't forget to add the library and the version you installed to the requirements.txt so that other collaborators can also install the dependency in their virtualenvs.

### MySQL
```
mysql -u root -p
```
 - opens shell of MySQL

#### In the MySQL shell:
```
DROP DATABASE speed;
```
 - deletes the database named speed

```
CREATE DATABASE speed;
```
 - creates database named speed

**Note that the username and password of your MySQL configuration, as well as the name of the database you made, must match the ones in the .env file.**

### Github Workflow
Remember you're working with `develop` branch, so make sure to branch out of `develop`. Make a merge request from your branch to develop after.

### Django Commands
Please read the Django tutorials in their official docs to fully understand these commands.

1. Activate your virtualenv by running the command above: `source ~/.virtualenvs/speed/bin/activate` or `~\.virtualenvs\speed\Scripts\activate`
2. Run the script: `bash exec.sh` on Mac/Linux or `./exec.sh` on Windows.

Every time you want to run the server, repeat step #2 for running the `exec.sh`.
