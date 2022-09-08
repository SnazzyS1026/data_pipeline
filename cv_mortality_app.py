
"""

To run this app:
1. cd into this directory
2. Run `streamlit run cv_mortality_app.py`

"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

######################################################

st.set_page_config(
    page_title="Hypertensive-Related Cardiovascular Disease Mortality Trends",
    # layout='wide'
)

st.title('''
Hypertension-related CVD Mortality Rates and Trend in the US
'''
)

st.header('''
What is Cardiovascular Disease?
''')

st.write('''
Cardiovascular disease (CVD) is a disease that affects the heart and blood vessels. Some examples of CVDs include:

- Coronary heart disease 
- Cerebrovascular disease 
- Congenital heart disease
- Peripheral arterial disease
- And many others

CVDs are the leading cause of death globally, representing 32% of all global deaths.$^1$ And there is a 39% prevalence of diagnosed CV conditions in the U.S. $^2$

The strongest risk factor for CVD is hypertension, or high blood pressure. Acute signs of hypertension may manifest as heart attacks or strokes.$^1$

''')

st.write('''
##### Explore the following graphs and map to see the trends in hypertension-related CVD mortality among US adults recorded by the Centers for Disease and Control Prevention (CDC) from 2000 to 2019.
''')
#####################################################################

# Load data and store in local cache

@st.cache(allow_output_mutation=True)
def load_data(path, compression, encoding):
    data = pd.read_csv(path)
    data = data.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})
    return data

df = load_data('cv_mortality.gz', compression='gzip', encoding='utf-8')

by_state = load_data('groupby_state.csv', compression='none', encoding='utf-8')

by_county = load_data('county_2019.csv', compression='none', encoding='utf-8')

#############################################

# Create tabs for different graphs/maps
tabs = st.tabs(['Dataset', 'Pie Charts', 'US Map', 'Bar Graph'])

tab_dataset = tabs[0]
with tab_dataset:
    st.markdown('''
    #### Sample Dataset
    ''')

    # Display an interactive table
    st.dataframe(df.sample(n=8))


##############################################

tab_pie = tabs[1]
with tab_pie:

    # cols = st.columns(2)
    # with cols[0]:

    # PIE CHARTS

    # Dropdown menu for graphs
    options_list = ['By Age Group', 'By Gender', 'By Race/Ethnicity']
    options_menu = st.selectbox('Please select:', options_list)

    if options_menu == 'By Age Group':
        st.markdown('''
        #### CVD Mortality by Age Group
        ''')

        #Grouping by Age
        age_filter = df.groupby('Age_Group')['Data_Value'].sum()
        age_groups = ['Ages 35-64 yrs', 'Ages 65+ yrs']
        colors_list =['Maroon', 'tab:blue']
        explode_val = (0, 0.1)

        pie_age = plt.figure(figsize=(5,5))
        plt.pie(age_filter, labels=age_groups, autopct='%1.1f%%', explode = explode_val, colors=colors_list, textprops={'fontsize': 12})
        st.pyplot(pie_age)
    elif options_menu == 'By Gender':
        st.markdown('''
        #### CVD Mortality by Gender
        ''')

        #Grouping by Gender
        genders = df[df['Sex'] !='Overall']
        gender_filter = genders.groupby('Sex')['Data_Value'].sum()
        gender_groups = ['Female', 'Male']
        colors_list2 =['Chocolate', 'DarkBlue']
        explode_val2 = (0, 0.1)

        pie_gender = plt.figure(figsize=(5,5))
        plt.pie(gender_filter, labels=gender_groups, autopct='%1.1f%%', explode = explode_val2, colors=colors_list2, textprops={'fontsize': 12})
        st.pyplot(pie_gender)
    else:
        st.markdown('''
        #### CVD Mortality by Race/Ethnicity
        ''')

        #Group by Race/Ethnicity
        race = df[df['Race_Ethnicity']!='Overall']
        race_filter = race.groupby('Race_Ethnicity')['Data_Value'].mean()
        race_groups = ['American Indian and Alaska Native', 'Asian and Pacific Islander', 'Black', 'Hispanic', 'White']
        colors_list3 =['CadetBlue', 'Crimson', 'Cornsilk', 'DarkGray', 'DarkSalmon']
        explode_val3 = (0.05, 0.05, 0.05, 0.05, 0.05)

        pie_race = plt.figure(figsize=(5,5))
        plt.pie(race_filter, labels=race_groups, autopct='%1.1f%%', explode = explode_val3, colors=colors_list3, textprops={'fontsize': 12})
        st.pyplot(pie_race)
       
    # with cols[1]:
       
####################################################################
 
tab_map = tabs[2]
with tab_map:
    # CHLOROPETH MAP

    st.write('''
    #### CVD Mortality by County
    '''
    )

    # Create US Map
    by_county['text'] = by_county['County'] + ", " + by_county['State'] + " " +  (by_county['Data_Value']).astype(str)+' cases per 100,000'
    limits = [(0,100),(101,300),(301,600),(601,1000),(1001,1500), (1501, 3000)]
    colors = ["#E34234","#CD5C5C","#FF0000", "#FF1C00", "#FF6961", "#F4C2C2"]
    cities = []
    scale = 5000

    fig = go.Figure()

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = by_county[lim[0]:lim[1]]
        fig.add_trace(go.Scattergeo(
            locationmode = 'USA-states',
            lon = df_sub['lon'],
            lat = df_sub['lat'],
            text = df_sub['text'],
            marker = dict(
                size = df_sub['Data_Value']*0.2,
                color = colors[i],
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode = 'area'
                ),
            name = '{0} - {1}'.format(lim[0],lim[1])))


        fig.update_layout(
            title_text = '(Click legend to toggle cases)',
            title_font_size=20,
            title_x=0.5,
            showlegend = True,
            legend_title_text='<b>Cases per 100,000</b>',
            font=dict(size=12),
            geo = dict(
                scope = 'usa',
                landcolor = 'rgb(217, 217, 217)',
                projection=go.layout.geo.Projection(type = 'albers usa')
            )
        )
    st.plotly_chart(fig)


##############################################################
tab_bar = tabs[3]
with tab_bar:

# BAR GRAPH

    # Groupedby State, Year
    st.write('''
    #### CVD Mortality by State
    '''
    )

    # Make option bar
    state_option = by_state['State'].unique().tolist()

    state = st.multiselect('Which state(s) would you like to see?', state_option, ['AL', 'AR', 'CA', 'FL', 'MS', 'NE', 'NY', 'OH', 'OK', 'OR', 'TX', 'WY'])

    by_state = by_state[by_state['State'].isin(state)]

    # Figure
    fig3 = px.bar(by_state, x='State', y=by_state['AVG(Data_Value)'], 
                hover_name = by_state['AVG(Data_Value)'], 
                range_y= [0,550], 
                animation_frame='Year', 
                animation_group='State', 
                barmode='group').update_layout(xaxis_title='<b>States</b>', 
                                                yaxis_title='<b>Average Cases per 100,000<b>'
                                                )
    fig3.update_xaxes(title_font=dict(size=15))
    fig3.update_yaxes(title_font=dict(size=15))

    st.write(fig3)


############################################################################## 

# Add spaces between charts and references

st.text("")
st.text("")
st.text("")
st.text("")

##############################################################################

# References

st.write('''
##### References
1. https://www.who.int/news-room/fact-sheets/detail/cardiovascular-diseases-(cvds)
2. https://www.statista.com/topics/3484/cardiovascular-disease-in-the-us/#dossierContents__outerWrapper
3. Dataset: https://chronicdata.cdc.gov/Heart-Disease-Stroke-Prevention/Rates-and-Trends-in-Hypertension-related-Cardiovas/uc9k-vc2j
'''
)

################################################################################


# def barplot_by_year(year_input):
#     fig_year = df3[df3['Year']==year_input]
    
#     fig = plt.figure(figsize = (10,5))

#     # Assign label names and font
#     plt.xlabel('US States', fontsize=18, fontweight='black', color = '#333F4B')
#     plt.ylabel('Cases per 100,000', fontsize=18, fontweight='black', color = '#333F4B')

#     # Set style for axes
#     plt.rcParams['axes.edgecolor']='#333F4B'
#     plt.rcParams['axes.linewidth']=0.8
#     plt.rcParams['xtick.color']='#333F4B'
#     plt.rcParams['ytick.color']='#333F4B'

#     # Set font
#     plt.xticks(fontsize=6)
#     plt.rcParams['font.family'] = 'sans-serif'
#     plt.rcParams['font.sans-serif'] = 'Helvetica'
#     plt.bar(fig_year['State'], fig_year['AVG(Data_Value)'], color='#9370DB')

#     # animation_frame = year_input, animation_group ='State'

#     show=st.pyplot(fig)
#     return show

# # Create time slider
# year_input = st.slider("Year", int(df3['Year'].min()), int(df3['Year'].max()))
# year_filter = df3['Year'] < year_input

# barplot_by_year(year_input)

############################################################