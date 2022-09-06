from create_df import create_df
from data_cleaning import *
from write_to_csv import write_to_csv
from sql_query_df import *

def run_pipeline():
    
    # Get and clean data
    df=create_df()
    df=convert_dt(df)
    df=rename_cols(df)
    
    # write sql query into df
    groupby_state=groupby_state(df)
    groupby_county_2019=groupby_county_2019(df)

    # Output to csv
    df.write_to_csv('cv_mortality.gz', compression='gzip', encoding='utf-8', index=False)
    groupby_state.write_to_csv('groupby_state.csv', encoding='utf-8', index=False)
    groupby_county_2019.write_to_csv('county_2019.csv', encoding='utf-8', index=False)

    
if __name__=='__main__':
    run_pipeline()
    
    #if the name of the python instance is main, go ahead and run the application
