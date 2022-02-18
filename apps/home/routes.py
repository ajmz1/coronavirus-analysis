# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from jinja2 import TemplateNotFound

import pandas as pd
import os.path as path

file_path = path.abspath(path.join('routes.py', "../"))
df_full = pd.read_csv(file_path + '\\tests\\full-data.csv')
df_usa = df_full[df_full['location'] == 'United States']


@blueprint.route('/index')
@blueprint.route('/')
def index():
    colNames = ['new_cases', 'new_deaths', 'total_cases', 'total_deaths', 'stringency_index',
                'population']
    data_fetched = df_usa.date.iloc[-1]
    data = [data_fetched]
    return render_template('home/index.html', segment='index', data=data)


@blueprint.route('/<template>')
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
