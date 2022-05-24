from flask import Flask, request
from flask_cors import CORS

from server.services.rhyme import check_rhyme


app = Flask(__name__)

CORS(app)

@app.route('/')
def hello():
    return 'Hello, World! - this is an API'

@app.route('/rhyme', methods=['GET','POST'])
def rhyme():
    data = request.get_json()
    poem = data["poem"]
    # print(poem)
    return {"poem":check_rhyme(poem)}
