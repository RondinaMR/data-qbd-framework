# from collections import Counter
import pandas as pd
import numpy as np
from prettytable import PrettyTable
import os


class Imbalance:
    def __init__(self, dataset_name, df, names, output_path=''):
        self._df = df
        self._names = names
        self._frequencies = {}
        self._results = {}
        self._dataset_name = dataset_name
        self._output_path = output_path
        for feature_name in names:
            self._frequencies[feature_name] = self._df[feature_name].value_counts(normalize=True, dropna=True)
            self._results[feature_name] = self.calc_single_feature(feature_name)
        self.print()
        self.save()

    def gini(self, feature_name):
        # frequencies = feature.value_counts(normalize=True)
        m = len(self._frequencies[feature_name])  # number of classes
        if m > 1:
            sumsquare = 0
            for f in self._frequencies[feature_name]:
                sumsquare += f ** 2
            ginival = (m / (m - 1)) * (1 - sumsquare)
        else:
            ginival = np.nan
        return ginival

    def shannon(self, feature_name):
        # frequencies = feature.value_counts(normalize=True)
        m = len(self._frequencies[feature_name])
        if m > 1:
            logsum = 0
            for f in self._frequencies[feature_name]:
                # when fi = 0 – we resort to the notable limit: lim x→0 xlnx = 0
                if f != 0:
                    logsum += f * np.log(f)
            shannonval = -(1 / np.log(m)) * logsum
        else:
            shannonval = np.nan
        return shannonval

    def simpson(self, feature_name):
        # frequencies = feature.value_counts(normalize=True)
        m = len(self._frequencies[feature_name])
        sumsquare = 0
        if m > 1:
            for f in self._frequencies[feature_name]:
                sumsquare += f ** 2
            simpsonval = (1 / (m - 1)) * ((1 / sumsquare) - 1)
        else:
            simpsonval = np.nan
        return simpsonval

    def imbalance_ratio(self, feature_name):
        # frequencies = feature.value_counts(normalize=True)
        imbalanceval = self._frequencies[feature_name].min() / self._frequencies[feature_name].max()
        return imbalanceval

    def calc_single_feature(self, feature_name):
        # feature = self._df[feature_name]
        metrics = {
            "gini": self.gini(feature_name),
            "shannon": self.shannon(feature_name),
            "simpson": self.simpson(feature_name),
            "imbalance_ratio": self.imbalance_ratio(feature_name),
        }
        return metrics

    def frequencies(self, feature_name='all_features_printing'):
        if feature_name=='all_features_printing':
            for name in self._names:
                print(self._frequencies[name])
        else:
            print(self._frequencies[feature_name])

    def print(self):
        print("\n", f'*** {self._dataset_name} ***', "\n")
        my_table = PrettyTable()
        my_table.field_names = ["Feature", "Gini", "Shannon", "Simpson", "I.I.R."]
        for feature_name in self._names:
            my_table.add_row([feature_name, f"{self._results[feature_name]['gini']:.2f}",
                              f"{self._results[feature_name]['shannon']:.2f}",
                              f"{self._results[feature_name]['simpson']:.2f}",
                              f"{self._results[feature_name]['imbalance_ratio']:.2f}"])
        print(my_table)
        # print('Relative frequencies:')
        # print(self._frequencies)
        # print(
        #     f'Gini: {self.gini():.2} - Shannon: {self.shannon():.2} - Simpson: {self.simpson():.2} - IIR: {self.imbalance_ratio():.2}',
        #     "\n")
        return

    def save(self):
        if self._output_path != '':
            if not os.path.exists(self._output_path):
                os.makedirs(self._output_path)
        data = {'Feature': [], 'Gini': [], 'Shannon': [], 'Simpson': [], 'I.I.R.': []}
        for feature_name in self._names:
            data['Feature'].append(feature_name)
            data['Gini'].append(round(self._results[feature_name]['gini'], 2))
            data['Shannon'].append(round(self._results[feature_name]['shannon'], 2))
            data['Simpson'].append(round(self._results[feature_name]['simpson'], 2))
            data['I.I.R.'].append(round(self._results[feature_name]['imbalance_ratio'], 2))
        df = pd.DataFrame(data)
        df.to_csv(f'{self._output_path}{self._dataset_name}.csv', index=False)
        return
