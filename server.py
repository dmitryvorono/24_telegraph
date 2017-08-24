import os
import json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method== 'POST':
        article = {'header': request.form['header'],
                   'signature': request.form['signature'],
                   'body': request.form['body']}
        json_dump(article, ''.join(['articles/', article['header'], '.json']))
    return render_template('form.html')


def json_dump(dumping_dict, filepath):
    with open(filepath, 'w') as file_handler:
        json.dump(dumping_dict, file_handler)


if __name__ == "__main__":
    app.run()
