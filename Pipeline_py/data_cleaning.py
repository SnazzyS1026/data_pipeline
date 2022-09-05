"""
Cleaning the data

"""
import pandas as pd
import numpy as np

# Convert specific columns to appropriate datatypes
def convert_dt(df):
    df[['Year', 'Data_Value', 'Confidence_limit_Low', 
        'Confidence_limit_High']]=df[['Year','Data_Value', 'Confidence_limit_Low', 
                                      'Confidence_limit_High']].apply(pd.to_numeric)
    return df

# Rename columns for easier interpretability
def rename_cols(df):
    df.rename(columns={"LocationID": "Location_ID", "Age Group": "Age_Group", 
                       "Race/Ethnicity":"Race_Ethnicity", "X_long": "Longitude", 
                       "Y_lat": "Latitude"}, inplace=True)
    return df