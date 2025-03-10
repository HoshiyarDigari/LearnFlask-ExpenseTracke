from flask import Flask, render_template
from datetime import datetime
#flask app 
app = Flask(__name__)
#route for home page
@app.route('/')
def homepage():
    return render_template('index.html', current_time= datetime.now())

if __name__ == '__main__':
    app.run(debug=True)
    