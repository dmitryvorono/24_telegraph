import os
import json
from flask import Flask, render_template, request, redirect, url_for, make_response, abort
from datetime import date
from transliterate import translit
import re
import uuid
from http import HTTPStatus


app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        article = {'header': request.form['header'],
                   'signature': request.form['signature'],
                   'body': request.form['body'],
                   'unid': str(uuid.uuid4())}
        article_filepath, article['filename'] = generate_unique_article_name(article)
        json_dump(article, article_filepath)
        redirect_to_article = redirect(url_for('render_article', article_name=article['filename']))
        response = make_response(redirect_to_article)
        response.set_cookie(article['unid'], value='1')
        return response
    return render_template('form.html')


@app.route('/<article_name>', methods=['GET', 'POST'])
def render_article(article_name):
    article_filename = 'articles/{0}.json'.format(article_name)
    article = json_load(article_filename)
    if not article:
        abort(HTTPStatus.NOT_FOUND.value)
    can_edit = bool(article['unid'] in request.cookies)
    if can_edit and request.method == 'POST':
        new_article_values = {'header': request.form['header'],
                              'signature': request.form['signature'],
                              'body': request.form['body']}
        article.update(new_article_values)
        json_dump(article, article_filename)
        return redirect(url_for('render_article', article_name=article_name))
    return render_template('article.html', article=article, can_edit=can_edit)


@app.errorhandler(HTTPStatus.NOT_FOUND.value)
def page_not_found(error):
    return render_template('404.html'), HTTPStatus.NOT_FOUND.value


def json_dump(dumping_dict, filepath):
    with open(filepath, 'w') as file_handler:
        json.dump(dumping_dict, file_handler)


def json_load(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)


def generate_unique_article_name(article, length_name=100):
    article_header_latin = translit(article['header'], "ru", reversed=True)
    prepared_article_header_latin = re.sub(' ', '-', re.sub('\W+', ' ', article_header_latin))[:length_name]
    index_article = 1
    current_date = date.today()
    article_filename = '{0}-{1}-{2}-{3}'.format(prepared_article_header_latin, current_date.month, current_date.day, index_article)
    article_filepath = 'articles/{0}.json'.format(article_filename)
    while os.path.exists(article_filepath):
        index_article += 1
        article_filename = '{0}-{1}-{2}-{3}'.format(prepared_article_header_latin, current_date.month, current_date.day, index_article)
        article_filepath = 'articles/{0}.json'.format(article_filename)
    return article_filepath, article_filename


if __name__ == "__main__":
    app.run()
