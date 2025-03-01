import joblib
import kagglehub
import logging
import pandas as pd

from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


log_path = Path.cwd() / "logs"  # root folder + 'logs' folder
log_path.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=log_path /'sklearn_model_log_file.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)


df = pd.read_csv("data/data.csv")

X = df.drop(columns=['date_sold_new', 'car_age_sold_new', 'sale_price_used'])
y = df['price_difference_sold_used']

numeric_features = ['hp', 'used_mileage', 'year', 'sale_price_new']
numeric_transformer = StandardScaler()

categorical_features = ['make', 'model', 'fuel', 'gear']
categorical_transformer = OneHotEncoder(drop='first', handle_unknown='ignore')

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())  # Change to SVM or other models as needed
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit the pipeline to the training data
pipeline.fit(X_train, y_train)

# Evaluate the model on the test set
score = pipeline.score(X_test, y_test)
print(f"score: {score:,.2f}")
logging.info(f"sklearn model score : {score:,.2f}")
pipeline_path = 'data/models/sklearn_pipeline.pkl'
joblib.dump(pipeline, pipeline_path)
logging.info(f"Successfully saved sklearn pipline at {pipeline_path}")