"""
Connect to local database and create df

"""

import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def create_df():
    engine = create_engine("sqlite:///C:\\Users\sandr\OneDrive\Desktop\Metis\DS_Engineering\Projects\Data_Pipeline\github_files\cardiovascular_mortality_db.db")
    df = pd.read_sql(
    '''
    SELECT *
    FROM
    new_table;
    '''
    , engine)
    
    return df