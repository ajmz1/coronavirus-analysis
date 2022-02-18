import pandas as pd


class DataManager:
    def __init__(self, csv_file_path):
        self.df = pd.read_csv(csv_file_path)
        self.df['date'] = pd.to_datetime(self.df['date'])

    def filter_country(self, country):
        df_country = self.df[self.df['location'] == country]
        return df_country




