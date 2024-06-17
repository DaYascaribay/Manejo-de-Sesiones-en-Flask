from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256

#se usa el codigo hash para encriptar contraseñas, se basa en que una palabra pasa por el algoritmo hash que se convertira 
#en una serie de numeros, letras y caracteres y no se podra volver a la palabra original


app = Flask(__name__) # se crea una instancia de clase Flask y le dice a Flask que utilice el nombre 
#del módulo actual como el nombre de la aplicación
app.secret_key = '1234' #cifra los datos de sesion


#se guarda en un diccionario, simulando una BD
users = {}
print(users)


@app.route('/') #manejara las solicitudes HTTP que lleguen a una ruta especifica en este caso ruta raiz
def index():
    user = session.get('user') #asigna el valor asociado con la clave 'user' a la variable user. 
    #Si no hay un usuario almacenado en la sesión, user será None

    if user: #verifica si la variable user contiene algún valor que no sea None, vacío, cero o 
        #cualquier otro valor que evalúe como falso en Python
        return f"Bienvenido, {user} <br> <a href='/logout'>CERRAR SESIÓN</a>" #aparecera con una sesion activa
    return "BIENVENIDO AL APARTADO DE REGISTRAR USUARIOS <p> <br><a href='/registrar'>REGISTRARSE</a> <p><a href='/login'>INICIAR SESIÓN</a>"
    #aparecera cuando se ejecute la aplicacion es decir sera la pagina principal



@app.route('/registrar', methods=['GET', 'POST'])#asigna una ruta especifica a través de un navegador web (método GET)
#cuando se envíe datos sera a través de un formulario HTML (método POST).

#GET: mostrar un formulario html al usuario 

#POST: procesar los datos enviados por el usuario a través de ese formulario
def register():
    if request.method == 'POST': #verifica si la solicitud HTTP recibida por el servidor es del tipo POST. El atributo method 
        #de este objeto devuelve el método HTTP utilizado en la solicitud actual

        username = request.form['username'] #asigna el valor del campo de formulario 'username' a la variable username, request.form 
        #contiene los datos del formulario enviado con la solicitud POST

        #username = request.form['password']
        password = pbkdf2_sha256.hash(request.form['password'])#toma la contraseña proporcionada por el usuario, la pasa a través 
        #del algoritmo hash, y asigna el resultado (el hash de la contraseña) a la variable password

        session['user'] = username #establece el nombre de usuario en la sesión del usuario, lo que permite que la aplicación 
        #rastree la identidad del usuario mientras navega por el sitio web.

        users[username] = password #guarda la contraseña hasheada en el diccionario users, asociándola con el nombre de usuario correspondiente.

        print(users)#imprime el usuario registrado por consola 

        return redirect(url_for('index'))#redirige al usuario a la página principal de tu aplicación después de completar la acción deseada.
    return render_template('registrar.html')#asocia a la ruta registrar el render o la pagina HTML REGISTRAR



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Verifica si el usuario existe en el diccionario users
        if username in users:
            # Verifica si la contraseña coincide con la contraseña almacenada, se usa verify por que la contraseña esta hasheada
            if pbkdf2_sha256.verify(password, users[username]):
                session['user'] = username
                return redirect(url_for('index'))
            else:
                return "Nombre de usuario o contraseña incorrectos<br><a href='/'>REGRESAR</a>"
        else:
            return "Usuario no encontrado<br><a href='/'>REGRESAR</a>"
    return render_template('login.html')#asocia a la ruta login el render o la pagina HTML LOGIN



@app.route('/logout')
def logout():
    session.pop('user', None)#elimina el valor asociado con la clave 'user' del objeto de sesión.
    return redirect(url_for('index'))


if __name__ == '__main__': #se ejecutará únicamente si el script se está ejecutando directamente, 
    #es decir, si es el punto de entrada principal del programa.
    app.run(debug=True, port=8080)#inicia el servidor web Flask en modo de depuración, 
    #lo que proporciona información detallada sobre cualquier error, y lo ejecuta en el puerto 8080.