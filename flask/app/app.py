#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template,request

#Flaskオブジェクトの生成
app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    user_name = request.args.get("name")
    return render_template("index.html",name=user_name)


if __name__ == "__main__":
    app.run(debug=True)
