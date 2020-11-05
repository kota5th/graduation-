import sqlite3
from flask import Flask, render_template, request,redirect,session
from datetime import datetime
app = Flask(__name__) 
UPLOAD_FOLDER = '/static/img'


app.secret_key = "sunaebe"

@app.route("/")
def index():
    return render_template('top.html')

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
    if "user_id" in session:
        return render_template("/post.html")
    else:
        return render_template('login.html')
    
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
    if "user_id" in session:
        return render_template("/map.html")
    else:
        return render_template('login.html')
    
@app.route("/map",methods=["POST"])
def map_post():
    map = request.form.get("map")
    player_name1 = request.form.get("player_name1")
    kill_1 =  request.form.get("kill_1")
    death1 =  request.form.get("death1")
    times1 =  request.form.get("times1")
    defence1 =  request.form.get("defence1")
    win1 =  request.form.get("win1")
    player_name2 = request.form.get("player_name2")
    kill_2 =  request.form.get("kill_2")
    death2 =  request.form.get("death2")
    times2 =  request.form.get("times2")
    defence2 =  request.form.get("defence2")
    win2 =  request.form.get("win2")
    player_name3 = request.form.get("player_name3")
    kill_3 =  request.form.get("kill_3")
    death3 =  request.form.get("death3")
    times3 =  request.form.get("times3")
    defence3 =  request.form.get("defence3")
    win3 =  request.form.get("win3")
    player_name4 = request.form.get("player_name4")
    kill_4 =  request.form.get("kill_4")
    death4 =  request.form.get("death4")
    times4 =  request.form.get("times4")
    defence4 =  request.form.get("defence4")
    win4 =  request.form.get("win4")
    player_name5 = request.form.get("player_name5")
    kill_5 =  request.form.get("kill_5")
    death5 =  request.form.get("death5")
    times5 =  request.form.get("times5")
    defence5 =  request.form.get("defence5")
    win5 =  request.form.get("win5")
    user_id = session["user_id"]

    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    c.execute("insert into map values (null,?,?,?,?,?,?,?,?)",(user_id,player_name1,kill_1,death1,times1,defence1,win1,map))
    c.execute("insert into map values (null,?,?,?,?,?,?,?,?)",(user_id,player_name2,kill_2,death2,times2,defence2,win2,map))
    c.execute("insert into map values (null,?,?,?,?,?,?,?,?)",(user_id,player_name3,kill_3,death3,times3,defence3,win3,map))
    c.execute("insert into map values (null,?,?,?,?,?,?,?,?)",(user_id,player_name4,kill_4,death4,times4,defence4,win4,map))
    c.execute("insert into map values (null,?,?,?,?,?,?,?,?)",(user_id,player_name5,kill_5,death5,times5,defence5,win5,map))
    conn.commit()
    c.close()
    
    return redirect("/grade")

# GRADE
@app.route("/grade")
def grade_list():
    if "user_id" in session:
        user_id = session["user_id"]
        conn = sqlite3.connect("flasktest.db")
        c = conn.cursor()
            # taskテーブルからすべての値を取得する

        c.execute("select name, kill, death, point_time, defense, win, kill / death as kd, kill + death as approach from map where user_id = user_id" )
        grade_list = []
        for row in c.fetchall():
            
        
            grade_list.append({"name":row[0], "kill": row[1], "death": row[2], "point_time": row[3], "defense": row[4],  "win": row[5], "kd":row[6], "approach": row[7]})

        c.close()
        print(grade_list)
        return render_template("grade.html",grade_list = grade_list)
    else:
        return render_template('login.html')

@app.route("/search", methods=["get"])
def search_ent():
        return render_template("search.html")

    


# 検索
@app.route("/search", methods=["post"])
def search_post():
        return redirect("/search_result")

# 検索結果
@app.route("/search_result", methods=["post"])
def search_entry():
    
        team = request.form.get("team")
        user_id = session["user_id"]
        map = request.form.get("map")
        print(map)
        print(team)
        if map == 0:
            conn = sqlite3.connect("flasktest.db")
            c = conn.cursor()
            c.execute("select user_id from map where name = ?", (team,))
            task = c.fetchone()
            c.execute("select name, avg(kill), avg(death), avg(point_time), avg(defense), avg(win), avg(lose), avg(kill / death) as kd, avg(kill + death) as approach from map where user_id = ? and name = ?", (user_id, team))
            grade_list = []
            for row in c.fetchall():   
                
                grade_list.append({"name":row[0], "kill": row[1], "death": row[2], "point_time": row[3], "defense": row[4],  "win": row[5], "lose": row[6], "kd":row[7], "approach": row[8]})

            c.close()
        
        else:
            
            conn = sqlite3.connect("flasktest.db")
            c = conn.cursor()
                # taskテーブルからすべての値を取得する
            c.execute("select user_id from map where name = ?", (team,))
            task = c.fetchone()
            c.execute("select name, avg(kill), avg(death), avg(point_time), avg(defense), avg(win), avg(kill / death) as kd, avg(kill + death) as approach from map where user_id = ? and name = ? and map = ?", (user_id, team, map))
            grade_list = []
            for row in c.fetchall():   
                    
                grade_list.append({"name":row[0], "kill": row[1], "death": row[2], "point_time": row[3], "defense": row[4],  "win": row[5], "kd":row[6], "approach": row[7]})

            c.close()
        print(grade_list)
        print(task)
        print(user_id)
        return render_template("grade.html", grade_list = grade_list)


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
        c.execute("select id, task, user_name,date from friend_recruitment order by id desc")
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