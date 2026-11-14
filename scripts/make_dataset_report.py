import pandas as pd
df = pd.read_csv('data/training_reports.csv')
print('Rows:', len(df))
print('Synthetic rows:', int(df['synthetic'].sum()))
print(pd.crosstab(df.language, df.category))
