from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from controller.controllerCarro import listaCarros, registrarCarro, updateCarro, detallesdelCarro, recibeActualizarCarro, stringAleatorio 
import mysql.connector
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps 

# --------------------------------------------
# CONFIGURACIÓN FLASK CON RUTAS ABSOLUTAS
# --------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),  
    static_folder=os.path.join(BASE_DIR, 'static')       
)

app.secret_key = 'clave_secreta_123'

# --------------------------------------------
# CONEXIÓN A BD DE LOGIN
# --------------------------------------------
def connection_login():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="flask_login"
    )

# --------------------------------------------
# RUTAS PÚBLICAS
# --------------------------------------------
@app.route('/', methods=['GET'])
def index():
    """Redirige automáticamente la ruta raíz al formulario de login."""
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connection_login()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM user WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
            return redirect(url_for('login'))

    return render_template('public/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = connection_login()
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE username=%s", (username,))
        existing_user = cur.fetchone()
        if existing_user:
            flash('El usuario ya existe', 'warning')
            cur.close()
            conn.close()
            return redirect(url_for('register'))

        cur.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cur.close()
        conn.close()

        flash('Usuario registrado correctamente', 'success')
        return redirect(url_for('login'))

    return render_template('public/register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

# --------------------------------------------
# DECORADOR LOGIN REQUIRED
# --------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión primero.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --------------------------------------------
# CRUD DE CARROS (REQUIERE SESIÓN)
# --------------------------------------------
@app.route('/inicio', methods=['GET', 'POST'])
@login_required
def inicio():
    try:
        data = listaCarros()
        return render_template('public/layout.html', miData=data)
    except Exception as e:
        # 🔑 FIX: En lugar de forzar logout, mostramos la página con datos vacíos y un error.
        print(f"Error al cargar lista de carros (BD Carros): {e}")
        flash('Error grave de conexión con la Base de Datos de Carros. No se pudieron cargar los datos.', 'danger')
        # Retornamos el template, permitiendo que el usuario permanezca logueado.
        return render_template('public/layout.html', miData=[]) 

@app.route('/registrar-carro', methods=['GET', 'POST'])
@login_required
def addCarro():
    return render_template('public/acciones/add.html')

@app.route('/carro', methods=['POST'])
@login_required
def formAddCarro():
    marca = request.form['marca']
    modelo = request.form['modelo']
    year = request.form['year']
    color = request.form['color']
    puertas = request.form['puertas']
    favorito = request.form['favorito']

    if 'foto' in request.files and request.files['foto'].filename != '':
        file = request.files['foto']
        nuevoNombreFile = recibeFoto(file) 
        resultData = registrarCarro(marca, modelo, year, color, puertas, favorito, nuevoNombreFile)
        
        if resultData == 1:
            flash('El Registro fue un éxito', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('No se pudo registrar en la base de datos', 'danger')
            return redirect(url_for('inicio')) 
    else:
        flash('Debe cargar una foto', 'warning')
        return redirect(url_for('addCarro')) 

@app.route('/form-update-carro/<string:id>', methods=['GET', 'POST'])
@login_required
def formViewUpdate(id):
    if request.method == 'GET':
        resultData = updateCarro(id)
        if resultData:
            return render_template('public/acciones/update.html', dataInfo=resultData)
        else:
            flash('No existe el carro solicitado', 'danger')
            return redirect(url_for('inicio'))
    return redirect(url_for('inicio'))

@app.route('/ver-detalles-del-carro/<int:idCarro>', methods=['GET', 'POST'])
@login_required
def viewDetalleCarro(idCarro):
    if request.method == 'GET':
        resultData = detallesdelCarro(idCarro)
        if resultData:
            return render_template('public/acciones/view.html', infoCarro=resultData, msg='Detalles del Carro', tipo=1)
        else:
            flash('No existe el Carro solicitado', 'danger')
            return redirect(url_for('inicio'))
    return redirect(url_for('inicio'))

@app.route('/actualizar-carro/<string:idCarro>', methods=['POST'])
@login_required
def formActualizarCarro(idCarro):
    marca = request.form['marca']
    modelo = request.form['modelo']
    year = request.form['year']
    color = request.form['color']
    puertas = request.form['puertas']
    favorito = request.form['favorito']

    foto_carro = None
    if 'foto' in request.files and request.files['foto'].filename != '':
        file = request.files['foto']
        foto_carro = recibeFoto(file) 

    resultData = recibeActualizarCarro(marca, modelo, year, color, puertas, favorito, foto_carro, idCarro)
    
    if resultData == 1:
        flash('Datos del carro actualizados', 'success')
        return redirect(url_for('inicio'))
    else:
        flash('No se pudo actualizar el carro', 'danger')
        return redirect(url_for('inicio'))

@app.route('/borrar-carro', methods=['POST'])
@login_required
def formViewBorrarCarro():
    idCarro = request.form['id']
    nombreFoto = request.form['nombreFoto']
    resultData = eliminarCarro(idCarro, nombreFoto) 
    
    return jsonify([1] if resultData == 1 else [0])

# --------------------------------------------
# FUNCIONES AUXILIARES (DEFINIDAS LOCALMENTE)
# --------------------------------------------
def eliminarCarro(idCarro='', nombreFoto=''):
    from controller.controllerCarro import connectionBD 
    
    conexion_MySQLdb = connectionBD()
    cur = conexion_MySQLdb.cursor(dictionary=True)
    cur.execute('DELETE FROM carros WHERE id=%s', (idCarro,))
    conexion_MySQLdb.commit()
    resultado_eliminar = cur.rowcount

    basepath = os.path.dirname(__file__)
    url_File = os.path.join(basepath, 'static/assets/fotos_carros', nombreFoto)
    if os.path.exists(url_File):
        os.remove(url_File)

    return resultado_eliminar

def recibeFoto(file):
    basepath = os.path.dirname(__file__)
    filename = secure_filename(file.filename)
    extension = os.path.splitext(filename)[1]
    nuevoNombreFile = stringAleatorio() + extension 
    upload_path = os.path.join(basepath, 'static/assets/fotos_carros', nuevoNombreFile)
    file.save(upload_path)
    return nuevoNombreFile

# --------------------------------------------
# MANEJO DE ERROR 404
# --------------------------------------------
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('login')) 

# --------------------------------------------
# EJECUCIÓN DEL SERVIDOR
# --------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=8000)