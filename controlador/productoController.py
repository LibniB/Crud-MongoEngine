
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
    if "user" in session:
        try:
            listaProductos = productos.objects()  # Consulta la base de datos para obtener todos los productos
            return render_template('listarProductos.html', productos=listaProductos)
        except Exception as error:
            mensaje = 'Error al cargar la lista de productos: {}'.format(error)
            return render_template('error.html', mensaje=mensaje)
    else:
        mensaje = "Debe primero iniciar sesión"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)

@app.route('/agregarProducto', methods=['POST'])  
def agregarProducto():
    if "user" in session:
        try:
            codigo = int(request.form['txtCodigo'])
            nombre = request.form['txtNombre']
            precio = int(request.form['txtPrecio'])
            idCategoria = ObjectId(request.form['cbCategoria'])
            foto = request.files['fileFoto'] 
            producto_data = {
                "codigo": codigo,
                "nombre": nombre,
                "precio": precio,
                "categoria": idCategoria,
            }
            producto = productos(**producto_data)  # Crea un nuevo documento de productos
            producto.save()  # Guarda el nuevo producto en la base de datos
            if producto:
                idProducto = producto.id  # Obtiene el ID del producto insertado
                nombreFoto = f'{idProducto}.jpg'
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreFoto))
                mensaje = 'Producto agregado correctamente'
                return render_template('listarProductos.html', mensaje=mensaje)
            else:
                mensaje = 'No se pudo agregar el producto'
                return render_template('error.html', mensaje=mensaje)
        except Exception as error: 
            mensaje = 'Error al agregar el producto: {}'.format(error)
            return render_template('error.html', mensaje=mensaje)
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
            # Obtener el producto por su ID
            producto = productos.objects(id=idProducto).first()
            
            # Verificar si el producto existe
            if producto:
                # Eliminar el producto
                producto.delete()
                print ('Entra condicion eliminar')
                return redirect(url_for("inicio"))  
            else:
                return "Producto no encontrado."
        except Exception as error:
            return f"Error al eliminar el producto: {error}"
    else:
        mensaje="Debe primero iniciar sesion"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)



@app.route('/editarProducto/<idProducto>', methods=['GET'])
def vistaEditarProducto(idProducto):
    if "user" in session:
        try:
            producto = productos.objects.get(id=idProducto)
            listaCategorias = categorias.objects()
            return render_template('frmEditarProducto.html', producto=producto, categorias=listaCategorias, idProducto=idProducto)
        except productos.DoesNotExist:
            abort(404)
        except Exception as e:
            return f"Error: {e}"
    else:
        mensaje = "Debe primero iniciar sesión"
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

            # Obtener el producto a editar
            producto = productos.objects.get(id=idProducto)

            # Actualizar los campos del producto
            producto.codigo = codigo
            producto.nombre = nombre
            producto.precio = precio
            producto.categoria = idCategoria

            # Guardar los cambios en la base de datos
            producto.save()

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

