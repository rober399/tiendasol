from flask import Flask, flash, render_template, request, session, redirect, url_for
import mysql.connector
from datetime import datetime
from modulos import usuarios_bp
#import bcrypt 

app = Flask(__name__)
# Registrar el blueprint de usuarios
app.register_blueprint(usuarios_bp)

# Función para obtener la conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        db='solunadb'
    )
app.secret_key = 'mysecretkey'
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

if __name__ == '__main__':
    app.run(port=3000, debug=True)