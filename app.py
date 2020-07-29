import os
from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'marvel.db')

db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database Created')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database Dropped')


@app.cli.command('db_seed')
def db_seed():
    ironman = Origin(character_name='Anthony Edward Stark',
                     alias='Ironman',
                     birthplace='Long Island, New York',
                     first_appearance='Tales of Suspence #39 (March, 1963)',
                     occupation='Inventor, Industrialist',
                     base='Seattle, Washington',
                     intelligence=100,
                     strength=85,
                     speed=70,
                     power=100)

    black_panther = Origin(character_name="T'Challa",
                           alias='Black Panther',
                           birthplace='Wakanda',
                           first_appearance='Captain America: Civil War',
                           occupation='King',
                           base='Wakanda',
                           intelligence=75,
                           strength=60,
                           speed=75,
                           power=70)

    db.session.add(ironman)
    db.session.add(black_panther)
    db.session.commit()
    print("Database seeded")


@app.route('/characters', methods=['GET'])
def characters():
    characters_list = Origin.query.all()
    result = origins_schema.dump(characters_list)
    return jsonify(result)


@app.route("/character_details/<int:character_id>", methods=['GET'])
def character_details(character_id: int):
    character = Origin.query.filter_by(character_id=character_id).first()
    if character:
        result = origin_schema.dump(character)
        return jsonify(result)
    else:
        return jsonify(message="This character does not exist"), 404


@app.route('/add_character', methods=['POST'])
def add_character():
    character_name = request.form['character_name']
    test = Origin.query.filter_by(character_name=character_name).first()
    if test:
        return jsonify(message="There is already a character by that name"), 409
    else:
        alias = request.form['alias']
        birthplace = request.form['birthplace']
        first_appearance = request.form['first_appearance']
        occupation = request.form['occupation']
        base = request.form['base']
        intelligence = int(request.form['intelligence'])
        strength = int(request.form['strength'])
        speed = int(request.form['speed'])
        power = int(request.form['power'])

        new_character = Origin(character_name=character_name,
                               alias=alias,
                               birthplace=birthplace,
                               first_appearance=first_appearance,
                               occupation=occupation,
                               base=base,
                               intelligence=intelligence,
                               strength=strength,
                               speed=speed,
                               power=power)
        db.session.add(new_character)
        db.session.commit()
        return jsonify(message='You added a new character'), 201


@app.route('/update_character', methods=['PUT'])
def update_character():
    character_id = int(request.form['character_id'])
    character = Origin.query.filter_by(character_id=character_id).first()
    if character:
        character.character_name = request.form['character_name']
        character.alias = request.form['alias']
        character.birthplace = request.form['birthplace']
        character.first_appearance = request.form['first_appearance']
        character.occupation = request.form['occupation']
        character.base = request.form['base']
        character.intelligence = float(request.form['intelligence'])
        character.strength = float(request.form['strength'])
        character.speed = float(request.form['speed'])
        character.power = float(request.form['power'])
        db.session.commit()
        return jsonify(message='You updated a character'), 202
    else:
        return jsonify(message="This character doesnt exist"), 404
    

@app.route('/remove_character/<int:character_id>',methods=['DELETE'])
def remove_character(character_id: int):
    character = Origin.query.filter_by(character_id=character_id).first()
    if character:
        db.session.delete(character)
        db.session.commit()
        return jsonify(message='You deleted a Character'), 202
    else:
        return jsonify(messsage='Character not found'), 404


# database models
class Origin(db.Model):
    __tablename__ = 'origin'
    character_id = Column(Integer, primary_key=True)
    character_name = Column(String)
    alias = Column(String)
    birthplace = Column(String)
    first_appearance = Column(String)
    occupation = Column(String)
    base = Column(String)
    intelligence = Column(Integer)
    strength = Column(Integer)
    speed = Column(Integer)
    power = Column(Integer)


class OriginSchema(ma.Schema):
    class Meta:
        fields = ('character_id', 'character_name', 'alias', 'birthplace', 'first_appearance'
                  , 'intelligence', 'strength')


origin_schema = OriginSchema()
origins_schema = OriginSchema(many=True)

if __name__ == '__main__':
    app.run()
