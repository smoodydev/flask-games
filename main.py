import os
from flask import Flask, redirect, jsonify, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import random
import itertools

if os.path.exists("env.py"):
    import env
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
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

    def to_dict(self):
        as_dict = {
            "name": self.name,
            "generation":self.generation,
            "type_one": self.type_one,
            "type_two": self.type_two,
            "height":self.height,
            "weight":self.weight
        }
        return as_dict




@app.route('/test')
def test():
    test = "a"
    pk =  get_pokemon(test)
    if pk:
        return pk.name
    else:
        return "Shit"


def compare_pokemon(should, guess):
    # type_one_m = [should.type_one if should.type_one in {guess.type_one, guess.type_two}]
    types = []
    not_types = []
    should_types = [should["type_one"], should["type_two"]]
    if guess["type_one"] in should_types:
        types.append(guess["type_one"])
    else:
        not_types.append(guess["type_one"])
    if guess["type_two"] in should_types:
        types.append(guess["type_two"])
    else:
        not_types.append(guess["type_two"])
    
    


    height = [1, guess["height"]] if should["height"] > guess["height"] else [0,guess["height"]]
    weight = [1, guess["weight"]] if should["weight"] > guess["weight"] else [0,guess["weight"]]

    dict_back = {
        "name": guess["name"], 
        "types": types,
        "not_types": not_types,
        "height": height,
        "weight": weight
 
    }

    return dict_back

def get_pokemon(pokemon):
    is_pokemon = Pokemon.query.filter(Pokemon.name==pokemon).first()
    if (is_pokemon):
        is_pokemon = is_pokemon.to_dict()
    return is_pokemon


def new_pokemon(gen=False):
    if gen:
        allPokemon = Pokemon.query.filter(Pokemon.generation <= gen)
    else:
        allPokemon = Pokemon.query.all()
    
    random_number = random.randint(0, len(list(allPokemon)))
    the_pokemon = allPokemon[random_number]
    pokemon_dict = {
        "name": the_pokemon.name,
        "number": the_pokemon.number,
        "generation": the_pokemon.generation, 
        "type_one": the_pokemon.type_one, 
        "type_two": the_pokemon.type_two, 
        "height": the_pokemon.height, 
        "weight": the_pokemon.weight
        
    }
    session["pokemon"] = pokemon_dict
    session["attempts"] = []
    
    
    return pokemon_dict

@app.route("/new")
def new():
    new_pokemon(1)
    if "complete" in session:
        session.pop("complete")
    session.pop("attempts")
    return redirect("/")

@app.route('/guess_pokemon', methods=["POST"])
def guess_pokemon():
    word = request.form["pokemon"].capitalize()
    
    if ("complete" not in session):
        is_pokemon = get_pokemon(word)
        if is_pokemon:
            
            the_pokemon = session["pokemon"]
            print(the_pokemon)
            
            if word == the_pokemon["name"]:
                text_back = "You are a winner!"
                result = the_pokemon
                result["types"] = [the_pokemon["type_one"], the_pokemon["type_two"]]
                code = 2
                session["complete"] = True
            elif 'attempts' in session:
                attempts = session.get("attempts")
                attempts.append(word)
                session["attempts"] = attempts
                text_back = "The server received the word "+ word
                result = compare_pokemon(the_pokemon, is_pokemon)
                code = 1
            else:
                session["attempts"] = [word]
                code = 1
                text_back = "The server received the word "+ word
                result = compare_pokemon(the_pokemon, is_pokemon)
            # if "user" in session:
            #     updating = {"word":session["word"], "current_attempts": session["attempts"]}
            #     mongo.db.useraccount.update_one({"username": session["user"]}, {"$set" : updating})
            #     if "complete" in session:
            #         score = len(session["attempts"])
            #         mongo.db.useraccount.update_one({"username": session["user"]},{"$inc": {"score": 5 if score <= 3 else 7-score}})
            
            
            return jsonify(validated=True, result=result, code=code, text_back=text_back)
        else:
            return jsonify(validated=False, text_back="Not a Valid Pokemon")
    else:
        print("completed")
        text_back = "You have already completed this word"
    return jsonify(validated=False, text_back=text_back)


@app.route('/')
def index():
    if not all([key in session for key in ["pokemon", "attempts"]]):
        new_pokemon(1)
        
    pokemon = "pokemon"


    return render_template("index.html", pokemon=pokemon)



if __name__ == '__main__':
    db.create_all()
    app.run(host=os.environ.get('IP', "0.0.0.0"),
            port=int(os.environ.get('PORT', 8000)),
            debug=True)