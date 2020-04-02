import socket
from datetime import datetime

from flask import Flask

app = Flask(__name__)

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

@app.route("/")
def hello():
    return "Hello from the machine: {}!".format(host_ip)

@app.route("/hostname")
def get_hostname():
    return "Hostname: {}".format(host_name)

@app.route("/datetime")
def get_datetime():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return "DateTime: {}".format(dt_string)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
