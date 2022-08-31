import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


st.title('''
Hypertensive-Related Cardiovascular Disease Mortality Trends
'''
)
st.write('''
##### Explore the following graphs and maps to see the trends in hypertension-related CVD mortality among US adults by age group, race, location, and gender as recorded by the Centers for Disease and Control Prevention (CDC) from 2000 to 2019.
''')

#header1='<h1 style=font-family: verdana; color=blue;>What is Cardiovascular Disease?</h1>'
#st.markdown(header1, unsafe_allow_html=True)


st.header('''
What is Cardiovascular Disease?
''')

st.markdown('''
Cardiovascular disease (CVD) is a disease that affects the heart and blood vessels. Some examples of CVDs include:

    - Coronary heart disease 
    - Cerebrovascular disease 
    - Congenital heart disease
    - Peripheral arterial disease
    - And many others

CVDs are the leading cause of death globally, representing 32% of all global deaths.$^1$ And there is a 39% prevalence of diagnosed CV conditions in the U.S. $^2$

The strongest risk factor for CVD is hypertension, or high blood pressure. Acute signs of hypertension may manifest as heart attacks or strokes.$^1$

''')


#Define load_data function to prevent loading data everytime we make changes in dataset.
#Use streamlit's cache notation.

dataset = (
   "/github_files/cv_mortality_app.py"
   )

@st.cache(persist=True)
def load_data(nrows):
    df = pd.read_csv(data, nrows=nrows)
    #Drop N/A values in latitude and longitude so it doesn't fail when we use map
    df.dropna(subset=['Latitude', 'Longitude'], inplace=True)
    lowercase = lambda x: str(x).lower()
    df.rename(lowercase, axis='columns', inplace=True)
    return df

#Load first 100000 rows
df1 = load_data(100000)
st.markdown('''
#### Sample Dataset
''')
# Display an interactive table
st.dataframe(df.sample(n=8))

#Plot 1
st.markdown('''
#### CVD mortality throughout the years, from 2000 to 2019
''')
agree = st.checkbox('Show', value=True)

if agree:
    #def 
    year = st.slider("Year", int(2000), int(df['year'].max()))
    st.map(df.query("data_value >= @year")[['latitude', 'longitude']].dropna(how='any'))

#Plot 2
st.markdown('''
CVD mortality by age group
''')
agree = st.checkbox('Show', value=True)

if agree:
    #def pie_chart_age(df):

#map_data = df[['latitude', 'longitude']]
#st.map(map_data)















#st.write('''
#References
#1. Cardiovascular diseases (CVDs): https://www.who.int/news-room/fact-sheets/detail/cardiovascular-diseases-(cvds)
#2. Cardiovascular disease in the U.S. - Statistics & Facts : https://www.statista.com/topics/3484/cardiovascular-disease-in-the-us/#dossierContents__outerWrapper
#3. Hypertensive and cardiovascular risk: General aspects: https://pubmed.ncbi.nlm.nih.gov/29127059/#:~:text=Hypertension%20is%20the%20strongest%20or%20one%20of%20the,including%20atrial%20fibrillation%2C%20cerebral%20stroke%20and%20renal%20failure.
#''')
