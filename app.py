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


# ログイン機能
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        if "user_id" in session:
          return redirect("/map")
        else:
          return render_template('login.html')

    else:
        # ブラウザから送られてきたデータを受け取る
        name = request.form.get("name")
        password = request.form.get("password")

        # ブラウザから送られてきた name ,password を userテーブルに一致するレコードが
        # 存在するかを判定する。レコードが存在するとuser_idに整数が代入、存在しなければ nullが入る
        conn = sqlite3.connect('flasktest.db')
        c = conn.cursor()
        c.execute("select id from users where name = ? and pass = ?", (name, password) )
        user_id = c.fetchone()
        conn.close()
        # DBから取得してきたuser_id、ここの時点ではタプル型
        print(type(user_id))
        # user_id が NULL(PythonではNone)じゃなければログイン成功
        if user_id is None:
            # ログイン失敗すると、ログイン画面に戻す
            return render_template("login.html")
        else:
            session['user_id'] = user_id[0]
            return render_template("map.html")



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

    c.execute("select name, kill, death, point_time, defense, win, lose, kill / death as kd from map")
    grade_list = []
    for row in c.fetchall():
        
    
        grade_list.append({"name":row[0], "kill": row[1], "death": row[2], "point_time": row[3], "defense": row[4],  "win": row[5], "lose": row[6], "kd":f'{row[7]:.2f}'})

    c.close()
    print(grade_list)
    return render_template("grade.html",grade_list = grade_list)











# flaskアプリを動かすための記述
if __name__ == "__main__":
    app.run(debug = True)