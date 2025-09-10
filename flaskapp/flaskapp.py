from flask import Flask, send_file, request, render_template_string
import datetime
import urllib.request
import os

# Instance Flask au niveau global
app = Flask(__name__)

# Chemin relatif : repo racine
base_dir = os.path.dirname(os.path.abspath(__file__))
path_to_directory = base_dir

@app.route('/')
def home():
    spy_meme = os.path.join(path_to_directory, "spy-pixel", "flaskapp", "spy.gif")
    if not os.path.exists(spy_meme):
        return "Le fichier spy.gif est introuvable."
    return send_file(spy_meme, mimetype="image/gif")

@app.route('/logging')
def logs():
    log_file = os.path.join(path_to_directory, "spy-pixel", "spy_pixel_logs.txt")
    if not os.path.exists(log_file):
        return "Le fichier de logs est introuvable."
    with open(log_file, 'r') as f:
        content = f.read()
    return render_template_string('<pre>{{ content }}</pre>', content=content)

@app.route('/image')
@app.route('/image/<id>')
def pixel(id=None):
    filename = os.path.join(path_to_directory, "spy-pixel", "flaskapp", "pixel.png")
    log_file = os.path.join(path_to_directory, "spy-pixel", "spy_pixel_logs.txt")

    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    get_ip = request.remote_addr

    # Géolocalisation IP
    try:
        with urllib.request.urlopen(f"http://ip-api.com/json/{get_ip}") as url:
            data = url.read().decode()
    except:
        data = "Impossible de récupérer la géolocalisation."

    log_entry = f"Email {id if id else 'Opened'}:\nTimestamp: {timestamp}\nUser Agent: {user_agent}\nIP Address Data: {data}\n\n"
    with open(log_file, 'a') as f:
        f.write(log_entry)

    return send_file(filename, mimetype="image/png")

# Exécution locale
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
