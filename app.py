from flask import Flask
from flask_mongoengine import MongoEngine
from mongoengine import connect
import os
app = Flask(__name__)
#clave secreta manejo de sesiones
app.secret_key= os.urandom(10)

app.config['UPLOAD_FOLDER'] = './static/imagenes'

connect(host="mongodb+srv://libnibetancourth:12345678Lb@cluster0.xng9auw.mongodb.net/GestionProductos")
db=MongoEngine(app)

from models.model import *
@app.route('/test')
def test_connection():
    # Intenta leer un documento de la colección de usuarios
    usario = usuarios.objects().first()
    if usario:
        return f'¡Conexión exitosa! Usuario: {usario.usuario}'
    else:
        return 'No se pudo leer el usuario. Verifica la conexión a la base de datos.'
if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)

# miConexion = pymongo.MongoClient('mongodb+srv://libnibetancourth:12345678Lb@cluster0.xng9auw.mongodb.net/')








