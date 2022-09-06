from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())

# Create new pandas dataframes from sql query

def group_state(df): 
    q = """ 
        SELECT Year, State, Data_Value, Sex, Longitude as lon, Latitude as lat, AVG(Data_Value)
        FROM df
        WHERE Sex <> 'Overall'
        GROUP BY State, Year;
        """
    groupby_state = pysqldf(q)
    return groupby_state


def group_county_2019(df):
    q = """ 
        SELECT Year, County, State, Data_Value, Sex, Longitude as lon, Latitude as lat, AVG(Data_Value)
        FROM df
        WHERE Sex <> 'Overall'
        AND Year==2019
        GROUP BY County, Year
        ORDER BY State;
        """
    groupby_county_2019 = pysqldf(q)
    return groupby_county_2019
    