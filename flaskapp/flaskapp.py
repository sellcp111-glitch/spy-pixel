from flask import Flask, send_file, request, render_template_string
import datetime
import urllib.request

app = Flask(__name__)

# you must fill this in or it will not work...
path_to_directory = "FILL THIS IN"

# Serve a default page. This function is not required. Serving up a spy.gif for the homepage.
@app.route('/')
def my_function():
    if path_to_directory == "FILL THIS IN":
        content = "you need to fill in the path_to_directory variable in flaskapp.py"
        return render_template_string('<pre>{{ content }}</pre>', content=content)
    spy_meme = path_to_directory+"/spy-pixel/flaskapp/spy.gif"
    return send_file(spy_meme, mimetype="image/gif")

@app.route('/logging')
def display_text_file():
    if path_to_directory == "FILL THIS IN":
        content = "you need to fill in the path_to_directory variable in flaskapp.py"
        return render_template_string('<pre>{{ content }}</pre>', content=content)
    try:
        with open((path_to_directory+'/spy-pixel/spy_pixel_logs.txt'), 'r') as file:
            content = file.read()
    except FileNotFoundError:
        content = "File not found."
    except Exception as e:
        content = f"An error occurred: {e}"
    
    return render_template_string('<pre>{{ content }}</pre>', content=content)

@app.route('/image')
def my_spy_pixel_no_id():
    if path_to_directory == "FILL THIS IN":
        content = "you need to fill in the path_to_directory variable in flaskapp.py"
        return render_template_string('<pre>{{ content }}</pre>', content=content)
    # File path and name for 1 x 1 pixel. Must be an absolute path to pixel.
    filename = path_to_directory+"/spy-pixel/flaskapp/pixel.png"
    # Log the User-Agent String.
    user_agent = request.headers.get('User-Agent')
    # Get the current time of request and format time into readable format.
    current_time = datetime.datetime.now()
    timestamp = datetime.datetime.strftime(current_time, "%Y-%m-%d %H:%M:%S")

    # Log the IP address of requester.
    get_ip = request.remote_addr

    # Lookup Geolocation of IP Address.
    with urllib.request.urlopen("http://ip-api.com/json/"+ get_ip) as url:
        data = url.read().decode()

    # Add User-Agent, Timestamp, and IP Address + Geolocation information to dictionary.
    log_entry = f"Email Opened:\nTimestamp: {timestamp}\nUser Agent: {user_agent}\nIP Address Data: {data}\n"

    # Write log to hardcoded path. Must be an absolute path to the log file.
    with open((path_to_directory+'/spy-pixel/spy_pixel_logs.txt'), 'r') as file:
        f.write(log_entry)

    # Serve a transparent pixel image when navigating to .../image URL. "image/png" displays the image in PNG format.
    return send_file(filename, mimetype="image/png")

@app.route('/image/<id>')
def my_spy_pixel(id):
    if path_to_directory == "FILL THIS IN":
        content = "you need to fill in the path_to_directory variable in flaskapp.py"
        return render_template_string('<pre>{{ content }}</pre>', content=content)
    # File path and name for 1 x 1 pixel. Must be an absolute path to pixel.
    filename = path_to_directory+"/spy-pixel/flaskapp/pixel.png"
    # Log the User-Agent String.
    user_agent = request.headers.get('User-Agent')
    # Get the current time of request and format time into readable format.
    current_time = datetime.datetime.now()
    timestamp = datetime.datetime.strftime(current_time, "%Y-%m-%d %H:%M:%S")

    # Log the IP address of requester.
    get_ip = request.remote_addr

    # Lookup Geolocation of IP Address.
    with urllib.request.urlopen("http://ip-api.com/json/"+ get_ip) as url:
        data = url.read().decode()

    # Add User-Agent, Timestamp, and IP Address + Geolocation information to dictionary.
    log_entry = f"Email {id} Opened:\nTimestamp: {timestamp}\nUser Agent: {user_agent}\nIP Address Data: {data}\n"

    # Write log to hardcoded path. Must be an absolute path to the log file.
    with open((path_to_directory+'/spy-pixel/spy_pixel_logs.txt'), 'r') as file:
        f.write(log_entry)

    # Serve a transparent pixel image when navigating to .../image URL. "image/png" displays the image in PNG format.
    return send_file(filename, mimetype="image/png")


if __name__ == '__main__':
    app.run()
