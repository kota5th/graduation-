import sqlite3
from flask import Flask, render_template, request,redirect
app = Flask(__name__) 


# 会員登録 
@app.route("/regist",methods=["GET"])
def regist_get():
    return render_template("regist.html")

@app.route("/regist",methods = ["POST"])
def regist_post():
    name = request.form.get("name")
    password = request.form.get("password")

    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("insert into users values(null,?,?)",(name, password))
    conn.commit()
    c.close()

    return "会員登録完了致しました"





# 掲示板サイト
@app.








# flaskアプリを動かすための記述
if __name__ == "__main__":
    app.run(debug = True)