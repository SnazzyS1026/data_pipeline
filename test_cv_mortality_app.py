import unittest
import pandas as pd
import numpy as np

class TestApp(unittest.TestCase):
    def test_cv_mortality_db_numeric_columns_datatype(self):
        df = pd.read_csv('cv_mortality.gz', compression='gzip', encoding='utf-8')
        assert df['Year'].dtype =='int64'
        assert df['Data_Value'].dtype=='float64'
        assert df['X_long'].dtype=='float64'
        assert df['Y-lat'].dtype=='float64'
        
    def test_groupby_state_csv_year_range_2000_2019(self):
        groupby_state = pd.read_csv('groupby_state.csv', encoding='utf-8', index=False)
        assert groupby_state['Year'].max()==2019
        assert groupby_state['Year'].min()==2000

    def test_groupby_state_csv_50_states(self):
        groupby_state = pd.read_csv('groupby_state.csv', encoding='utf-8', index=False)
        assert groupby_state['State'].unique().count()==50
    
    def test_county_2019_csv_year_is_2019(self):
        county_2019 = pd.read_csv('county_2019.csv', encoding='utf-8', index=False)
        assert county_2019['Year']==2019

if __name__=='__main__':
    unittest.main()