import os
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import random


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'somesecret'


db = SQLAlchemy(app)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    name = db.Column(db.String(80), unique=True, nullable=False)
    generation = db.Column(db.Integer)
    type_one = db.Column(db.String(80), nullable=False)
    type_two = db.Column(db.String(80), nullable=False)
    height = db.Column(db.Float)
    weight =  db.Column(db.Float)

    def __init__(self, number, name, generation, type_one, type_two, height, weight):
        
        self.number = number
        self.name = name
        self.generation = generation
        self.type_one = type_one
        self.type_two = type_two
        self.height = height
        self.weight = weight


@app.route('/')
def index():
    pokemon = "pokemon"
    print(len(pokemon))
    total_pokemon = len(Pokemon.query.all())
    random_number = random.randint(1, total_pokemon)
    the_pokemon = Pokemon.query.filter(Pokemon.id == random_number)
    print(the_pokemon[0].name)


    return render_template("index.html", pokemon=pokemon)

if __name__ == '__main__':
    db.create_all()
    app.run(host=os.environ.get('IP', "0.0.0.0"),
            port=int(os.environ.get('PORT', 8000)),
            debug=True)