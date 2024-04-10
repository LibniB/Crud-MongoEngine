from flask import Flask
from flask_mongoengine import MongoEngine
from mongoengine import connect
from json import JSONEncoder
import os

app = Flask(__name__)

app.secret_key= os.urandom(10)
app.config['MONGODB_HOST'] = "mongodb+srv://libnibetancourth:12345678Lb@cluster0.xng9auw.mongodb.net/"
app.config['MONGODB_DB'] = "GestionProductos"
app.config['UPLOAD_FOLDER'] = './static/imagenes'

db = MongoEngine(app)

    
if __name__ == '__main__':   
    from controlador.productoController import * 
    from controlador.usuarioController import *
    app.run(port=5000, host='0.0.0.0', debug=True)
