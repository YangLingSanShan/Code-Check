import os
import subprocess
import webbrowser
import time
import requests

current_directory = os.getcwd()

manage_py_path = os.path.join(current_directory, 'manage.py')

if not os.path.isfile(manage_py_path):
    print(f"Error: {manage_py_path} does not exist.")
    exit(1)

command = f"python {manage_py_path} runserver"

process = subprocess.Popen(command, shell=True)
url = "http://127.0.0.1:8000/"
max_attempts = 10
for attempt in range(max_attempts):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            break
    except requests.ConnectionError:
        pass
    time.sleep(1)

webbrowser.open(url)

process.wait()

