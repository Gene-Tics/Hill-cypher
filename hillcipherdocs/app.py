from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def documentation():
    return render_template('documentation.html')

if __name__ == '__main__':
    app.run(debug=True)
