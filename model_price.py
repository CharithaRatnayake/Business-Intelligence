import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv('resources/dataset.csv' ,index_col='Date' ,parse_dates=True)
print('Shape of data',df.shape)
df.head()
df

df['Price'].plot(figsize=(49,1))
plt.show()