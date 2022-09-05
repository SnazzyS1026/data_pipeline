"""
Write to CSV, specifying compression type 'gzip'

"""

import pandas as pd

def write_to_csv(df):
    df.to_csv('cv_mortality.gz', compression='gzip', encoding='utf-8', index=False)
    return