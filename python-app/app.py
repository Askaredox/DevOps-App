from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origin": "*"}}) # this part is to let any browser know that have CORS permision


@app.route('/') # address to make the call, i.e. http://localhost:5000/
def todo_good():
    return 'Hello World of Rest Api!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True) # The flask app is running in localhost of container and on port 5000
