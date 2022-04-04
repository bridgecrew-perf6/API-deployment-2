import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression





#open the csv
df = pd.read_csv('preprocessing/clean_data_nadia.csv')

#drop the column except ..
df.drop(df.columns.difference(["Property type", "Living area", "Post code", "Bedrooms", "Price", "Swimming pool", "Garden"]), 1, inplace=True)

#get rid of infinite values
df.replace([np.inf, -np.inf], np.nan, inplace=True)
#get rid null values
df.fillna(0, inplace=True)

X = df.drop(['Price'], axis =1)
y = df['Price']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
print(X_train.shape)

regressor = LinearRegression()
regressor = regressor.fit(X_train, y_train)

   