import streamlit as st
import sys
sys.path.append('..')
from utils.db import init_database, insert_record, get_unique_values
from datetime import datetime

st.set_page_config(page_title="Data Entry - Supply Chain", layout="wide")

# Dark theme with pink accents inspired by streamlit.io
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #1a1a2e;
        color: #ffffff;
    }
    
    [data-testid="stHeader"] {
        background-color: #1a1a2e;
    }
    
    .stForm {
        border: 2px solid #ff006e;
        border-radius: 12px;
        padding: 28px;
        background: #252a3a;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    
    .stForm > button {
        background: linear-gradient(135deg, #ff006e 0%, #d63384 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 16px 28px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 6px 20px rgba(255, 0, 110, 0.18) !important;
        width: 100% !important;
    }
    
    .stForm > button:hover {
        background: linear-gradient(135deg, #d63384 0%, #ff006e 100%) !important;
        transform: translateY(-2px) !important;
    }
    
    .stForm > button:active {
        transform: translateY(0) !important;
    }
    
    .stSelectbox > div > div,
    .stRadio > div,
    .stMultiselect > div > div {
        background-color: #1a1f2e !important;
        color: #ffffff !important;
        border: 1px solid #404860 !important;
        border-radius: 10px !important;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.15) !important;
    }
    
    .stSelectbox > div > div:hover,
    .stRadio > div:hover,
    .stMultiselect > div > div:hover {
        border-color: #ff006e !important;
    }
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input {
        border-radius: 10px !important;
        border: 1px solid #404860 !important;
        background-color: #1f2433 !important;
        color: #ffffff !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus {
        border-color: #ff006e !important;
        box-shadow: 0 0 0 3px rgba(255, 0, 110, 0.15) !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0f1419;
        color: #ffffff;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(255, 0, 110, 0.15) 0%, rgba(214, 51, 132, 0.15) 100%);
        border-left: 4px solid #ff006e;
        border-radius: 10px;
        color: #ffffff;
    }
    
    .stSuccess {
        background-color: #1a4d2e !important;
        color: #ffffff !important;
        border-left: 4px solid #4ecca3 !important;
    }
    
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 800 !important;
    }
    
    p, li, span {
        color: #e0e0e0 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📝 Supply Chain Data Entry")
st.markdown("Add new supply chain records to the database with a clean, intuitive interface.")

# Initialize database on first load
init_database()

with st.form("data_entry_form"):
    st.subheader("Enter Supply Chain Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date = st.date_input("Date", value=datetime.now())
        product_type = st.selectbox("Product Type", ["haircare", "skincare", "cosmetics"])
        sku = st.text_input("SKU", value="SKU000")
        price = st.number_input("Price", value=0.0, step=0.01)
        availability = st.number_input("Availability", value=0, step=1)
    
    with col2:
        number_of_products_sold = st.number_input("Number of Products Sold", value=0, step=1)
        revenue_generated = st.number_input("Revenue Generated", value=0.0, step=0.01)
        customer_demographics = st.selectbox("Customer Demographics", ["Male", "Female", "Non-binary", "Unknown"])
        stock_levels = st.number_input("Stock Levels", value=0, step=1)
        lead_times = st.number_input("Lead Times (days)", value=0, step=1)
    
    with col3:
        order_quantities = st.number_input("Order Quantities", value=0, step=1)
        shipping_times = st.number_input("Shipping Times (days)", value=0, step=1)
        shipping_carriers = st.selectbox("Shipping Carriers", ["Carrier A", "Carrier B", "Carrier C"])
        shipping_costs = st.number_input("Shipping Costs", value=0.0, step=0.01)
        supplier_name = st.text_input("Supplier Name", value="Supplier 1")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        location = st.selectbox("Location", ["Mumbai", "Delhi", "Kolkata", "Chennai", "Bangalore"])
        production_volumes = st.number_input("Production Volumes", value=0, step=1)
        manufacturing_lead_time = st.number_input("Manufacturing Lead Time", value=0, step=1)
        manufacturing_costs = st.number_input("Manufacturing Costs", value=0.0, step=0.01)
    
    with col5:
        inspection_results = st.selectbox("Inspection Results", ["Pass", "Fail", "Pending"])
        defect_rates = st.number_input("Defect Rates (%)", value=0.0, step=0.01, min_value=0.0, max_value=100.0)
        transportation_modes = st.selectbox("Transportation Modes", ["Road", "Rail", "Sea", "Air"])
        routes = st.selectbox("Routes", ["Route A", "Route B", "Route C"])
    
    with col6:
        costs = st.number_input("Costs", value=0.0, step=0.01)
    
    submitted = st.form_submit_button("✨ Submit Entry", use_container_width=True)

if submitted:
    data_dict = {
        "date": date,
        "product_type": product_type,
        "sku": sku,
        "price": price,
        "availability": availability,
        "number_of_products_sold": number_of_products_sold,
        "revenue_generated": revenue_generated,
        "customer_demographics": customer_demographics,
        "stock_levels": stock_levels,
        "lead_times": lead_times,
        "order_quantities": order_quantities,
        "shipping_times": shipping_times,
        "shipping_carriers": shipping_carriers,
        "shipping_costs": shipping_costs,
        "supplier_name": supplier_name,
        "location": location,
        "production_volumes": production_volumes,
        "manufacturing_lead_time": manufacturing_lead_time,
        "manufacturing_costs": manufacturing_costs,
        "inspection_results": inspection_results,
        "defect_rates": defect_rates,
        "transportation_modes": transportation_modes,
        "routes": routes,
        "costs": costs,
    }
    
    if insert_record(data_dict):
        st.success("✅ Record inserted successfully!")
        st.balloons()
    else:
        st.error("❌ Failed to insert record. Please check your MySQL connection.")

st.markdown("---")
st.info("💡 Tip: All fields are required. Fill them with appropriate values or 0/N/A for optional data.")
