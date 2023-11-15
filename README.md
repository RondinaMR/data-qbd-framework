# Experience: Bridging Data Measurement and Ethical Challenges with Extended Data Briefs

Tools related to the paper "Experience: Bridging Data Measurement and Ethical Challenges with Extended Data Briefs".

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
Imbalance(dataset_name='BankMarketing_DB', df=dataframe, sensitive_features, , output_path="analysis/")
```
It is possible to specify the parameter `output_path="output/path/"` in order to save the output csv file in a 
different folder.

## Quality
A call to the `Quality` class constructor will compute the selected standard data quality measures and store the results in a csv file.

```python
from quality import Quality
import pandas as pd
dataframe = pd.read_csv(bank-additional-full.csv,sep=";", na_values=['unknown'])
Quality(dataset_name=f'BankMarketing_DQ', df=dataframe, "analysis/", isurl=False, pretty_name='Bank Marketing')
```