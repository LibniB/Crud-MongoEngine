from mongoengine import Document, ReferenceField,StringField,IntField,EmailField

class usuarios(Document):
    usuario=StringField(max_length=50,required=True,unique=True)
    password=StringField(max_length=50)
    nombres=StringField(max_length=50)
    apellidos=StringField(max_length=50)
    correo= EmailField(required=True,unique=True)

class categorias(Document):
    nombre=StringField(max_length=50,unique=True)

class productos(Document):
    codigo=IntField(unique=True)
    nombre=StringField(max_length=50)
    precio=IntField()
    categoria= ReferenceField(categorias)

productos= productos.objects()
print(productos)