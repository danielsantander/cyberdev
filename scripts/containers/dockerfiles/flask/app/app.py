import random
from flask import Flask, Response, render_template
from typing import List

APP_HOST='0.0.0.0'
APP_PORT=8000
DEBUG=True

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

# Example endpoint
@app.route('/home')
def home():
    # Define the data you want to send
    page_title = "My Awesome Website"
    user_name = "Jane Doe"
    fruits_list = ["Apple", "Banana", "Cherry"]
    user_info = {
        'age': 30,
        'location': 'San Antonio, TX'
    }

    # Pass the data to the template as keyword arguments
    return render_template(
        'home.html',
        title=page_title,
        name=user_name,
        fruits=fruits_list,
        info=user_info
    )


if __name__ == '__main__':
    # Important: host='0.0.0.0' makes the app accessible externally within the Docker network
    # Set debug true to allow real-time code changes without restarting the container, but remember to set it to False in production for security reasons!
    app.run(host=APP_HOST, port=APP_PORT, debug=DEBUG)
