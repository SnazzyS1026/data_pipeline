import unittest
import pandas as pd
import numpy as np

class Testclass(unittest.TestCase):
    def test_cv_mortality_db_numeric_columns_datatype(self):
        df = pd.read_csv('cv_mortality.gz', compression='gzip', encoding='utf-8')
        assert df['Year'].dtype =='int64'
        assert df['Data_Value'].dtype=='float64'
        assert df['Longitude'].dtype=='float64'
        assert df['Latitude'].dtype=='float64'
        
    def test_groupby_state_csv_year_range_2000_2019(self):
        groupby_state = pd.read_csv('groupby_state.csv', encoding='utf-8')
        assert groupby_state['Year'].max()==2019
        assert groupby_state['Year'].min()==2000

    def test_groupby_state_csv_50_states(self):
        groupby_state = pd.read_csv('groupby_state.csv', encoding='utf-8')

        # Washington D.C. is recognized as a state in this instance
        assert len(groupby_state['State'].unique())==51
    
    def test_county_2019_csv_year_is_2019(self):
        county_2019 = pd.read_csv('county_2019.csv', encoding='utf-8')
        assert len(county_2019[county_2019['Year']!=2019])==0

if __name__=='__main__':
    unittest.main()

