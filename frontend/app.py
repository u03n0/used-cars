import streamlit as st
import joblib
import pandas as pd


pipeline = joblib.load('data/models/pipeline.pkl')
df = pd.read_csv("data/clean/data.csv")


car_models = {
    'chevrolet': ['silverado'],
    'honda': ['civic'],
    'nissan': ['altima', 'f-150'],
    'ford': ['f-150', 'mustang'],
    'toyota': ['camry'],
    'bmw': ['320i'],
    'audi': ['a3']
}

fuel_types = {
    'chevrolet': ['gasoline', 'diesel'],
    'honda': ['gasoline', 'hybrid'],
    'nissan': ['gasoline', 'electric'],
    'ford': ['gasoline', 'electric', 'hybrid'],
    'toyota': ['gasoline', 'electric'],
    'bmw': ['gasoline', 'diesel'],
    'audi': ['gasoline', 'electric']
}

gear_types = {
    'chevrolet': ['automatic', 'manual'],
    'honda': ['automatic', 'manual'],
    'nissan': ['automatic', 'manual'],
    'ford': ['automatic'],
    'toyota': ['automatic', 'manual'],
    'bmw': ['automatic', 'manual'],
    'audi': ['automatic', 'manual']
}

hp_range = {
    'chevrolet': (100, 400),
    'honda': (80, 300),
    'nissan': (100, 350),
    'ford': (150, 450),
    'toyota': (100, 350),
    'bmw': (150, 500),
    'audi': (150, 400)
}

year_range = {
    'chevrolet': (2019, 2022),
    'honda': (2011, 2022),
    'nissan': (2011, 2022),
    'ford': (2011, 2022),
    'toyota': (2011, 2022),
    'bmw': (2011, 2022),
    'audi': (2011, 2022)
}

st.title('Used Car Price Prediction')

car_make = st.selectbox('Car Make', list(car_models.keys()))
car_model = st.selectbox('Car Model', car_models[car_make])

year_min, year_max = year_range[car_make]
year = st.number_input('Year', min_value=year_min, max_value=year_max, step=1)

hp_min, hp_max = hp_range[car_make]
hp = st.number_input('Horsepower', min_value=hp_min, max_value=hp_max, step=1)

mileage = st.number_input('Mileage (in miles)', min_value=1000, max_value=300000, step=1000)

fuel = st.selectbox('Fuel Type', fuel_types[car_make])

gear = st.selectbox('Gear Type', gear_types[car_make])

sale_price_new = df[(df['make'] == car_make) &
                    (df['model'] == car_model) &
                    (df['year'] == year)]['sale_price_new']
if not sale_price_new.empty:
    sale_price_new = sale_price_new.mean()
    st.write(sale_price_new)
else:
    st.error("No data available for the selected car make, model and year.")
    sale_price_new = 0

data = {
    'make': car_make,
    'model': car_model,
    'year': year,
    'hp': hp,
    'used_mileage': mileage,
    'fuel': fuel,
    'gear': gear,
    'sale_price_new': sale_price_new
}

input_data = pd.DataFrame([data])

if st.button('Predict Used Car Price Range'):
    predicted_price_diff = pipeline.predict(input_data)[0]
    
    # Calculate the used car price range
    predicted_used_price = sale_price_new + predicted_price_diff
    price_range_low = predicted_used_price * 0.9  # Lower bound (10% less)
    price_range_high = predicted_used_price * 1.1  # Upper bound (10% more)
    
    # Display the results
    st.subheader(f'Predicted Used Car Price: €{predicted_used_price:,.2f}')
    st.write(f'Estimated Price Range: €{price_range_low:,.2f} - €{price_range_high:,.2f}')
# Decision-making logic
    buy_threshold = 5000  # For example, only buy cars worth above €5,000
    max_price_diff = 1000  # Maximum acceptable price difference (e.g., no more than €5,000 loss)
    max_car_age = 7  # Maximum acceptable car age (e.g., avoid cars older than 15 years)
    
    # Decision rule: if predicted price is above threshold and within acceptable price difference
    if predicted_used_price > buy_threshold and predicted_price_diff > -max_price_diff and (2023 - year) <= max_car_age:
        st.success(f"Decision: The salesman should buy this car!")
        st.success(f"predicted_price_diff {predicted_price_diff}")
    else:
        st.error(f"Decision: The salesman should not buy this car.")