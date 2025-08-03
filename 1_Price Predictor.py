import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Real Estate Assistant")

st.title('Property Price Predictor')

with open ('D:\Divya\Portfolio Projects\The project\Gurgaon\APP_STREAMLIT\df.pkl','rb') as file:
    df = pickle.load(file)
    
with open ('D:\Divya\Portfolio Projects\The project\Gurgaon\APP_STREAMLIT\pipeline.pkl','rb') as file:
    pipeline = pickle.load(file)  
 
st.header('Enter Your Inputs')
 
# property type
property_type = st.selectbox('Property Type',['flat','house'])   

# Sector
sector = st.selectbox('Sector',sorted(df['sector'].unique().tolist()))

#Bedroom
bedroom = float(st.selectbox('Number of Bedrooms',sorted(df['bedRoom'].unique().tolist())))

#Bathroom
bathroom = float(st.selectbox('Number of Bathrooms',sorted(df['bathroom'].unique().tolist())))

#Balcony
balcony = st.selectbox('Number of Balconies',sorted(df['balcony'].unique().tolist()))

#Property Age
property_age = st.selectbox('Age Of Property',sorted(df['agePossession'].unique().tolist()))

#Built Up Area
built_up_area = float(st.number_input('Built Up Area'))

#Servant Room
servant_room = float(st.selectbox('Servant Room',[0.0,1.0]))

#Store Room
store_room = float(st.selectbox('Store Room',[0.0,1.0]))

#Furnishing Type
furnishing_type = st.selectbox('Furnishing Type',sorted(df['furnishing_type'].unique().tolist()))

#Luxury Category
luxury_category = st.selectbox('Luxury Category',sorted(df['luxury_category'].unique().tolist()))

#Floor Category
floor_category = st.selectbox('Floor Category',sorted(df['floor_category'].unique().tolist()))


if st.button('Predict The Price'):
    
    #Create a datafrome
    
    data = [property_type,sector,bedroom,bathroom,balcony,property_age,built_up_area,servant_room,store_room,furnishing_type,luxury_category,floor_category]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony','agePossession', 'built_up_area', 'servant room', 'store room','furnishing_type', 'luxury_category', 'floor_category']
    
    #convert to dataframe
    one_df = pd.DataFrame([data],columns=columns)
    
       
    # predict
    
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = round(base_price - 0.22,2)
    high = round(base_price + 0.22,2)
    
    # Display
    st.text(f'The price of the property is between {low} Cr and {high} Cr.')
    
    
    