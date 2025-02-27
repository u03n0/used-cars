import streamlit as st
import joblib
import pandas as pd
from datetime import date


# Load pipeline and dataframe
pipeline = joblib.load('data/models/pipeline.pkl')
df = pd.read_csv("data/clean/data.csv")


st.title(f'Used Car Price Prediction')
user_options = ["Sell Vehicle", "Buy Vehicle for Inventory"]
user = st.pills("What would you like to do?", user_options, selection_mode="single")



if user:
    if user == "Buy Vehicle for Inventory":
        commission_rate = st.slider("What is your commission rate?", 0.01, .20, .08)
        st.write(f"Your commission rate is {commission_rate}%")

        profit_margin = st.slider("What is your minimum profit margin?", 1000, 10000, 7000)
        st.write("Profit margin: ", profit_margin)

    makes = df['make'].unique()
    current_year = date.today().year
    car_make = st.selectbox('Car Make',makes)
    car_model = st.selectbox('Car Model', df[df['make'] == car_make]['model'].unique().tolist())

    car_years = df[(df['make'] == car_make) & (df['model'] == car_model)]['year'].unique().tolist()
    year_min =  min(car_years)
    year_max = max(car_years)
    year = st.number_input('Year', min_value=year_min, max_value=year_max, step=1)
    hp_range = df[(df['make'] == car_make) & (df['model'] == car_model)]['hp'].unique().tolist()
    hp_min =  min(hp_range)
    hp_max = max(hp_range)
    hp = st.number_input('Horsepower', min_value=hp_min, max_value=hp_max)

    mileage = st.number_input('Mileage (in miles)', min_value=5000, max_value=500000, step=1000)

    fuel = st.selectbox('Fuel Type', df[(df['make'] == car_make) & (df['model'] == car_model)]['fuel'].unique().tolist())

    gear = st.selectbox('Gear Type', df[(df['make'] == car_make) & (df['model'] == car_model)]['gear'].unique().tolist())

    sale_price_new = df[(df['make'] == car_make) &
                        (df['model'] == car_model) &
                        (df['year'] == year)]['sale_price_new']
    if not sale_price_new.empty:
        sale_price_new = sale_price_new.mean()
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
        if predicted_price_diff > 0:
            st.success(f"Predicted price difference: +€{predicted_price_diff:,.2f}")
        elif predicted_price_diff < 0:
            st.error(f"Predicted price difference: -€{-1 * predicted_price_diff:,.2f}")
        st.write(f"Price brand new  : €{sale_price_new:,.2f}")
        # Calculate the used car price range
        predicted_used_price = sale_price_new + predicted_price_diff
        price_range_low = predicted_used_price * 0.9  # Lower bound (10% less)
        price_range_high = predicted_used_price * 1.1  # Upper bound (10% more)
        
        # Display the results
        st.subheader(f'Predicted Used Car Price: €{predicted_used_price:,.2f}')
        st.write(f'Estimated Price Range: €{price_range_low:,.2f} - €{price_range_high:,.2f}')
        if user == "Buy Vehicle for Inventory":
           st.subheader(f"Offer no more than €{(predicted_used_price - profit_margin):,.2f} in order to make your €{profit_margin} margin in profit")
           st.success(f"At {commission_rate}% commission, you'll make €{(predicted_used_price * commission_rate):,.2f}")