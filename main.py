from analysis import analyze
from flask import Flask, jsonify, request

# from werkzeug import secure_filename

app = Flask(__name__)


@app.route('/upload', methods = ['POST'])
def hello_world():
    filename = upload_file()
    return analyze()


def upload_file():
    f = request.files['file']
    f.save("groceries_final.csv")
    return f.filename
  
if __name__ == '__main__':
   app.run(port=80)