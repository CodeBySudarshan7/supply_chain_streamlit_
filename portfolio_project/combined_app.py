import os
import sys
import streamlit as st
from utils.db import init_database

st.set_page_config(
    page_title="Supply Chain Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme with pink accents inspired by streamlit.io
st.markdown("""
<style>
    /* Main page background */
    [data-testid="stAppViewContainer"] {
        background-color: #1a1a2e;
        color: #ffffff;
    }
    
    [data-testid="stHeader"] {
        background-color: #1a1a2e;
    }
    
    /* Professional button styling - Pink gradient */
    .stButton > button {
        background: linear-gradient(135deg, #ff006e 0%, #d63384 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 16px 28px;
        font-size: 16px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(255, 0, 110, 0.4);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #d63384 0%, #ff006e 100%);
        box-shadow: 0 8px 30px rgba(255, 0, 110, 0.6);
        transform: translateY(-3px);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Form styling */
    .stForm {
        border: 2px solid #ff006e;
        border-radius: 12px;
        padding: 28px;
        background: #252a3a;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div,
    .stRadio > div,
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input {
        background-color: #1a1f2e !important;
        border: 2px solid #404860 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover,
    .stTextInput > div > div > input:hover,
    .stNumberInput > div > div > input:hover,
    .stDateInput > div > div > input:hover {
        border-color: #ff006e !important;
        box-shadow: 0 0 12px rgba(255, 0, 110, 0.3) !important;
    }
    
    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus {
        border-color: #ff006e !important;
        box-shadow: 0 0 0 3px rgba(255, 0, 110, 0.15) !important;
    }
    
    /* Labels */
    label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar professional styling */
    [data-testid="stSidebar"] {
        background: #0f1419;
    }
    
    /* Title and headings */
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 800;
    }
    
    h1 {
        background: linear-gradient(135deg, #ff006e 0%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Info box styling */
    .stInfo {
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.15) 0%, rgba(214, 51, 132, 0.15) 100%);
        border-left: 4px solid #ff006e;
        border-radius: 10px;
        color: #ffffff;
    }
    
    /* Success message */
    .stSuccess {
        background-color: #1a4d2e !important;
        color: #ffffff !important;
        border-left: 4px solid #4ecca3 !important;
    }
    
    /* Metric styling */
    .stMetric {
        background: #252a3a;
        border-radius: 12px;
        border: 1px solid #404860;
        padding: 16px;
    }
    
    /* Markdown text color */
    p, li {
        color: #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize database on app start
init_database()

st.title("🏪 Supply Chain Analytics Platform")

st.markdown("""
### Welcome to the Supply Chain Analytics Dashboard

This platform provides comprehensive tools for managing and analyzing supply chain data:

**📊 Features:**
- **Dashboard**: Real-time analytics with visualizations
- **Data Entry**: Add new supply chain records directly
- **MySQL Integration**: All data is stored securely in a database
- **Intelligent Filtering**: Filter by product type, supplier, and date range
- **Auto-fill Nulls**: Missing values are automatically handled

### Getting Started:

1. **Data Entry Page**: Add new supply chain records
2. **Dashboard Page**: View analytics and visualizations

---

### Navigation:

Use the sidebar to navigate between pages or click the buttons below.
""")

st.markdown("---")

col1, col2 = st.columns(2, gap="large")

with col1:
    if st.button("📝 Data Entry", use_container_width=True, key="btn_entry"):
        st.switch_page("pages/01_data_entry.py")

with col2:
    if st.button("📊 Analytics Dashboard", use_container_width=True, key="btn_dashboard"):
        st.switch_page("pages/02_dashboard.py")

st.markdown("---")
st.info("💡 All data is persisted in MySQL. Null values are automatically handled as 0 for numeric fields and 'N/A' for text fields.")

