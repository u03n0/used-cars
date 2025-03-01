import joblib
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


df = pd.read_csv("data/clean/autoscout24-germany-dataset.csv")


X = df.drop(columns=['price'])
y = df['price']

numeric_features = ['hp', 'mileage', 'year']
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
    ('regressor', LinearRegression())
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit the pipeline to the training data
pipeline.fit(X_train, y_train)

# Evaluate the model on the test set
score = pipeline.score(X_test, y_test)
print(f"score: {score:,.2f}")
logging.info(f"sklearn model score : {score:,.2f}")
pipeline_dir = Path.cwd() / "models" # root folder + 'models' folder
pipeline_dir.mkdir(parents=True, exist_ok=True)
pipeline_full_path = pipeline_dir / 'sklearn_pipeline.pkl'
joblib.dump(pipeline, pipeline_full_path)
logging.info(f"Successfully saved sklearn pipline at {pipeline_full_path}")