# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from jinja2 import TemplateNotFound

from apps.data_functions import DataManager
from pathlib import Path
import json
import numpy as np

csv_file_path = str(Path().resolve()) + '\\data\\full-data.csv'
a = DataManager(csv_file_path)


@blueprint.route('/index')
@blueprint.route('/')
def index():
    # This is the point where we load in data
    df_usa = a.filter_country('United States')

    # Create "as of" date
    date_asof = df_usa['date'].iloc[-1].strftime('%d-%B-%Y').split('-')
    date_asof = date_asof[0] + ' ' + date_asof[1] + ' ' + date_asof[2]

    # Create the date column
    date = df_usa['date'].dt.strftime('%b-%y').to_numpy()
    date_dense = df_usa['date'].dt.strftime('%d-%b-%y').to_numpy()

    # Populate the data list
    data = [date_asof,
            date,
            df_usa.total_cases,
            df_usa.total_deaths,
            df_usa.new_cases_smoothed,
            df_usa.new_deaths_smoothed,
            date_dense,
            df_usa.icu_patients,
            df_usa.hosp_patients,
            df_usa.total_vaccinations,
            df_usa.total_boosters,
            df_usa.people_vaccinated,
            df_usa.new_vaccinations_smoothed,
            df_usa.people_fully_vaccinated
            ]
    return render_template('home/index.html', segment='index', data=data, title='COVID-19 Home')


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
