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


def execute_non_query(statement: str) -> int:
    """
    Execute a non-query SQL statement (INSERT/UPDATE/DELETE) against Databricks

    Returns the number of affected rows when supported, otherwise 0.
    """
    databricks_config = st.secrets["databricks"]

    with sql.connect(
        server_hostname=databricks_config["server_hostname"],
        http_path=databricks_config["http_path"],
        access_token=databricks_config["access_token"]
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(statement)
            try:
                # Some drivers return rowcount
                return cursor.rowcount if hasattr(cursor, "rowcount") else 0
            except Exception:
                return 0


def run_databricks_job(job_id: int, timeout_seconds: int = 30) -> dict:
    """
    Trigger a Databricks job run using the Databricks REST API `jobs/run-now`.

    Args:
        job_id: numeric Databricks job id
        timeout_seconds: HTTP request timeout

    Returns:
        dict: parsed JSON response from Databricks on success, or an error dict on failure.
    """
    databricks_config = st.secrets.get("databricks", {})
    server = databricks_config.get("server_hostname")
    token = databricks_config.get("access_token")

    if not server or not token:
        return {"error": "Databricks credentials not found in st.secrets['databricks']"}

    url = f"https://{server}/api/2.1/jobs/run-now"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"job_id": int(job_id)}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout_seconds)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        # try to include response content when available
        err = {"error": str(e)}
        try:
            if e.response is not None:
                err["status_code"] = e.response.status_code
                try:
                    err["response_json"] = e.response.json()
                except Exception:
                    err["response_text"] = e.response.text
        except Exception:
            pass
        return err

