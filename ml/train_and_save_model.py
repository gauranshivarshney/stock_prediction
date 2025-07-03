import joblib
from sklearn.linear_model import LinearRegression  
model = LinearRegression()

X = [[1, 2, 3, 4]]
y = [100]
model.fit(X, y)
joblib.dump(model, 'model.pkl')