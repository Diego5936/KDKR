from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # This tells Flask to render index.html from your templates folder
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
