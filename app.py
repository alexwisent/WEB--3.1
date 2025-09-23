from flask import Flask, url_for, request, redirect 
import datetime
app = Flask(__name__)

@app.route("/web")
def web():
    return """<!doctype html>
    	<html>
        	<body>
        		<h1>web-сервер на flask<h1>
                <a href="/author">author</a> <!-- Ссылка на /author -->
        	<body>
        <html>"""

@app.route("/author")
def author():
    name = "Анчугова Софья Алексеевна" # Создание переменной name и присвоение ей значения с ФИО студента
    group = "ФБИ-32"  # Создание переменной group и присвоение ей значения с номером группы
    faculty = "ФБ" # Создание переменной faculty и присвоение ей значения с названием факультета

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/web">web</a> <!-- Ссылка на /web -->
            </body>
        </html>"""

@app.route('/image')
def image():
    path = url_for("static", filename="oak.jpg")
    return '''
<!doctype html> 
<html>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">
    </body>
</html> '''

count=0

@app.route('/counter')
def counter():
    global count
    count+=1
    time = datetime.datetime.today()    # текущую дату и время
    url = request.url                   # IP-адрес клиента
    client_ip = request.remote_addr     # имя хоста веб-сервера

    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Датаивремя: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        ВашIP-адрес: ''' + client_ip + '''<br>
    </body>
</html> '''

@app.route("/info")
def info():
    return redirect("/author")