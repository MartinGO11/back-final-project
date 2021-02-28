import os
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from models import db, User, Servicios, Horarios, Extras, Agendamiento
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = os.getenv('DEBUG')
app.config['ENV'] = os.getenv('ENV')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db.init_app(app)
jwt = JWTManager(app)
Migrate(app, db)
CORS(app)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route("/")
def main():
    return render_template('index.html')

@app.route("/API/Login", methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username: return jsonify({"msg": "username es requerido"}), 400
    if not password: return jsonify({"msg": "contraseña es requerida"}), 400

    user = User.query.filter_by(username=username).first()
    if not user: return jsonify({"msg": "username/contraseña incorrectos"}), 400

    if not check_password_hash(user.password, password):
        return jsonify({"msg": "nombre/contraseña incorrectos"}), 400
    
    if username == "admin" and password == "admin":
        expires = datetime.timedelta(days=1)
        token = create_access_token (identify=username, expires_delta=expires)
        data = {
        "access_token": access_token,
        "user": {
            "username": username
            } 
        }
        return jsonify(data), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 400


    access_token = create_access_token(identity=user.id, expires_delta=expires)

    return jsonify(data), 200

#/Registro
@app.route("/API/Registro", methods=['POST'])
def register():
    print(request.get_json())
    username = request.json.get('username')
    apellido = request.json.get('apellido')
    password = request.json.get('password')
    email = request.json.get('email')
    phone = request.json.get('phone')

    if not username: return jsonify({"msg": "username es requiredo"}), 400
    if not apellido: return jsonify({"msg": "apellido es requiredo"}), 400
    if not password: return jsonify({"msg": "contraseña es requireda"}), 400
    if not email: return jsonify({"msg": "email es requiredo"}), 400
    if not phone: return jsonify({"msg": "telefono es requiredo"}), 400

    user = User.query.filter_by(email=email).first()
    if user: return jsonify({"msg": "el email ya se encuentra registrado"}), 400

    user = User()
    user.username = username
    user.password = generate_password_hash(password)
    user.apellido = apellido
    user.email = email
    user.phone = phone
    user.save()

    if not user: return jsonify({"msg": "Falló registro"}), 400

    expires = datetime.timedelta(days=1)

    access_token = create_access_token(identity=user.id, expires_delta=expires)

    data = {
        "access_token": access_token,
        "user": user.serialize()
    }

    return jsonify(data), 200

    return jsonify ({"access_token": "", "user": ""}), 200

#/PROFILE
@app.route("/API/Profile/", methods=['GET'])
@jwt_required()
def profile():
    id = get_jwt_identity()
    user = User.query.get(id)
    return jsonify(user.serialize()), 200

@app.route("/API/Profile/<int:users_id>/", methods=['GET'])
def serialize_with_servicio_extra(users_id, id = None):
    if request.method == 'GET':
            if id is not None:
                agendamientos = Agendamiento.query.filter_by(users_id=users_id, id=id).first()
                if not agendamientos: return jsonify({"msg": "Task not found"}), 404
                return jsonify(agendamientos.serialize()), 200
            else:
                user = User.query.get(users_id)
                return jsonify(user.serialize_with_servicio_extra()), 200

#/SERVICIOS
@app.route("/API/Servicios", methods=['POST'])
def crearServicios():
    id = request.json.get('id')
    nombre_servicio = request.json.get('nombre_servicio')
    valor_servicio = request.json.get('valor_servicio')

    if not id: return jsonify({"msg": "id servicio es requerido"}), 400
    if not nombre_servicio: return jsonify({"msg": "nombre servicio es requerido"}), 400
    if not nombre_servicio: return jsonify({"msg": "valor servicio es requerido"}), 400

    servicios = Servicios.query.filter_by(id=id).first()
    if servicios: return jsonify({"msg": "el id ya se encuentra en uso"}), 400
    
    servicios = Servicios()  
    servicios.id = id
    servicios.nombre_servicio = nombre_servicio
    servicios.valor_servicio = valor_servicio
    servicios.save()

    if not servicios: return jsonify({"msg": "Falló registro"}), 400

    data = {
        "servicios": servicios.serialize()
    }

    return jsonify(data), 200

@app.route("/API/Servicios/<int:id>", methods=['GET'])
def servicios(id = None):
    if id is not None:
        servicios = Servicios.query.get(id)
        if not servicios: return jsonify({"msg": "Servicio not found"})
        return jsonify(servicios.serialize()), 200
    else:
        servicios = Servicios.query.all()
        servicios = list(map(lambda servicios: servicios.serialize, servicios))
        return jsonify(servicios), 200

#/EXTRAS
@app.route("/API/Extras", methods=['POST'])
def crearExtras():
    id = request.json.get('id')
    nombre_extra = request.json.get('nombre_extra')
    valor_extra = request.json.get('valor_extra')

    if not id: return jsonify({"msg": "id extra es requerido"}), 400
    if not nombre_extra: return jsonify({"msg": "nombre extra es requerido"}), 400
    if not valor_extra: return jsonify({"msg": "valor extra es requerido"}), 400

    extra = Extras.query.filter_by(id=id).first()
    if extra: return jsonify({"msg": "el id ya se encuentra en uso"}), 400
    
    extra = Extras()  
    extra.id = id
    extra.nombre_extra = nombre_extra
    extra.valor_extra = valor_extra
    extra.save()

    if not extra: return jsonify({"msg": "Falló registro"}), 400

    data = {
        "extras": extra.serialize()
    }

    return jsonify(data), 200

@app.route("/API/Extras/<int:id>", methods=['GET'])
@app.route("/API/Extras/<int:id>", methods=['GET','PUT'])
def extras(id = None):
    if request.method == 'GET':
        if id is not None:
            extra = Extras.query.get(id)
            if not extra: return jsonify({"msg": "extra not found"}), 404
            return jsonify(extra.serialize()), 200
        else:
            extras = Extras.query.all()
            extras = list(map(lambda extra: extra.serialize(), extras))
            return jsonify(extras), 200

#/Extras
@app.route("/Extras", methods=['GET'])
def extra(id=None):
    extra = Extras.query.get(id)
    return jsonify(extra.serialize()), 200

# /Horarios

@app.route("/API/Horarios", methods=['POST', 'DELETE'])
def crearHorarios():
    horarios_id = request.json.get('horarios_id')
    fechas = request.json.get('fechas')
    horas = request.json.get('horas')

    if not horarios_id: return jsonify({"msg": "id horario es requerido"}), 400
    if not fechas: return jsonify({"msg": "fecha es requerido"}), 400
    if not horas: return jsonify({"msg": "hora es requerido"}), 400

    horario = Horarios.query.filter_by(horarios_id=horarios_id).first()
    if horario: return jsonify({"msg": "el id ya se encuentra en uso"}), 400
    
    horario = Horarios()  
    horario.horarios_id = horarios_id
    horario.fechas = datetime.datetime.strptime(fechas,'%d-%m-%Y').date()
    horario.horas = horas
    horario.save()

    if not horario: return jsonify({"msg": "Falló registro"}), 400

    data = {
        "horarios": horario.serialize()
    }

    return jsonify(data), 200
    
    if request.method == 'DELETE':
            horario = Horarios.query.get(id)
            if not horario: return jsonify({"msg": "Horario not found"}), 404
            horario.delete()
            return jsonify({"result": "Horario has delete"}), 200    

# Agendamiento
@app.route("/API/Checkout", methods=['GET', 'POST'])
@app.route("/API/Checkout/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def agendamientos(id = None):
    if request.method == 'GET':
        if id is not None:
            agendamiento = Agendamiento.query.get(id)
            if not agendamiento: return jsonify({"msg": "agendamiento not found"}), 404
            return jsonify(agendamiento.serialize()), 200
        else:
            agendamiento = Agendamiento.query.all()
            agendamiento = list(map(lambda agendamiento: agendamiento.serilize(), agendamientos))
            return jsonify(agendamiento), 200

    if request.method == 'POST':
        servicio = request.json.get("servicio")
        extra = request.json.get("extra")
        fecha = request.json.get("fecha")
        hora = request.json.get("hora")
        users_id = request.json.get("users_id")

        if not servicio: return jsonify({"msg": "servicio  is required"}), 400
        if not extra: return jsonify({"msg": "extra is required"}), 400
        if not fecha: return jsonify({"msg": "fecha is required"}), 400
        if not hora: return jsonify({"msg": "hora is required"}), 400
        if not users_id: return jsonify({"msg": "usuario is required"}), 400

        agendamiento = Agendamiento.query.filter_by(id=id).first()
        if agendamiento: return jsonify({"msg": "agendamiento ya existe"}), 400

        agendamiento = Agendamiento()
        agendamiento.servicio = servicio
        agendamiento.extra = extra
        agendamiento.fecha = fecha
        agendamiento.hora = hora
        agendamiento.users_id = users_id
        agendamiento.save()

        return jsonify(agendamiento.serialize()), 201

"""
####EXTRAS 2
@app.route("/API/extras_2", methods=['GET', 'POST'])
@app.route("/API/extras_2/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def extras(id = None):
    if request.method == 'GET':
        if id is not None:
            extra = Extras.query.get(id)
            if not extra: return jsonify({"msg": "Extra not found"}), 404
            return jsonify(extras), 200
        else:
            extras = Extra.query.all()
            extras = list(map(lambda extra: extra.serialize(), extras))
            return jsonify(extras), 200

        if request.method == 'POST':
            nombre = request.json.get("nombre")
            valor = request.json.get("valor")

            if not nombre: return jsonify({"msg": "nombre es requerido"}), 400
            if not valor: return jsonify({"msg": "valor es requerido"}), 400

            extra = Extra()
            extra.nombre = nombre
            extra.valor = valor
            extra.save()

            return jsonify(extra.serialize()), 201

        if request.method == 'PUT':
            nombre = request.json.get("nombre")
            valor = request.json.get("valor")

            extra = Extra()
            if nombre: extra.nombre = nombre
            if valor: extra.valor = valor
            extra.update()

            return jsonify(extra.serialize()), 200

        if request.method == 'DELETE':
            extra = Extra.query.get(id)
            if not extra: return jsonify({"msg": "Extra no entonctrado"}), 404
            extra.delete()
            return jsonify(extra.serialize()), 200
            return jsonify({"resultado": "Extra eliminado"}), 404
"""

if __name__ == '__main__':
    manager.run()
