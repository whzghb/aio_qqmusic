from flask import *
from flask_pymongo import PyMongo
from config import *
from search_music import *

app = Flask(__name__)
# app.secret_key = "fjfkjfafeu33842mdfej!@eew"
app.config["MONGO_URI"] = "mongodb://localhost:27017/%s"%MONGO_DB
mongo = PyMongo(app)

@app.route('/',methods=["GET","POST"])
def index():
    if request.method == "GET":
        data = mongo.db.list.find().sort("rank")
        return render_template('index.html',data=data)
    else:
        keyword = request.form.get("name")
        print(keyword)
        keyword = quote_plus(keyword.strip())
        # data_music_name = mongo.db.list.find({"name":music})
        # data_music_singer = mongo.db.list.find({"singer":music})
        get_music = GetMusic(keyword, headers)
        get_music.get_url()
        all_song = get_music.json_parse()
        del get_music
        return render_template('index.html',all_song = all_song)
if __name__  == "__main__":
    app.run(debug=True)