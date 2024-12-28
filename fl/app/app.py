from flask import Flask,render_template,request
from app.models.models import OnegaiContent
from app.models.database import db_session
from datetime import datetime

app = Flask(__name__)

@app.route("/",methods=["GET"])
@app.route("/index",methods=["GET", "POST"])
def index():
    name = request.args.get("name")
    records = OnegaiContent.query.all()
    return render_template("index.html",name=name,records=records)

@app.route("/add",methods=["post"])
def add():
    title = request.form["title"]
    body = request.form["body"]
    content = OnegaiContent(title,body,datetime.now())
    db_session.add(content)
    db_session.commit()
    return index()

@app.route("/delete",methods=["post"])
def delete():
    id_list = request.form.getlist("delete")
    for id in id_list:
        content = OnegaiContent.query.filter_by(id=id).first()
        db_session.delete(content)
    db_session.commit()
    return index()

@app.route("/update",methods=["post"])
def update():
    content = OnegaiContent.query.filter_by(id=request.form["update"]).first()
    content.title = request.form["title"]
    content.body = request.form["body"]
    db_session.commit()
    return index()

if __name__ == "__main__":
    app.run(debug=True)
