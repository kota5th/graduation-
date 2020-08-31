import sqlite3
from flask import Flask, render_template, request,redirect,session
from datetime import datetime

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


# map 戦歴記入ページ
@app.route("/map",methods=["GET"])
def map_get():
    return render_template("/map.html")
@app.route("/map",methods=["POST"])
def map_post():
    map = request.form.get("map")
    player_name1 = request.form.get("player_name1")
    kill_1 =  request.form.get("kill_1")
    death1 =  request.form.get("death1")
    times1 =  request.form.get("times1")
    defence1 =  request.form.get("defence1")
    win1 =  request.form.get("win1")
    lose1 =  request.form.get("lose1")

    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("insert into map values (null,?,?,?,?,?,?,?,?)",(player_name1,kill_1,death1,times1,defence1,win1,lose1,map))
    conn.commit()
    c.close()
    
    return redirect("/grade")

# GRADE
@app.route("/grade")
def grade_list():
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
        # taskテーブルからすべての値を取得する

    c.execute("select id , kill / death as kd from map ")
    kd = c.fetchone()
    c.execute("select id, name, kill, death, point_time, defense,  win, lose from map")
    grade_list = []
    for row in c.fetchall():
    
        grade_list.append({"id": row[0], "name":row[1], "kill": row[2], "death": row[3], "point-time": row[4], "defense": row[5],  "win": row[6], "lose": row[7]})
    c.close()
    print(grade_list)
    print(kd[1])
    return render_template("grade.html",grade_list = grade_list)


# 仲間募集掲示板
@app.route("/friends", methods=["GET"])
def friend_get():
    return render_template("/friends.html")
@app.route("/friends", methods=["POST"])
def friend_post():
    dt_now = datetime.now().strftime('%m-%d %H:%M:%S')
    print(dt_now)
    task = request.form.get("task")
    user_name = request.form.get("user_name")
    # user_id = session["user_id"]
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("insert into friend_recruitment values (null,?,?,?)",(task,user_name,dt_now,))
    conn.commit()
    c.close()
    
    return redirect("/list")


@app.route("/list")
def task_list():
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("select id, task, user_name,date from friend_recruitment")
    task_list = []
    for row in c.fetchall():
        task_list.append({"id":row[0] , "task":row[1] , "user_name":row[2] , "date":row[3]})
    return render_template("task_list.html", task_list = task_list)


@app.route("/edit/<int:id>")
def edit(id):
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("select task from friend_recruitment where id = ?",(id,))
    task = c.fetchone()
    c.close()

    if task is not None:
        task = task[0]
    else:
        return "見つかりません"

    task = task[0]
    item = {"id":id,"task":task}
    return render_template("edit.html" , task = item )

@app.route("/edit", methods=["POST"])
def update_task():
    item_id = request.form.get("task_id")
    item_id = int(item_id)
    task = request.form.get("task")
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("update friend_recruitment set task = ? where id = ?",(task,item_id))
    conn.commit()
    c.close()

    return redirect("/list")



@app.route("/del/<int:id>")
def del_task(id):
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("delete from friend_recruitment where id = ?",(id,))
    conn.commit()
    c.close()
    return redirect("/list")




# flaskアプリを動かすための記述
if __name__ == "__main__":
    app.run(debug = True)