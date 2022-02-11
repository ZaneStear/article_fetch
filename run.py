from flask import Flask, render_template, request, redirect

import core

app = Flask(__name__)

column_url = ''  # 专栏url
column_ids = []  # 专栏文章id的list


@app.route("/")
def index():
    """主页"""
    return render_template("index.html")


@app.route("/fetch")
def fetcher_baidu_post_bar():
    """判断抓取的网站"""
    if request.method == "GET":
        web = request.args.get("web")
        url = request.args.get("url")
        if web == "tieba":
            return core.article_baidu_url(url).content
        elif web == "bili":
            return core.article_bili_url(url).content
        elif web == "column":
            global column_url
            column_url = url
            return redirect("/column")
    else:
        return "ERROR METHOD"


@app.route("/column/")
def column():
    """专栏抓取页面"""
    global column_ids
    # 专栏全部文章的id和数量
    column_ids = core.get_column_ids(column_url)
    num = len(column_ids)
    return render_template("column.html", num=num)


@app.route("/column/f")
def f_column():
    """抓取专栏区间"""
    if request.method == "GET":
        # 抓取区间
        min_num = int(request.args.get("min")) - 1
        max_num = int(request.args.get("max")) - 1
        ids = column_ids[min_num:max_num]
        return core.articles_bili_ids(ids).content
    return "ERROR METHOD"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
