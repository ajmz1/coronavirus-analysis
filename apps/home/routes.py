# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from jinja2 import TemplateNotFound

from apps.data_functions import DataManager
from pathlib import Path

csv_file_path = str(Path().resolve()) + '\\data\\full-data.csv'
a = DataManager(csv_file_path)




@blueprint.route('/index')
@blueprint.route('/')
def index():
    # Call for the usa data columns that will be used in plotting
    data = a.usa_data
    return render_template('home/index.html', segment='index', data=data, title='COVID-19 Home')


@blueprint.route('/<template>')
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'

        segment = get_segment(request)

        return render_template("home/" + template, segment=segment, data=a.compute_detailed_analysis(a.df_usa))

    except TemplateNotFound:
        return render_template("home/page-404.html"), 404

    except:
        return render_template("home/page-500.html"), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
