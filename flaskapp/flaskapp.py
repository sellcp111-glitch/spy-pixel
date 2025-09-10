from flask import Flask, send_file, request, render_template_string
import datetime
import urllib.request
import os

app = Flask(__name__)

# Remplis ici le chemin absolu vers le dossier contenant "spy-pixel"
path_to_directory = "/absolute/path/to/your/folder"

# Page d'accueil
@app.route('/')
def my_function():
    if not os.path.exists(path_to_directory):
        content = "Vous devez remplir la variable path_to_directory dans flaskapp.py"
        return render_template_string('<pre>{{ content }}</pre>', content=content)
    
    spy_meme = os.path.join(path_to_directory, "spy-pixel", "flaskapp", "spy.gif")
    return send_file(spy_meme, mimetype="image/gif")

# Affichage des logs
@app.route('/logging')
def display_text_file():
    log_file = os.path.join(path_to_directory, "spy-pixel", "spy_pixel_logs.txt")
    if not os.path.exists(log_file):
        content = "Fichier de logs introuvable."
        return render_template_string('<pre>{{ content }}</pre>', content=content)
    
    with open(log_file, 'r') as file:
        content = file.read()
    return render_template_string('<pre>{{ content }}</pre>', content=content)

# Pixel sans ID
@app.route('/image')
def my_spy_pixel_no_id():
    return log_and_send_pixel("")

# Pixel avec ID
@app.route('/image/<id>')
def my_spy_pixel(id):
    return log_and_send_pixel(id)

# Fonction pour log et renvoyer le pixel
def log_and_send_pixel(id):
    if not os.path.exists(path_to_directory):
        content = "Vous devez remplir la variable path_to_directory dans flaskapp.py"
        return render_template_string('<pre>{{ content }}</pre>', content=content)
    
    filename = os.path.join(path_to_directory, "spy-pixel", "flaskapp", "pixel.png")
    log_file = os.path.join(path_to_directory, "spy-pixel", "spy_pixel_logs.txt")

    user_agent = request.headers.get('User-Agent')
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    get_ip = request.remote_addr

    # Géolocalisation IP
    try:
        with urllib.request.urlopen(f"http://ip-api.com/json/{get_ip}") as url:
            data = url.read().decode()
    except:
        data = "Impossible de récupérer la géolocalisation."

    log_entry = f"Email {id if id else 'Opened'}:\nTimestamp: {current_time}\nUser Agent: {user_agent}\nIP Address Data: {data}\n\n"

    # Écriture du log (création du fichier si inexistant)
    with open(log_file, 'a') as file:
        file.write(log_entry)

    return send_file(filename, mimetype="image/png")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
