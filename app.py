from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
app.debug = True
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db = SQLAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)

class Textile(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  description = db.Column(db.String(200))

  def __init__(self, name, description):
    self.name = name
    self.description = description

# Textile Schema
class TextileSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description')

# Init Schema
# strict so that it does not report errors
textile_schema = TextileSchema()
textiles_schema = TextileSchema(many=True)

# create a Textile
@app.route('/textile', methods = ['POST'])
def add_textile():
  name = request.json['name']
  description = request.json['description']

  new_textile = Textile(name, description)
  db.session.add(new_textile)
  db.session.commit()

  return textile_schema.jsonify(new_textile)

# Get textiles
@app.route('/textile', methods=['GET'])
def get_textiles():
  all_textiles = Textile.query.all()
  result = textiles_schema.dump(all_textiles)

  return jsonify(result)

# Get one textiles
@app.route('/textile/<id>', methods=['GET'])
def get_textile(id):
  textile = Textile.query.get(id)
  result = textile_schema.dump(textile)

  return jsonify(result)

# Update a Textile
@app.route('/textile/<id>', methods = ['PUT'])
def update_textile(id):
  textile = Textile.query.get(id)

  # Debugger
  # import pdb; pdb.set_trace()

  name = request.json['name']
  description = request.json['description']

  textile.name = name
  textile.description = description

  db.session.commit()

  return textile_schema.jsonify(textile)

# Remove textile
@app.route('/textile/<id>', methods=['DELETE'])
def delete_textile(id):
  textile = Textile.query.get(id)

  db.session.delete(textile)
  db.session.commit()

  return textile_schema.jsonify(textile)



# Run server
if __name__ == '__main__':
  app.run(debug=True)
