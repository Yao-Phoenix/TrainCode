#!/usr/bin/env python3
from flask import Flask, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def hidden_email(email):
    parts = email.split('@')
    parts[0] = '*****'
    return '@'.join(parts)

app.add_template_filter(hidden_email)

@app.route('/')
def index():
    teacher = {
            'name': 'Aiden',
            'email': 'loujin@simplecloud.cn'
            }

    course = {
            'name': 'Python Basic',
            'teacher': teacher,
            'user_count': 5348,
            'price': 199.0,
            'lab': None,
            'is_private': False,
            'is_menber_course': True,
            'tags': ['Python', 'big data', 'Linux']
            }
    return render_template('index.html', course=course)
