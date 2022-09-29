from flask import Flask, render_template, url_for, flash, request, redirect
from config import *

app = Flask(__name__)
app.secret_key = 'mysecretkey' # para poder usar flash

sesion = True
con_db = get_connection()

#ruta de la pagina principal
@app.route("/salir")
def salir():
	return render_template("login.html")

@app.route("/")
def index():
	return render_template("login.html")

@app.route("/home")
def home():
	if sesion == True:
		print(con_db)
		cur = con_db.cursor()
		cur.execute("SELECT * FROM productos")
		data = cur.fetchall()
		print("----------------------------------------------")
		print(data)
		return render_template("index.html", productos=data)
	else:
		return redirect(url_for('index'))
	#return render_template("index.html")

#ruta de la pagina de registro
@app.route("/registro")
def registro():
	return render_template("registro.html")

#ruta de la pagina de login
@app.route("/login")
def login():
	return render_template("login.html")


#ruta de layaut
@app.route("/layaut")
def layaut():
	print("Hola layut")
	return render_template("layout.html")

@app.route("/registrarusuario", methods=['POST'])
def registrarse():
	if request.method == 'POST':
		correo = request.form['correo']
		contraseña1 = request.form['contraseña1']
		contraseña2 = request.form['contraseña2']
		print(correo, contraseña1, contraseña2)
		if (contraseña1==contraseña2):
			cur = con_db.cursor()
			cur.execute("INSERT INTO usuarios (email, password) VALUES (%s, %s)", (correo, contraseña1))
			con_db.commit()
			flash("registro de usuarios")
			return redirect(url_for('login'))
		else:
			flash("Las contraseñas no coinciden")
			return redirect(url_for('registro'))

@app.route("/ingresar", methods=['GET', 'POST'])
def ingresars():
	if request.method == 'POST':
		email = request.form['nombre']
		contraseñaf = request.form['contraseña']
		cur = con_db.cursor()
		cur.execute("SELECT * FROM usuarios WHERE email = %s AND password = %s", (email, contraseñaf))
		data = cur.fetchall()
		print("_-----------------------------------")
		print(data)
		if len(data) > 0:
			print("si hay datos")
			return redirect(url_for('home'))
		else:
			flash("Datos no encontrados")
			return redirect(url_for('login'))

@app.route("/guardar_producto", methods=['POST'])
def guardar_personas():
	if request.method == 'POST':
		nombre = request.form['nombre']
		valor = request.form['valor']
		cantidad = request.form['cantidad']
		cur = con_db.cursor()
		cur.execute("INSERT INTO productos (nombre_producto, valor_producto, cantidad) VALUES (%s, %s, %s)", (nombre, valor, cantidad))
		con_db.commit()
		cur.execute("SELECT * FROM productos")
		data = cur.fetchall()
		print("----------------------------------------------")
		print(data)
		return render_template("index.html", productos=data)
		#return redirect(url_for('index'))

@app.route("/listar_personas")
def listar_personas():
	cur = con_db.cursor()
	cur.execute("SELECT * FROM personas")
	data = cur.fetchall()
	print(data)
	return render_template("ver.html", personas=data)

#Actualizar persona
@app.route("/update/<id>", methods=['POST'])
def get_producto(id):
	nombre = request.form['nombre']
	valor = request.form['valor']
	cantidad = request.form['cantidad']
	cur = con_db.cursor()
	if nombre and valor and cantidad:
		sql = """
			UPDATE productos
			SET nombre_producto = %s,
			valor_producto = %s,
			cantidad = %s
			WHERE idproducto = %s
		"""
		cur.execute(sql, (nombre, valor, cantidad, id))
		con_db.commit()
		flash("Producto actualizado correctamente", "success")
		return redirect(url_for('home'))
	else:
		return 'Error en la consulta'

#eliminar persona
@app.route("/delete/<id>")
def delete_producto(id):
	cur = con_db.cursor()
	cur.execute("DELETE FROM productos WHERE idproducto=%s", (id))
	con_db.commit()
	flash("Se elimino el producto correctamente", "warning")
	return redirect(url_for('home'))

#ruta de error 404
@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html'), 404

# funciones
def create_table():
	cur = con_db.cursor()
	cur.execute("""
			CREATE TABLE IF NOT EXISTS productos(
				idproducto serial  NOT NULL,
				nombre_producto VARCHAR(100),
				valor_producto INTEGER,
				cantidad INTEGER,
				CONSTRAINT pk_productos_id PRIMARY KEY (idproducto));
		""")
	con_db.commit()

def create_table_usuarios():
	cur = con_db.cursor()
	cur.execute("""
			CREATE TABLE IF NOT EXISTS usuarios(
				idusuario serial  NOT NULL,
				email VARCHAR(50),
				password VARCHAR(50),
				CONSTRAINT pk_usuarios_id PRIMARY KEY (idusuario));
		""")
	con_db.commit()

if __name__ == '__main__':
	create_table()
	create_table_usuarios()
	app.run(debug=True, port=5000)