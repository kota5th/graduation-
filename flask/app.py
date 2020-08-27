# 記事投稿python



@app.route("/●●●",methods=["GET"])
def add_get():
    return render_template("/●●●.html")
# post通信はデーターを暗号化送信 情報の登録、送信に使う
# 送信したときにDBnotaskリスト に追加されるようにつくるよー
# add.htmlのvalue 送信ボタンが押されることで下記のルーティング発動
@app.route("/●●●",methods=["POST"])
def ●●●():
    # request.form[パラメーター名(htmlの変数名)]代入する変数名は何でよい
    # DBに接続する前にrequestする
    # HTML.入力フォームから値を取得してAPP.PY変数に格納
    ●●● = request.form["●●●"］
    conn = sqlite3.connect("flasktest.db")
    c = conn.cursor()
    # DBにデータを追加したい場合はINSERT INTOやで
    # (左値はID（AI）になるので最大値に＋１追加出来るNULL）
    # (右側は書き込まれる内容がふめいなので？で対応)
    # 変数名taskはタプルで記述する
    c.execute("insert into task values (null,?)",(task,))
    conn.commit()
    c.close()
    return redirect("/●●●")　　※リダイレクトしたいページ
