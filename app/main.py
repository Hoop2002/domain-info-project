from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "FLASK APP"



if __name__ == '__main__':
    app.run(port=8000, 
            debug=True)