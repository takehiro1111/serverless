#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template,request

#Flaskオブジェクトの生成
app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    name = request.args.get("name") # /index?name="hoge"でクエリパラメータの"?name="の値を取得している。
    return render_template("index.html",key=name) # keyは、index.htmlの{{key}}とリンクしている.
  


if __name__ == "__main__":
    app.run(debug=True)
