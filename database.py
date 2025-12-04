from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Inizializaçao do ORM, criado aqui para nao ter as importaçoes circulares e nao ocorrer travamentos