import csv


class CsvDataService:
    def __init__(self, filename):
        self.filename = filename
        self.raw_stick_data = None
        self.formatted_stick_data = list()
        self.unique_years = set()
        self.unique_makes = set()
        self.unique_models = set()
        self.unique_curves = set()
        self.unique_kickpoints = set()
        self.unique_flexes = set()

    def load_current_data(self):
        self._wipe_old_data()
        self.update_raw_data()
        formatted_data, split_data = self.update_formatted_data()
        self.update_unique_values(split_data)
        return formatted_data

    # Read and save the raw data out of the CSV file
    def update_raw_data(self):
        with open(self.filename, mode='r') as data_file:
            sticks_data = csv.reader(data_file, delimiter=',')
            next(sticks_data)  # Skip over the header line
            self.raw_stick_data = [stick for stick in sticks_data]
            data_file.close()
        return self.raw_stick_data

    # Format the raw data so that it's easier to lookup. TODO: Add IDs or find a way to index?
    def update_formatted_data(self):
        split_data = {'years': list(), 'makes': list(), 'models': list(),
                      'curves': list(), 'kickpoints': list(), 'flexes': list()}
        for stick in self.raw_stick_data:
            formatted_stick = {
                    'year': stick[0],
                    'make': stick[1],
                    'model': stick[2],
                    'curves': stick[3].strip('[]').split(', '),
                    'kickpoint': stick[4],
                    'flexes': stick[5].strip('[]').split(', '),
                    'search_string': f"{stick[0]} {stick[1]} {stick[2]}"
                }
            self.formatted_stick_data.append(formatted_stick)

            split_data['years'].append(formatted_stick['year'])
            split_data['makes'].append(formatted_stick['make'])
            split_data['models'].append(formatted_stick['model'])
            split_data['curves'].extend(formatted_stick['curves'])
            split_data['kickpoints'].append(formatted_stick['kickpoint'])
            split_data['flexes'].extend(formatted_stick['flexes'])
        return self.formatted_stick_data, split_data

    # Unique values will be used to populate the search parameters
    def update_unique_values(self, stick_data):
        self.unique_years.update(stick_data['years'])
        self.unique_makes.update(stick_data['makes'])
        self.unique_models.update(stick_data['models'])
        self.unique_curves.update(stick_data['curves'])
        self.unique_kickpoints.update(stick_data['kickpoints'])
        self.unique_flexes.update(stick_data['flexes'])

        return {
            'years': self.unique_years,
            'makes': self.unique_makes,
            'models': self.unique_models,
            'curves': self.unique_curves,
            'kickpoints': self.unique_kickpoints,
            'flexes': self.unique_flexes
        }

    def get_unique_values(self):
        return {
            'years': list(self.unique_years),
            'makes': list(self.unique_makes),
            'models': list(self.unique_models),
            'curves': list(self.unique_curves),
            'kickpoints': list(self.unique_kickpoints),
            'flexes': list(self.unique_flexes)
        }

    def _wipe_old_data(self):
        self.raw_stick_data = None
        self.formatted_stick_data = list()
        self.unique_years = set()
        self.unique_makes = set()
        self.unique_models = set()
        self.unique_curves = set()
        self.unique_kickpoints = set()
        self.unique_flexes = set()
