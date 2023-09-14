import streamlit as st
import joblib
import numpy as np
import os
import dictionarys
from dictionarys import preprocess, process, number_to_words
from database_helper import DataBaseHelper

st.title("Flat Price Prediction For Mumbai")

model_filepath = os.path.join('model_repository', os.listdir("model_repository")[-1], 'xgboost_model.pkl')
pipe = joblib.load(model_filepath)

area = st.number_input('Enter Area of Flat')

latitude = st.number_input('Enter Latitude of Area')

longitude = st.number_input('Enter Longitude of Area')

bedrooms = st.selectbox("Number of Bedroom's", ['One', 'Two', 'Three', 'Four', 'Five', 'Six_Plus'])

bathrooms = st.selectbox("Number of Bathroom's", ['One', 'Two', 'Three', 'Four', 'Five', 'Six_Plus'])

balcony = st.selectbox("Number of Balcony's", ['One', 'Two', 'Three', 'Four', 'Five', 'Six_Plus'])

neworold = st.selectbox("Property Type", ['Resale', 'New Property'])

parking = st.selectbox("Number of Parking Availabel", ['One', 'Two', 'Three', 'Four', 'Five'])

furnished_status = st.selectbox("furnished_status", ["Unfurnished", "Semi-Furnished", "Furnished"])

lift = st.selectbox("Number of Lift Avaliable", ['One', 'Two', 'Three', 'Four', 'Five'])

type_of_building = st.selectbox("It is", ['Flat', 'Individual House'])

db_helper = DataBaseHelper()

if st.button('Price is'):

   features = [area, latitude, longitude, process(bedrooms), process(bathrooms), process(balcony), neworold, 
            process(parking), furnished_status, process(lift), type_of_building]
   
   query = preprocess(features)
   query = np.array(query)
   query = query.reshape(1, 58)

   pred = pipe.predict(query)[0]
   features = [area, latitude, longitude, process(bedrooms), process(bathrooms), process(balcony), neworold, 
            process(parking), furnished_status, process(lift), type_of_building, int(pred)]
   db_helper.insert_values(features)

   st.title("The predicted fare price is " + str(number_to_words(int(pred))))