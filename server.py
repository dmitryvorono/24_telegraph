import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method== 'POST':
        article = {'header': request.form['header'],
                   'signature': request.form['signature'],
                   'body': request.form['body']}
        article_filename = ''.join(['articles/', article['header'], '.json'])
        json_dump(article, article_filename)
        return redirect(url_for('render_article', article_name = article['header']))
    return render_template('form.html')


@app.route('/<article_name>')
def render_article(article_name):
    article = json_load(''.join(['articles/', article_name, '.json']))
    if not article:
        return 'Not found'
    return render_template('article.html', article=article)


def json_dump(dumping_dict, filepath):
    with open(filepath, 'w') as file_handler:
        json.dump(dumping_dict, file_handler)


def json_load(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)


if __name__ == "__main__":
    app.run()
