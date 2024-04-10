
from flask import Flask, render_template, request, jsonify,redirect, url_for,abort, session
import pymongo
import os
from bson.objectid import ObjectId
import base64
from PIL import Image
from io import BytesIO
from bson.json_util import dumps
from flask_mongoengine import MongoEngine
from models.model import productos,categorias
from app import app 

    

@app.route('/listarProductos')
def inicio():
    if("user" in session):
        listaProductos = productos.objects()   
        return render_template('listarProductos.html', productos=listaProductos)
    else:
        mensaje="Debe primero iniciar sesion"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)

@app.route('/agregarProducto', methods=['POST'])  
def agregarProducto():
    if("user" in session):
            mensaje = None
            estado = False
            try:
                codigo = int(request.form['txtCodigo'])
                nombre = request.form['txtNombre']
                precio = int(request.form['txtPrecio'])
                idCategoria = ObjectId(request.form['cbCategoria'])
                foto = request.files['fileFoto'] 
                producto = {
                    "codigo": codigo,
                    "nombre": nombre,
                    "precio": precio,
                    "categoria": idCategoria,
                }
                resultado = productos.insert_one(producto)
                if (resultado.acknowledged):
                    idProducto = resultado.inserted_id  
                    nombreFoto = f'{idProducto}.jpg'
                    foto.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreFoto))
                    mensaje = 'Producto agregado correctamente'
                    estado = True
                    return render_template('listarProductos.html')
                else:
                    mensaje = 'No se pudo agregar el producto'
                    return mensaje
                
            except pymongo.errors as error: 
                mensaje = error
                return error
    else:
        mensaje="Debe primero iniciar sesion"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)


    
@app.route('/vistaAgregarProducto')
def vistaAgregarProducto():
    if ("user" in session):
        
        listaCategorias = categorias.objects()
        return render_template('frmAgregarProducto.html', categorias=listaCategorias)
    
    else:
        mensaje="Debe primero iniciar sesion"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)


@app.route("/eliminarProducto/<idProducto>", methods=["GET"])
def eliminar_producto(idProducto):
    if ("user" in session):
        try:
            resultado = productos.delete_one({"_id": ObjectId(idProducto)})
            if resultado.deleted_count == 1:
                print ('Entra condicion eliminar')
                return redirect(url_for("inicio"))  
            else:
                return "Producto no encontrado."
        except pymongo.errors.PyMongoError as error:
            return f"Error al eliminar el producto: {error}"
    else:
        mensaje="Debe primero iniciar sesion"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)




@app.route('/editarProducto/<idProducto>', methods=['GET'])
def vistaEditarProducto(idProducto):
    if ("user" in session):
        try:
        
            producto = productos.find_one({"_id": ObjectId(idProducto)})
            if producto is None:
                abort(404)  
            listaCategorias = categorias.find()
            return render_template('frmEditarProducto.html', producto=producto, categorias=listaCategorias)
        except Exception as e:
            return f"Error: {e}"
    else:
        mensaje="Debe primero iniciar sesion"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)


@app.route('/editar', methods=['POST'])
def editar():
    if("user" in session):
        try:
            idProducto = request.form['idProducto']
            codigo = int(request.form['txtCodigo'])
            nombre = request.form['txtNombre']
            precio = int(request.form['txtPrecio'])
            idCategoria = ObjectId(request.form['cbCategoria'])
            foto = request.files['fileFoto'] if 'fileFoto' in request.files else None

            # Actualiza los datos del producto en la base de datos
            productos.update_one(
                {"_id": ObjectId(idProducto)},
                {"$set": {
                    "codigo": codigo,
                    "nombre": nombre,
                    "precio": precio,
                    "categoria": idCategoria
                }}
            )

            # Si se proporcionó una nueva foto, guarda la foto
            if foto:
                nombreFoto = f"{idProducto}.jpg"
                foto.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreFoto))

            return redirect(url_for("inicio"))
        
        except Exception as error:
            return f"Error al editar el producto: {error}"
    else:
        mensaje="Debe primero iniciar sesion"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)
