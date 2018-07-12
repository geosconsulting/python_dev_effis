import pandas as pd

df = pd.DataFrame({'Year': ['2014', '2015'], 'quarter': ['q1', 'q2']})
print(df)

df['period'] = df[['Year', 'quarter']].apply(lambda x: ''.join(x), axis=1)
print(df)