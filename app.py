from flask import Flask, flash, render_template, request, session, redirect, url_for
import mysql.connector
from datetime import datetime
#import bcrypt 

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Función para obtener la conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        db='solunadb'
    )

# Página de inicio
@app.route('/')
def home():
    return render_template('index.html')


#login
@app.route('/login', methods=["GET", "POST"])
def login():
    Nombres = request.form['username'].strip()
    password = request.form['password'].strip()
    
    miConexion = get_db_connection()
    cur = miConexion.cursor()

    # Usa una consulta parametrizada
    query = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND password = %s"
    cur.execute(query, (Nombres, password))
    user = cur.fetchall()

    cur.close()
    miConexion.close()

    # Verifica si la lista de usuarios está vacía
    if not user:  # Esto verifica si la lista está vacía
        success_message = 'Contraseña o usuario incorrecto'
        flash(success_message)
        return render_template('index.html')
    else:
        # Cambia a 'username' para acceder correctamente al nombre del usuario
        session['username'] = Nombres
        return render_template('Registrousuario.html')


@app.route('/profile') #Ruta que muestra mensaje de bienvenida
def profile():
    if 'username' in session:
        return f'Bienvenido, {session["username"]}! <a href="/logout">Cerrar sesión</a>'
    return redirect(url_for('login'))

@app.route('/logout') #Destruir inicio de sesion
def logout():
    session.pop('username', None)  # Eliminar el nombre de usuario de la sesión
    return render_template(('index.html'))



# Registrar Usuario
@app.route('/AgregarAdmin', methods=["GET", "POST"])
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
            return render_template('Registrousuario.html')  # Redirige a una página de éxito
        except Exception as e:
            print(f"Error en la base de datos: {e}")
            if 'miConexion' in locals():
                miConexion.rollback()
                miConexion.close()  # Asegurarse de cerrar la conexión
            return "Error interno del servidor", 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)