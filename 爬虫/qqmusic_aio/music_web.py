from flask import *
from flask_pymongo import PyMongo
from config import *

app = Flask(__name__)
app.secret_key = "fjfkjfafeu33842mdfej!@eew"
app.config["MONGO_URI"] = "mongodb://localhost:27017/%s"%MONGO_DB
mongo = PyMongo(app)

@app.route('/',methods=["GET","POST"])
def index():
    if request.method == "GET":
        data = mongo.db.list.find().sort("rank")
        return render_template('index.html',data=data)
    else:
        music = request.form.get("name")
        data_music_name = mongo.db.list.find({"name":music})
        data_music_singer = mongo.db.list.find({"singer":music})
        return render_template('index.html',data_from_name = data_music_name,
                               data_from_singer=data_music_singer,)
if __name__  == "__main__":
    app.run(debug=True)