import sqlite3
from flask import Flask, render_template, request,redirect,session
app = Flask(__name__) 

@app.route("/")
def index():
    return "hello"

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





# 記事投稿
@app.route("/post",methods=["GET"])
def add_get():
    return render_template("/post.html")
@app.route("/post",methods=["POST"])
def add_post():
    task = request.form.get("task")
    user_id = session["user_id"]
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("insert into published values (null,?,?)",(task,user_id))
    conn.commit()
    c.close()
    
    return redirect("/")

# リスト表
@app.route("/list")
def task_list():
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
        
    c.execute("select published, from *")
        # 取得したデータ扱うには一旦、変数にしなければいけない
        # 空の変数を作成する
    task_list = []
    for row in c.fetchall():
        
        task_list.append({"id" : row[0], "task" : row[1]})
    c.close()
    print(task_list)
    return render_template("task_list.html",task_list = task_list)










# flaskアプリを動かすための記述
if __name__ == "__main__":
    app.run(debug = True)