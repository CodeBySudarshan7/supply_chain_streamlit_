import streamlit as st
import sys
sys.path.append('..')
from utils.db import load_data_from_sql, get_unique_values, get_date_range, init_database
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Supply Chain Analytics Dashboard", layout="wide")

# Dark theme with pink accents inspired by streamlit.io
st.markdown("""
<style>
    /* Main background */
    [data-testid="stAppViewContainer"] {
        background-color: #1a1a2e;
        color: #ffffff;
    }
    
    [data-testid="stHeader"] {
        background-color: #1a1a2e;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0f1419;
        color: #ffffff;
    }
    
    .stRadio > div > label,
    .stSelectbox > div > label,
    .stMultiselect > div > label {
        font-weight: 700 !important;
        color: #ffffff !important;
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
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
    
    .stMetric {
        background: #252a3a;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #404860;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #ff006e !important;
        font-weight: 800 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
        color: #ffffff;
    }
    
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: rgba(255, 0, 110, 0.12) !important;
        color: #ff006e !important;
    }
    
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 800;
    }
    
    p, li {
        color: #e0e0e0;
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

    .dashboard-row {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin-bottom: 1.5rem;
    }

    .dashboard-card,
    .dashboard-small-card,
    .dashboard-chart-card {
        border-radius: 24px;
        background: #14182d;
        border: 1px solid #272e45;
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.18);
        padding: 22px;
    }

    .dashboard-card {
        min-width: 220px;
        flex: 1;
    }

    .dashboard-card-title {
        color: #a4acbc;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 12px;
        margin-bottom: 8px;
    }

    .dashboard-card-value {
        color: #ffffff;
        font-size: 2.6rem;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .dashboard-card-note {
        color: #7f8bb3;
        font-size: 0.95rem;
    }

    .dashboard-small-card {
        min-width: 280px;
        flex: 1;
        padding: 18px;
    }

    .dashboard-small-card h4 {
        margin: 0 0 8px 0;
        font-size: 1rem;
        font-weight: 700;
        color: #ffffff;
    }

    .dashboard-small-card p {
        color: #b0b8d5;
        margin: 0;
        line-height: 1.6;
    }

    .dashboard-chart-card {
        width: 100%;
    }

    .dashboard-chart-card h3 {
        margin-top: 0;
        color: #ffffff;
    }

    .dashboard-divider {
        height: 1px;
        background: rgba(255, 255, 255, 0.06);
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def add_period_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["month_period"] = df["date"].dt.to_period("M")
    df["week_start"] = df["date"] - pd.to_timedelta(df["date"].dt.weekday, unit="D")
    df["period_label"] = df["month_period"].dt.strftime("%b %Y")
    return df


def build_period_summary(df: pd.DataFrame, range_labels, period_type):
    rows = []
    for label, period_df in range_labels:
        rows.append({
            "period": label,
            "records": len(period_df),
            "total_revenue": round(period_df["revenue_generated"].sum(), 2),
            "avg_shipping_costs": round(period_df["shipping_costs"].mean() if len(period_df) else 0, 2),
            "total_shipping_costs": round(period_df["shipping_costs"].sum(), 2),
            "avg_price": round(period_df["price"].mean() if len(period_df) else 0, 2),
            "avg_lead_time": round(period_df["lead_times"].mean() if len(period_df) else 0, 2),
            "avg_defect_rate": round(period_df["defect_rates"].mean() if len(period_df) else 0, 2),
            "total_production_volume": int(period_df["production_volumes"].sum()) if "production_volumes" in period_df.columns else 0,
            "avg_order_quantity": round(period_df["order_quantities"].mean() if len(period_df) else 0, 2),
            "revenue_per_record": round(period_df["revenue_generated"].sum() / len(period_df), 2) if len(period_df) else 0,
        })
    return pd.DataFrame(rows)


def calculate_business_components(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["profit"] = (
        pd.to_numeric(df["revenue_generated"], errors="coerce").fillna(0)
        - pd.to_numeric(df["costs"], errors="coerce").fillna(0)
    )
    df["inventory_value"] = (
        pd.to_numeric(df["price"], errors="coerce").fillna(0)
        * pd.to_numeric(df["stock_levels"], errors="coerce").fillna(0)
    )

    order_statuses = []
    for _, row in df.iterrows():
        availability = pd.to_numeric(row.get("availability", 0), errors="coerce")
        order_quantity = pd.to_numeric(row.get("order_quantities", 0), errors="coerce")
        if pd.isna(availability):
            availability = 0
        if pd.isna(order_quantity):
            order_quantity = 0

        if availability > order_quantity:
            order_statuses.append("Healthy")
        elif order_quantity > 0:
            order_statuses.append("Pending")
        else:
            order_statuses.append("Low Stock")

    df["order_status"] = order_statuses
    return df


def render_comparison_metric_cards(period_values):
    if len(period_values) != 2:
        return

    first_label, first_df = period_values[0]
    second_label, second_df = period_values[1]

    st.markdown("#### Comparison summary")
    left, right = st.columns(2, gap="large")

    def format_value(value, fmt="{:,}"):
        return fmt.format(value) if value is not None else "0"

    with left:
        st.markdown(f"**{first_label}**")
        st.metric("Records", len(first_df))
        st.metric("Total revenue", f"${format_value(round(first_df['revenue_generated'].sum(), 2), '{:,.2f}')}")
        st.metric("Total shipping costs", f"${format_value(round(first_df['shipping_costs'].sum(), 2), '{:,.2f}')}")
        st.metric("Avg shipping cost", f"${format_value(round(first_df['shipping_costs'].mean() if len(first_df) else 0, 2), '{:,.2f}')}")
        st.metric("Avg lead time", f"{format_value(round(first_df['lead_times'].mean() if len(first_df) else 0, 2), '{:,.2f}')}")
        st.metric("Avg defect rate", f"{format_value(round(first_df['defect_rates'].mean() if len(first_df) else 0, 2), '{:,.2f}')}")
        st.metric("Total production volume", f"{format_value(int(first_df['production_volumes'].sum()) if len(first_df) else 0, '{:,}')}")
        st.metric("Revenue per record", f"${format_value(round(first_df['revenue_generated'].sum() / len(first_df), 2) if len(first_df) else 0, '{:,.2f}')}")

    with right:
        st.markdown(f"**{second_label}**")
        st.metric("Records", len(second_df))
        st.metric("Total revenue", f"${format_value(round(second_df['revenue_generated'].sum(), 2), '{:,.2f}')}")
        st.metric("Total shipping costs", f"${format_value(round(second_df['shipping_costs'].sum(), 2), '{:,.2f}')}")
        st.metric("Avg shipping cost", f"${format_value(round(second_df['shipping_costs'].mean() if len(second_df) else 0, 2), '{:,.2f}')}")
        st.metric("Avg lead time", f"{format_value(round(second_df['lead_times'].mean() if len(second_df) else 0, 2), '{:,.2f}')}")
        st.metric("Avg defect rate", f"{format_value(round(second_df['defect_rates'].mean() if len(second_df) else 0, 2), '{:,.2f}')}")
        st.metric("Total production volume", f"{format_value(int(second_df['production_volumes'].sum()) if len(second_df) else 0, '{:,}')}")
        st.metric("Revenue per record", f"${format_value(round(second_df['revenue_generated'].sum() / len(second_df), 2) if len(second_df) else 0, '{:,.2f}')}")


def plot_split_period_charts(period_values, metric, chart_type, title, y_label=None):
    if len(period_values) != 2:
        return

    first_label, first_df = period_values[0]
    second_label, second_df = period_values[1]

    c1, c2 = st.columns(2)
    with c1:
        st.subheader(f"{title} — {first_label}")
        if chart_type == "histogram":
            fig = px.histogram(first_df, x=metric, nbins=20, title=f"{title} ({first_label})")
        elif chart_type == "box":
            fig = px.box(first_df, y=metric, title=f"{title} ({first_label})")
        elif chart_type == "bar":
            grouped = first_df.groupby("product_type")[metric].sum().reset_index()
            fig = px.bar(grouped, x="product_type", y=metric, color="product_type", title=f"{title} ({first_label})")
        else:
            fig = px.scatter(first_df, x="production_volumes", y=metric, color="product_type", title=f"{title} ({first_label})")
        fig.update_layout(height=620, margin=dict(t=50, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader(f"{title} — {second_label}")
        if chart_type == "histogram":
            fig = px.histogram(second_df, x=metric, nbins=20, title=f"{title} ({second_label})")
        elif chart_type == "box":
            fig = px.box(second_df, y=metric, title=f"{title} ({second_label})")
        elif chart_type == "bar":
            grouped = second_df.groupby("product_type")[metric].sum().reset_index()
            fig = px.bar(grouped, x="product_type", y=metric, color="product_type", title=f"{title} ({second_label})")
        else:
            fig = px.scatter(second_df, x="production_volumes", y=metric, color="product_type", title=f"{title} ({second_label})")
        fig.update_layout(height=620, margin=dict(t=50, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)


def get_comparison_periods(df: pd.DataFrame, mode: str, option: str):
    df = add_period_columns(df)
    if df.empty:
        return []

    latest_date = df["date"].max()
    if mode == "Month":
        latest_period = latest_date.to_period("M")
        if option == "This month vs last month":
            current_period = latest_period
            previous_period = latest_period - 1
        else:
            current_period = latest_period - 1
            previous_period = latest_period - 2

        return [
            (previous_period.strftime("%b %Y"), df[df["month_period"] == previous_period]),
            (current_period.strftime("%b %Y"), df[df["month_period"] == current_period]),
        ]

    # Week comparison
    week_start = latest_date - pd.to_timedelta(latest_date.weekday(), unit="D")
    if option == "This week vs last week":
        current_week = week_start
        last_week = week_start - pd.Timedelta(days=7)
    else:
        current_week = week_start - pd.Timedelta(days=7)
        last_week = week_start - pd.Timedelta(days=14)

    return [
        (f"Week of {last_week.strftime('%b %d, %Y')}", df[df["week_start"] == last_week]),
        (f"Week of {current_week.strftime('%b %d, %Y')}", df[df["week_start"] == current_week]),
    ]

# Initialize database
init_database()

st.title("📊 Supply Chain Analytics Dashboard")
st.markdown("Real-time analytics dashboard powered by MySQL database")

# Sidebar filters
st.sidebar.markdown("### 🔍 Filters")

product_types = get_unique_values("product_type")
selected_products = st.sidebar.multiselect(
    "Product Type",
    product_types,
    default=product_types if product_types else []
)

supplier_names = get_unique_values("supplier_name")
selected_suppliers = st.sidebar.multiselect(
    "Supplier Name",
    supplier_names,
    default=supplier_names if supplier_names else []
)

min_date, max_date = get_date_range()
if min_date and max_date:
    date_range = st.sidebar.date_input(
        "Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date,
    )
    start_date, end_date = date_range if isinstance(date_range, tuple) and len(date_range) == 2 else (min_date, max_date)
else:
    start_date, end_date = None, None

comparison_mode = st.sidebar.radio(
    "Compare by",
    ["Month", "Week"],
    horizontal=True,
)

comparison_option = st.sidebar.selectbox(
    "Compare Period",
    [
        "This month vs last month" if comparison_mode == "Month" else "This week vs last week",
        "Last month vs previous month" if comparison_mode == "Month" else "Last week vs previous week",
    ],
)

# Apply filters
filters = {
    "product_type": selected_products if selected_products else product_types,
    "supplier_name": selected_suppliers if selected_suppliers else supplier_names,
    "start_date": start_date,
    "end_date": end_date,
}

filtered = load_data_from_sql(filters)

if len(filtered) == 0:
    st.warning("⚠️ No data found. Please add data using the Data Entry page.")
    st.stop()

period_values = get_comparison_periods(filtered, comparison_mode, comparison_option)
if period_values:
    period_comparison_df = build_period_summary(filtered, period_values, comparison_mode)
else:
    period_comparison_df = pd.DataFrame()

# Metrics
st.markdown(
    """
    <div class="dashboard-row">
        <div class="dashboard-card">
            <div class="dashboard-card-title">Total Traffic</div>
            <div class="dashboard-card-value">{total_records}</div>
            <div class="dashboard-card-note">entries across the selected period</div>
        </div>
        <div class="dashboard-card">
            <div class="dashboard-card-title">Total Revenue</div>
            <div class="dashboard-card-value">${total_revenue}</div>
            <div class="dashboard-card-note">revenue generated from sales</div>
        </div>
        <div class="dashboard-card">
            <div class="dashboard-card-title">Performance</div>
            <div class="dashboard-card-value">{avg_shipping_cost}</div>
            <div class="dashboard-card-note">average shipping cost</div>
        </div>
    </div>
    """.format(
        total_records=len(filtered),
        total_revenue=f"{filtered['revenue_generated'].sum():,.0f}",
        avg_shipping_cost=f"${filtered['shipping_costs'].mean():.2f}",
    ),
    unsafe_allow_html=True,
)

business_df = calculate_business_components(filtered)

st.markdown("---")
st.subheader("💼 Business Components")

kpi_cols = st.columns(3)
with kpi_cols[0]:
    st.metric("Profit", f"${business_df['profit'].sum():,.2f}")
with kpi_cols[1]:
    st.metric("Inventory Value", f"${business_df['inventory_value'].sum():,.2f}")
with kpi_cols[2]:
    st.metric("Order Status", f"{business_df['order_status'].value_counts().idxmax()}" )

perf_cols = st.columns(3)
with perf_cols[0]:
    st.metric("Delivery Performance", f"{business_df['shipping_times'].mean():.1f} days avg")
with perf_cols[1]:
    top_customer = business_df.groupby("customer_demographics")["revenue_generated"].sum().sort_values(ascending=False)
    st.metric("Top Customer Segment", top_customer.index[0] if not top_customer.empty else "N/A")
with perf_cols[2]:
    supplier_score = business_df.groupby("supplier_name")["defect_rates"].mean().sort_values()
    st.metric("Best Supplier", supplier_score.index[0] if not supplier_score.empty else "N/A")

c1, c2 = st.columns(2, gap="large")
with c1:
    profit_summary = business_df.groupby("product_type")["profit"].sum().reset_index().sort_values("profit", ascending=False)
    fig_profit = px.bar(profit_summary, x="product_type", y="profit", color="product_type", title="Profit by Product Type")
    fig_profit.update_layout(height=420, margin=dict(t=40, b=20, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#14182d")
    st.plotly_chart(fig_profit, use_container_width=True)

with c2:
    order_status_counts = business_df["order_status"].value_counts().reset_index()
    order_status_counts.columns = ["status", "count"]
    fig_orders = px.pie(order_status_counts, names="status", values="count", title="Order Status")
    fig_orders.update_layout(height=420, margin=dict(t=40, b=20, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#14182d")
    st.plotly_chart(fig_orders, use_container_width=True)

c1, c2 = st.columns(2, gap="large")
with c1:
    delivery_summary = business_df.groupby("shipping_carriers").agg(
        avg_shipping_time=("shipping_times", "mean"),
        avg_shipping_cost=("shipping_costs", "mean"),
        shipments=("sku", "count"),
    ).reset_index()
    fig_delivery = px.bar(delivery_summary, x="shipping_carriers", y="avg_shipping_time", color="shipping_carriers", title="Delivery Performance by Carrier")
    fig_delivery.update_layout(height=420, margin=dict(t=40, b=20, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#14182d")
    st.plotly_chart(fig_delivery, use_container_width=True)

with c2:
    customer_summary = business_df.groupby("customer_demographics")["revenue_generated"].sum().reset_index().sort_values("revenue_generated", ascending=False).head(8)
    fig_customers = px.bar(customer_summary, x="customer_demographics", y="revenue_generated", color="customer_demographics", title="Top Customers by Revenue")
    fig_customers.update_layout(height=420, margin=dict(t=40, b=20, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#14182d")
    st.plotly_chart(fig_customers, use_container_width=True)

c1, c2 = st.columns(2, gap="large")
with c1:
    supplier_summary = business_df.groupby("supplier_name").agg(
        total_revenue=("revenue_generated", "sum"),
        avg_defect_rate=("defect_rates", "mean"),
        avg_lead_time=("lead_times", "mean"),
    ).reset_index().sort_values("total_revenue", ascending=False).head(8)
    fig_supplier = px.scatter(supplier_summary, x="avg_defect_rate", y="total_revenue", size="avg_lead_time", color="supplier_name", hover_name="supplier_name", title="Supplier Performance")
    fig_supplier.update_layout(height=420, margin=dict(t=40, b=20, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#14182d")
    st.plotly_chart(fig_supplier, use_container_width=True)

with c2:
    inventory_summary = business_df.groupby("product_type")["inventory_value"].sum().reset_index().sort_values("inventory_value", ascending=False)
    fig_inventory = px.bar(inventory_summary, x="product_type", y="inventory_value", color="product_type", title="Inventory Value by Product Type")
    fig_inventory.update_layout(height=420, margin=dict(t=40, b=20, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#14182d")
    st.plotly_chart(fig_inventory, use_container_width=True)

if not period_comparison_df.empty:
    st.markdown("---")
    st.subheader("📅 Period Comparison")
    st.table(period_comparison_df)

if period_values:
    st.markdown("---")
    st.subheader("📊 Period Comparison Visualizations")
    render_comparison_metric_cards(period_values)
    plot_split_period_charts(period_values, "revenue_generated", "histogram", "Revenue Distribution")
    plot_split_period_charts(period_values, "shipping_costs", "box", "Shipping Cost Distribution")
    plot_split_period_charts(period_values, "revenue_generated", "bar", "Revenue by Product Type")
    plot_split_period_charts(period_values, "production_volumes", "scatter", "Production Volumes vs Revenue")
    st.markdown("---")

# Main visualizations
st.markdown(
    """
    <div class="dashboard-row">
        <div class="dashboard-chart-card">
            <h3>Revenue Distribution</h3>
        </div>
        <div class="dashboard-chart-card">
            <h3>Shipping Costs Box Plot</h3>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2 = st.columns(2, gap="large")

with c1:
    fig_hist = px.histogram(filtered, x="revenue_generated", nbins=20, title="Revenue Distribution")
    fig_hist.update_layout(height=520, margin=dict(t=30, b=20, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#14182d")
    st.plotly_chart(fig_hist, use_container_width=True)

with c2:
    fig_box = px.box(filtered, y="shipping_costs", title="Shipping Costs")
    fig_box.update_layout(height=520, margin=dict(t=30, b=20, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#14182d")
    st.plotly_chart(fig_box, use_container_width=True)

st.markdown(
    """
    <div class="dashboard-row">
        <div class="dashboard-chart-card">
            <h3>Revenue by Product Type</h3>
        </div>
        <div class="dashboard-chart-card">
            <h3>Production Volumes vs Revenue</h3>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2 = st.columns(2, gap="large")

with c1:
    revenue_product = filtered.groupby("product_type")["revenue_generated"].sum().reset_index()
    fig_bar = px.bar(revenue_product, x="product_type", y="revenue_generated", color="product_type", title="Revenue by Product Type")
    fig_bar.update_layout(height=520, margin=dict(t=30, b=20, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#14182d")
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    fig_scatter = px.scatter(filtered, x="production_volumes", y="revenue_generated", color="product_type", title="Production Volumes vs Revenue")
    fig_scatter.update_layout(height=520, margin=dict(t=30, b=20, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#14182d")
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# Correlation & distribution cards
st.markdown(
    """
    <div class="dashboard-row">
        <div class="dashboard-small-card">
            <h4>Health Care</h4>
            <p>Track performance metrics for the health care product category and identify growth opportunities.</p>
        </div>
        <div class="dashboard-small-card">
            <h4>Weather Updates</h4>
            <p>Monitor external conditions that impact shipping and logistics performance in real time.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2 = st.columns(2, gap="large")

with c1:
    fig_heatmap = px.imshow(filtered.select_dtypes(include=['number']).corr(), text_auto=".2f", title="Correlation Matrix")
    fig_heatmap.update_layout(height=520, margin=dict(t=30, b=20, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#14182d")
    st.plotly_chart(fig_heatmap, use_container_width=True)

with c2:
    pie_data = filtered["product_type"].value_counts().reset_index()
    pie_data.columns = ["product_type", "count"]
    fig_pie = px.pie(pie_data, names="product_type", values="count", title="Product Type Share")
    fig_pie.update_layout(height=520, margin=dict(t=30, b=20, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#14182d")
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")
st.subheader("📋 Detailed Data")
st.dataframe(filtered, use_container_width=True)

st.info("💡 Tip: Use the sidebar filters to drill down into specific data. All null values are filled with 0 for numeric columns and 'N/A' for text columns.")
