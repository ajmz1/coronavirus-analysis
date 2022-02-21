import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
from plotly.subplots import make_subplots
import numpy as np
import json
import datetime
from json import JSONEncoder


class DateTimeEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return  obj.isoformat()





class DataManager:
    def __init__(self, csv_file_path):
        self.df = pd.read_csv(csv_file_path)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df_usa = self.filter_country('United States')
        self.usa_data = self.index_data_manager(self.df_usa)

    def filter_country(self, country):
        df_country = self.df[self.df['location'] == country]
        return df_country

    def index_data_manager(self, df_usa):
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
        return data

    def compute_detailed_analysis(self, df):
        data = self.plot_detailed_analysis(df)
        return data


    def plot_detailed_analysis(self, df):
        # This works with notepad stuff
        date = df.date.dt.strftime('%d-%b-%y')
        y = df.new_cases_smoothed.values.tolist()
        y = json.dumps(y)
        data = [date, y]


        return data


