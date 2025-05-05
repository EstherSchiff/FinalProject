import sqlite3
import streamlit as st

# cached db connection
@st.cache_resource
def get_connection(db="cards.db"):
    conn = sqlite3.connect(db, check_same_thread=False)
    return conn
