import os
# splite3をimportする
import sqlite3
# flaskをimportしてflaskを使えるようにする
from flask import Flask , render_template , request , redirect , session
# appにFlaskを定義して使えるようにしています。Flask クラスのインスタンスを作って、 app という変数に代入しています。
app = Flask(__name__)
app.secret_key="sunaebe"


@app.route("/")
def index():
  return "Hello"

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

@app.route("/map", methods=["GET", "POST"])
def map():
  if request.method == "GET":
        if "user_id" in session:
          return redirect("/map")
        else:
          return render_template('map.html')

if __name__ == "__main__":
  app.run(debug=True)