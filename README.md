# data-qbd-framework

Tools related to the paper "TBC".

The analysis is based on two main calculation scripts:
- quality.py: calculation of standard data quality metrics (Com-I-1-DevA,Com-I-5,Acc-I-4,Con-I-3,Con-I-2-DevB,Con-I-4-DevC)
- imbalance.py: imbalance measure of sensitive features based on heterogeneity indices (Gini,Shannon,Simpson,I.I.R.)

## Imbalance
A call to the `Imbalance` class constructor will compute the imbalance metrics and store the results in a csv file.

```python
from imbalance import Imbalance
import pandas as pd
sensitive_features = ['job', 'education', 'marital', 'y']
dataframe = pd.read_csv(bank-additional-full.csv,sep=";", na_values=['unknown'])
Imbalance(dataset_name='BankMarketing', df=dataframe, sensitive_features)
```
It is possible to specify the parameter `output_path="output/path/"` in order to save the output csv file in a 
different folder.