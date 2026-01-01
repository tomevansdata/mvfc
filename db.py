import pandas as pd
import streamlit as st
from databricks import sql
import requests


@st.cache_data(ttl=900)
def execute_query(query: str) -> pd.DataFrame:
    """
    Execute a SQL query against Databricks SQL warehouse and return dataframe
    
    Args:
        query: SQL query string to execute
        
    Returns:
        pandas DataFrame containing query results
    """
    databricks_config = st.secrets["databricks"]
    
    with sql.connect(
        server_hostname=databricks_config["server_hostname"],
        http_path=databricks_config["http_path"],
        access_token=databricks_config["access_token"]
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            
            # Fetch all results
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            # Convert to pandas DataFrame
            df = pd.DataFrame(rows, columns=columns)
            
            return df
