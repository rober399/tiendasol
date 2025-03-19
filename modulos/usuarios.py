from flask import Flask, Blueprint,flash, render_template, request, session, redirect, url_for
from datetime import datetime
from app import get_db_connection
from . import usuarios_bp



app = Flask(__name__)
usuarios_bp = Blueprint('usuarios', __name__)


#from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import datetime

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/AgregarAdmin', methods=["GET", "POST"])
def AgregarAdmin():
    if request.method == 'POST':
        try:
            usuario = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            rol = request.form.get('role')
            fecha_actual = datetime.now()  # Genera la fecha actual

            if not all([usuario, email, password, rol]):
                return "Todos los campos son obligatorios", 400

            # Obtener la conexión a la base de datos
            miConexion = get_db_connection()
            cur = miConexion.cursor()
            cur.execute(
                "INSERT INTO usuarios (nombre_usuario, email, password, fecha_registro, rol) VALUES (%s, %s, %s, %s, %s)",
                (usuario, email, password, fecha_actual, rol)
            )
            miConexion.commit()
            cur.close()
            miConexion.close()  # Cerrar la conexión

            print("Datos Registrados")
            flash('Usuario agregado exitosamente', 'success')  # Mensaje de éxito
            return redirect(url_for('usuarios.Listausuario'))  # Redirige a la lista de usuarios
        except Exception as e:
            print(f"Error en la base de datos: {e}")
            if 'miConexion' in locals():
                miConexion.rollback()
                miConexion.close()  # Asegurarse de cerrar la conexión
            return "Error interno del servidor", 500

    # Si es un GET, simplemente renderiza el formulario
    return render_template('Registrousuario.html')

@usuarios_bp.route('/Listausuario', methods=["GET", "POST"])
def Listausuario():
     # Obtener la conexión a la base de datos
    miConexion = get_db_connection()
    cur = miConexion.cursor()

    cur.execute("SELECT id_usuario, nombre_usuario, email, fecha_registro, rol FROM usuarios")
    datos = cur.fetchall()
    print (datos)
    return render_template('Listausuario.html', registros = datos)


if __name__ == '__main__':
    app.run(port=3000, debug=True)