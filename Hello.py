# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
from flask import Flask, render_template
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import KustoServiceError
from azure.kusto.data.helpers import dataframe_from_result_table
import pandas as pd

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to PTP Tyre Bay! 👋")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        test edit
    """
    )

# URL AND DB NAME
CLUSTER_URL = "https://tyrebaycluster.southeastasia.kusto.windows.net"
KUSTO_DATABASE = "TyreBayDB"

# REDIRECT TO LOGIN PAGE
try:
    KCSB = KustoConnectionStringBuilder.with_interactive_login(CLUSTER_URL)
    KUSTO_CLIENT = KustoClient(KCSB)
except KustoServiceError as e:
    print("Error connecting to Azure Data Explorer:", e)

# KQL QUERY
KUSTO_QUERY = "tyrebaytable | take 10"
try:
    RESPONSE = KUSTO_CLIENT.execute(KUSTO_DATABASE, KUSTO_QUERY)
    df = dataframe_from_result_table(RESPONSE.primary_results[0])
except KustoServiceError as e:
    print("Error executing Kusto query:", e)
    df = pd.DataFrame()  # Empty DataFrame in case of error

if __name__ == "__main__":
    run()
