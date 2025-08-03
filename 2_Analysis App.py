import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
# import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import ast

st.set_page_config(page_title="Visualizations")

st.title('Gurgaon Real Estate Analytics')

new_df = pd.read_csv('data_viz1.csv')

#st.dataframe(new_df)

group_df = group_df = new_df.groupby('sector').agg({'price':'mean',
                              'price_per_sqft':'mean',
                              'built_up_area':'mean',
                              'latitude':'first','longitude':'first'}).reset_index()


# st.dataframe(group_df)



import streamlit as st
import plotly.express as px
import seaborn as sns

st.title('Geo Map')
# Scatter Map with Tile Source
# fig = px.scatter_map(
#     group_df, 
#     lat="latitude", 
#     lon="longitude", 
#     color="price_per_sqft", 
#     size="built_up_area",
#     color_continuous_scale=px.colors.cyclical.IceFire, 
#     zoom=10,
#     text="sector",
#     width=1200,
#     height=700,
#     hover_name="sector",
#     #map_tile="open-street-map"  # Ensure a valid map tile source
# )

# st.plotly_chart(fig, use_container_width=True)


fig = px.scatter_geo(
    group_df,
    lat="latitude",
    lon="longitude",
    color="price_per_sqft",
    size="built_up_area",
    scope="asia",  # Adjust based on location
    projection="natural earth",
    hover_name="sector"
)
st.plotly_chart(fig, use_container_width=True)


feature_text = pickle.load(open('feature_text.pkl','rb'))
    


# Generate Word Cloud
st.title('Wordcloud')
wordcloud = WordCloud(
    width=800, 
    height=800, 
    background_color='white', 
    stopwords=set(['s']),  # Customize stopwords
    min_font_size=10
).generate(feature_text)  # Use actual text

# Display in Matplotlib
plt.figure(figsize=(8, 8), facecolor=None) 
plt.imshow(wordcloud, interpolation='bilinear') 
plt.axis("off") 
plt.tight_layout(pad=0) 

# Display in Streamlit
st.pyplot(plt.gcf())  # Pass the figure object


st.title('Area Vs Price')

property_type = st.selectbox('Choose a Property Type', ['flat','house'])

if property_type == 'flat':
    fig = px.scatter(new_df[new_df['property_type']=='flat'],x='built_up_area',y='price',color='bedRoom',title='Area Vs Price')
    st.plotly_chart(fig,use_container_width=True)
    
else:
    fig = px.scatter(new_df[new_df['property_type']=='house'],x='built_up_area',y='price',color='bedRoom',title='Area Vs Price')
    st.plotly_chart(fig,use_container_width=True)    
    

st.title('No. Of Bedrooms by Sector')
sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0,'overall')
select_sector = st.selectbox('Choose a sector', sector_options)

if select_sector == 'overall':
    fig = px.pie(new_df,names='bedRoom')
    st.plotly_chart(fig, use_container_width = True)
else:
    fig = px.pie(new_df[new_df['sector']==select_sector],names='bedRoom')
    st.plotly_chart(fig, use_container_width = True)   
    
    
st.title('Bedroom Price Comparison')

temp_df = new_df[new_df['bedRoom'] <= 4]    
     
fig = px.box(temp_df,x='bedRoom',y='price',title='BHK Price Range')  
st.plotly_chart(fig,use_container_width=True)   


st.title('Flat Vs Houses Distribution Comparison')

# # Create a figure
# fig, ax = plt.subplots(figsize=(8, 5))

# # Plot the distribution
# sns.kdeplot(new_df[new_df['property_type'] == 'flat']['price'], ax=ax, fill=True)
# sns.kdeplot(new_df[new_df['property_type'] == 'house']['price'], ax=ax, fill=True)

# # Add labels and legend
# ax.set_xlabel("Price", fontsize=12)
# ax.set_ylabel("Density", fontsize=12)
# ax.set_title("Price Distribution for Flats vs Houses", fontsize=14)
# ax.legend(title= temp_df["property_type"])  # Adds a legend

# # Display in Streamlit
# st.pyplot(fig)

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

st.title('Property Type Price Distribution')

# Create a figure
fig, ax = plt.subplots(figsize=(8, 5))

# Get unique property types
property_types = new_df['property_type'].unique()

# Define colors for different property types
colors = sns.color_palette("husl", len(property_types))  # Generates unique colors

# Plot KDE for each property type
for i, prop in enumerate(property_types):
    sns.kdeplot(
        new_df[new_df['property_type'] == prop]['price'], 
        ax=ax, 
        fill=True, 
        color=colors[i], 
        label=prop
    )

# Add labels and legend
ax.set_xlabel("Price", fontsize=12)
ax.set_ylabel("Density", fontsize=12)
ax.set_title("Price Distribution by Property Type", fontsize=14)
ax.legend(title="Property Type")  # Legend dynamically updates

# Display in Streamlit
st.pyplot(fig)
