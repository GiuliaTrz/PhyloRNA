# Pyhlorna 
Phylorna is a Python web application designed for visualizing the PhyloRNA database. The application is built using the Flask framework and provides an interactive interface for exploring RNA sequences and their phylogenetic relationships.

## Requirements and Installation
- Python 3.10
- The packages in requirements.txt
- A running instance of the PhyloRNA database (MongoDB)

To install the required packages, run:
```
pip install -r requirements.txt
```
if the database is not hosted locally, update the database connection string in `config.py`.

The backend for MongoDB interaction is in `db_managment/menu.py`. Here you can manage the database with a CLI tool.

## Running the Application
Because the application runs on an apachi server with other services, the urls has a prefix `/phylorna`. If you want to run it standalone, you have to change all the urls in the templates.

To start the Flask application, run:
```
python app.py
```
with a running MongoDB instance.
