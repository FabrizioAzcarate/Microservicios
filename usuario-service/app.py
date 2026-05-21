import time

from flask import Flask, request
from flask_restx import Api, Resource, fields
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash

app = Flask(__name__)

api = Api(
    app,
    version='1.0',
    title='Microservicio Usuario',
    description='API REST para usuarios',
    doc='/swagger'
)

ns = api.namespace(
    'usuarios',
    description='Operaciones de usuarios'
)

engine = create_engine(
    'mysql+pymysql://root:root@mysql/microservicios_db'
)

conexion_exitosa = False

for intento in range(10):

    try:
        with engine.connect():
            conexion_exitosa = True
            print('Conexion a MySQL exitosa')
            break

    except Exception:

        print(
            f'Esperando MySQL... intento {intento + 1}'
        )

        time.sleep(5)

if not conexion_exitosa:
    raise Exception('No se pudo conectar a MySQL')

with engine.begin() as connection:

    connection.execute(text('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT PRIMARY KEY,
            nombre VARCHAR(100),
            email VARCHAR(100),
            password VARCHAR(255)
        )
    '''))

usuario_input_model = api.model('UsuarioInput', {
    'id': fields.Integer(
        required=True,
        description='ID único del usuario'
    ),

    'nombre': fields.String(
        required=True,
        description='Nombre completo del usuario'
    ),

    'email': fields.String(
        required=True,
        description='Correo electrónico'
    ),

    'password': fields.String(
        required=True,
        description='Contraseña del usuario'
    )
})

usuario_model = api.model('Usuario', {
    'id': fields.Integer(
        required=True,
        description='Identificador del usuario'
    ),

    'nombre': fields.String(
        required=True,
        description='Nombre completo del usuario'
    ),

    'email': fields.String(
        required=True,
        description='Correo electrónico del usuario'
    )
})

@ns.route('')
class UsuarioLista(Resource):

    @ns.marshal_list_with(usuario_model)
    def get(self):

        with engine.connect() as connection:

            resultado = connection.execute(
                text('SELECT * FROM usuarios')
            )

            usuarios = []

            for usuario in resultado:

                usuarios.append({
                    'id': usuario.id,
                    'nombre': usuario.nombre,
                    'email': usuario.email
                })

            return usuarios

    @ns.expect(usuario_input_model, validate=True)
    @ns.response(201, 'Usuario creado correctamente')
    @ns.response(400, 'Solicitud inválida')
    def post(self):

        data = request.get_json()

        hashed_password = generate_password_hash(
            data['password']
        )

        with engine.begin() as connection:

            connection.execute(
                text('''
                    INSERT INTO usuarios
                    (id, nombre, email, password)

                    VALUES
                    (:id, :nombre, :email, :password)
                '''),
                {
                    'id': data['id'],
                    'nombre': data['nombre'],
                    'email': data['email'],
                    'password': hashed_password
                }
            )

        return {
            'mensaje': 'Usuario creado correctamente'
        }, 201

@ns.route('/<int:id>')
class Usuario(Resource):

    @ns.marshal_with(usuario_model)
    def get(self, id):

        with engine.connect() as connection:

            resultado = connection.execute(
                text(
                    'SELECT * FROM usuarios WHERE id = :id'
                ),
                {'id': id}
            ).fetchone()

            if resultado:

                return {
                    'id': resultado.id,
                    'nombre': resultado.nombre,
                    'email': resultado.email
                }

            return {
                'error': 'Usuario no encontrado'
            }, 404

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )