import time

import requests
from flask import Flask, request
from flask_restx import Api, Resource, fields
from sqlalchemy import create_engine, text

app = Flask(__name__)

api = Api(
    app,
    version='1.0',
    title='Microservicio Pedido',
    description='API REST para pedidos',
    doc='/swagger'
)

ns = api.namespace(
    'pedidos',
    description='Operaciones de pedidos'
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
        CREATE TABLE IF NOT EXISTS pedidos (
            id INT PRIMARY KEY,
            usuario_id INT,
            producto VARCHAR(100),
            cantidad INT,
            estado VARCHAR(100)
        )
    '''))

pedido_model = api.model('Pedido', {
    'id': fields.Integer(
        required=True,
        description='ID del pedido'
    ),

    'usuario_id': fields.Integer(
        required=True,
        description='ID del usuario'
    ),

    'producto': fields.String(
        required=True,
        description='Producto solicitado'
    ),

    'cantidad': fields.Integer(
        required=True,
        description='Cantidad solicitada'
    ),

    'estado': fields.String(
        required=True,
        description='Estado del pedido'
    )
})

@ns.route('')
class PedidoLista(Resource):

    @ns.marshal_list_with(pedido_model)
    def get(self):

        with engine.connect() as connection:

            resultado = connection.execute(
                text('SELECT * FROM pedidos')
            )

            pedidos = []

            for pedido in resultado:

                pedidos.append({
                    'id': pedido.id,
                    'usuario_id': pedido.usuario_id,
                    'producto': pedido.producto,
                    'cantidad': pedido.cantidad,
                    'estado': pedido.estado
                })

            return pedidos

    @ns.expect(pedido_model, validate=True)
    @ns.response(201, 'Pedido creado correctamente')
    @ns.response(404, 'El usuario no existe')
    @ns.response(
        500,
        'No se pudo conectar al microservicio Usuario'
    )
    def post(self):

        data = request.get_json()

        usuario_id = data['usuario_id']

        try:

            respuesta = requests.get(
                f'http://usuario-service:5000/usuarios/{usuario_id}',
                timeout=5
            )

        except requests.RequestException:

            return {
                'error': (
                    'No se pudo conectar '
                    'al microservicio Usuario'
                )
            }, 500

        if respuesta.status_code != 200:

            return {
                'error': 'El usuario no existe'
            }, 404

        with engine.begin() as connection:

            connection.execute(
                text('''
                    INSERT INTO pedidos
                    (id, usuario_id, producto, cantidad, estado)

                    VALUES
                    (:id, :usuario_id, :producto,
                     :cantidad, :estado)
                '''),
                {
                    'id': data['id'],
                    'usuario_id': usuario_id,
                    'producto': data['producto'],
                    'cantidad': data['cantidad'],
                    'estado': data['estado']
                }
            )

        return {
            'mensaje': 'Pedido creado correctamente'
        }, 201

@ns.route('/<int:id>')
class Pedido(Resource):

    @ns.marshal_with(pedido_model)
    def get(self, id):

        with engine.connect() as connection:

            resultado = connection.execute(
                text(
                    'SELECT * FROM pedidos WHERE id = :id'
                ),
                {'id': id}
            ).fetchone()

            if resultado:

                return {
                    'id': resultado.id,
                    'usuario_id': resultado.usuario_id,
                    'producto': resultado.producto,
                    'cantidad': resultado.cantidad,
                    'estado': resultado.estado
                }

            return {
                'error': 'Pedido no encontrado'
            }, 404

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )