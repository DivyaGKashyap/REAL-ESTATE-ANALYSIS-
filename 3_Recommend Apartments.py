import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Recommend Apartments")

location_df = pickle.load(open('D:\Divya\Portfolio Projects\The project\Gurgaon\APP_STREAMLIT\location_distance.pkl','rb'))
cosine_sim1 = pickle.load(open('D:\Divya\Portfolio Projects\The project\Gurgaon\APP_STREAMLIT\cosine_sim1.pkl','rb'))
cosine_sim2 = pickle.load(open('D:\Divya\Portfolio Projects\The project\Gurgaon\APP_STREAMLIT\cosine_sim2.pkl','rb'))
cosine_sim3 = pickle.load(open('D:\Divya\Portfolio Projects\The project\Gurgaon\APP_STREAMLIT\cosine_sim3.pkl','rb'))


def recommend_properties_with_scores(property_name,top_n=5):
    
    cosine_sim_matrix = 30*cosine_sim1+20*cosine_sim2+8*cosine_sim3        
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))        
    sorted_scores = sorted(sim_scores,key = lambda x: x[1], reverse=True)        
    top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
    top_score = [i[1] for i in sorted_scores[1:top_n+1]]        
    top_properties = location_df.index[top_indices].tolist()
    recommendations_df = pd.DataFrame({'PropertyName': top_properties,'SimilarityScore': top_score })
    return recommendations_df    
        


st.dataframe(location_df)

st.title('Select a landmark and surrounding radius to get recommendations on properties')

selected_location = st.selectbox('Select a Property', sorted(location_df.columns.tolist()))
radius = st.number_input('Enter radius in kms')

search = st.button('Search')

if search:
    result_ser = location_df[location_df[selected_location] < radius*1000] [selected_location].sort_values().to_dict()
    
    for key,value in result_ser.items():
        st.text(str(key)+ ' --> '+ str(round(value)/1000)+ 'kms')
        
    
    
st.title('Select an Apartment for similar recommendations')  
      
selected_apartment = st.selectbox('Select an Apartment',sorted(location_df.index.tolist()))

if st.button('Recommend'):
    recommendations_df = recommend_properties_with_scores(selected_apartment)
    st.dataframe(recommendations_df)
    
    
    
    
    
    