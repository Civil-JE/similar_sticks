import csv
from flask import current_app


class CsvDataService:
    # Read the raw data out of the CSV file
    def load_raw_data(self, filename):
        with open(filename, mode='r') as data_file:
            data_reader = csv.reader(data_file, delimiter=',')
            next(data_reader)  # Skip over the header line
            raw_data = [data for data in data_reader]
            data_file.close()
        return raw_data
