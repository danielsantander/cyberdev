import random
from flask import Flask, render_template, url_for, request
from typing import List

APP_HOST='0.0.0.0'
APP_PORT=8000
DEBUG=True

app = Flask(__name__)

@app.route('/')
def hello_world():
    # Example of generating a URL to a static file
    static_file_url = url_for('static', filename='img/background.jpg')
    return render_template('index.html')

@app.route('/polls/')
@app.route('/polls/<poll_type>/')
def polls(poll_type:str='batman'):
    username = request.args.get('username', 'Guest')
    poll_data = [
        {
            "question": "Favorite programming language?",
            "answers": ["Python", "Java", "C++"],
        },
        {
            "question": "Best web framework?",
            "answers": ["Flask", "Django", "FastAPI"],
        }
    ]

    if poll_type == 'batman':
        poll_data = [
            {
                "question": "Who is your favorite Batman actor?",
                "answers": ["Michael Keaton", "Christian Bale", "Ben Affleck", "Robert Pattinson"],
            },
            {
                "question": "Which Batman movie is the best?",
                "answers": ["Batman (1989)", "The Dark Knight (2008)", "Batman v Superman (2016)", "The Batman (2022)"],
            }
        ]
    return render_template('polls.html', poll_type=poll_type, polls=poll_data)



if __name__ == '__main__':
    # Important: host='0.0.0.0' makes the app accessible externally within the Docker network
    # Set debug true to allow real-time code changes without restarting the container, but remember to set it to False in production for security reasons!
    app.run(host=APP_HOST, port=APP_PORT, debug=DEBUG)
