import pickle
import pandas as pd
import streamlit as st
import sklearn

# Load the saved model
with open('random_forest_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

st.title("Price Predictor")

property_type = st.selectbox("Property Type", options=['Apartment', 'Villa', 'Residential Plot', 'Independent Floor',
                                                       'Independent House'], index=0)

property_status = st.selectbox("Property Status", options=['Under Construction', 'Ready to move', 'Not determined'],
                               index=0)

property_building_status = st.selectbox("Property Building Status", options=['ACTIVE', 'UNVERIFIED', 'INACTIVE'],
                                        index=0)

Price_per_unit_area = st.number_input('Price per unit area for the property:')

City_id = st.number_input("City ID")

No_of_BHK = st.number_input("Number of rooms")

Locality_ID = st.number_input('Locality ID')

Size = st.number_input('Size of the property:')

is_furnished = st.selectbox("Is Furnished", options=['Furnished', 'Semi-Furnished', 'Unfurnished'], index=0)

is_RERA_registered = st.selectbox("is_RERA_registered", options=['True', 'False'], index=0)

property_type_mapping = {"Apartment": 0, "Villa": 4, "Residential Plot": 3, 'Independent Floor': 1,
                         'Independent House': 2}
property_status_mapping = {"Ready to move": 1, "Under Construction": 2, "Not determined": 0}
property_building_status_mapping = {'ACTIVE': 0, 'UNVERIFIED': 2, 'INACTIVE': 1}
is_furnished_mapping = {'Unfurnished': 2, 'Semi-Furnished': 1, 'Furnished': 0}
is_RERA_registered_mapping = {'True': 1, 'False': 0}

property_type_encoded = property_type_mapping[property_type]
property_status_encoded = property_status_mapping[property_status]
property_building_status_encoded = property_building_status_mapping[property_building_status]
is_furnished_encoded = is_furnished_mapping[is_furnished]
is_RERA_registered_encoded = is_RERA_registered_mapping[is_RERA_registered]


input_df = pd.DataFrame([{
        'Property_type': property_type_encoded,
        'Property_status': property_status_encoded,
        'Price_per_unit_area': Price_per_unit_area,
        'Property_building_status': property_building_status_encoded,
        'City_id': City_id,
        'No_of_BHK': No_of_BHK,
        'Locality_ID': Locality_ID,
        'Size': Size,
        'is_furnished': is_furnished_encoded,
        'is_RERA_registered': is_RERA_registered_encoded
    }])

if st.button("Predict Prices"):
    if input_df.empty:
        st.error("Please provide input data.")
    else:
        # Predict prices
        predictions = model.predict(input_df)
        st.success("Prediction Complete!")
        original_price = scaler.inverse_transform([[predictions[0]]])[0][0]
        input_df["Predicted_Price"] = original_price
        st.write(original_price)
        st.write(input_df)