import os
import json
import random
from flask import Flask, render_template, request, redirect, url_for, make_response


app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method== 'POST':
        article = {'header': request.form['header'],
                   'signature': request.form['signature'],
                   'body': request.form['body'],
                   'unid': generate_unid()}
        article_filename = ''.join(['articles/', article['header'], '.json'])
        json_dump(article, article_filename)
        redirect_to_article = redirect(url_for('render_article', article_name = article['header']))
        response = make_response(redirect_to_article)
        response.set_cookie(article['unid'], value='1')
        return response
    return render_template('form.html')


@app.route('/<article_name>', methods=['GET', 'POST'])
def render_article(article_name):
    article_filename = ''.join(['articles/', article_name, '.json'])
    article = json_load(article_filename)
    if not article:
        return 'Not found'
    can_edit = True if article['unid'] in request.cookies else False
    if can_edit and request.method == 'POST':
        new_article_values = {'header': request.form['header'],
                              'signature': request.form['signature'],
                              'body': request.form['body']}
        article.update(new_article_values)
        json_dump(article, article_filename)
        return redirect(url_for('render_article', article_name = article_name))
    return render_template('article.html', article=article, can_edit=can_edit)


def json_dump(dumping_dict, filepath):
    with open(filepath, 'w') as file_handler:
        json.dump(dumping_dict, file_handler)


def json_load(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)


def generate_unid(length_unid):
    count_digits = 16
    return ''.join([str(hex(random.randrange(count_digits)))[2] for x in range(length_unid)])


if __name__ == "__main__":
    app.run()
