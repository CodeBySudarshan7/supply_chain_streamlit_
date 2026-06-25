import os
import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

CSV_FALLBACK_PATH = "supply_chain_data_sequential_date.csv"


def get_db_connection():
    """Create a fresh MySQL connection."""
    mysql_config = {
        "host": "localhost",
        "user": "root",
        "password": "root",
        "database": "supply_chain",
    }

    try:
        if hasattr(st, "secrets") and "mysql" in st.secrets:
            secret_mysql = st.secrets.get("mysql", {})
            mysql_config.update({
                "host": secret_mysql.get("host", mysql_config["host"]),
                "user": secret_mysql.get("user", mysql_config["user"]),
                "password": secret_mysql.get("password", mysql_config["password"]),
                "database": secret_mysql.get("database", mysql_config["database"]),
            })
    except Exception:
        pass

    try:
        return mysql.connector.connect(
            host=mysql_config["host"],
            user=mysql_config["user"],
            password=mysql_config["password"],
            database=mysql_config["database"],
            autocommit=False,
        )
    except mysql.connector.Error as e:
        st.error(f"Database connection failed: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected connection error: {e}")
        return None


def normalize_csv_df(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize CSV column names and types to match the SQL schema."""
    rename_map = {
        "Date": "date",
        "Product type": "product_type",
        "SKU": "sku",
        "Price": "price",
        "Availability": "availability",
        "Number of products sold": "number_of_products_sold",
        "Revenue generated": "revenue_generated",
        "Customer demographics": "customer_demographics",
        "Stock levels": "stock_levels",
        "Lead times": "lead_times",
        "Order quantities": "order_quantities",
        "Shipping times": "shipping_times",
        "Shipping carriers": "shipping_carriers",
        "Shipping costs": "shipping_costs",
        "Supplier name": "supplier_name",
        "Location": "location",
        "Lead time": "lead_time",
        "Production volumes": "production_volumes",
        "Manufacturing lead time": "manufacturing_lead_time",
        "Manufacturing costs": "manufacturing_costs",
        "Inspection results": "inspection_results",
        "Defect rates": "defect_rates",
        "Transportation modes": "transportation_modes",
        "Routes": "routes",
        "Costs": "costs",
    }
    df = df.rename(columns=rename_map)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    numeric_columns = [
        "price",
        "availability",
        "number_of_products_sold",
        "revenue_generated",
        "stock_levels",
        "lead_times",
        "order_quantities",
        "shipping_times",
        "shipping_costs",
        "lead_time",
        "production_volumes",
        "manufacturing_lead_time",
        "manufacturing_costs",
        "defect_rates",
        "costs",
    ]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    text_columns = [
        "product_type",
        "sku",
        "customer_demographics",
        "shipping_carriers",
        "supplier_name",
        "location",
        "inspection_results",
        "transportation_modes",
        "routes",
    ]
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].fillna("N/A").astype(str)

    columns = [
        "date",
        "product_type",
        "sku",
        "price",
        "availability",
        "number_of_products_sold",
        "revenue_generated",
        "customer_demographics",
        "stock_levels",
        "lead_times",
        "order_quantities",
        "shipping_times",
        "shipping_carriers",
        "shipping_costs",
        "supplier_name",
        "location",
        "lead_time",
        "production_volumes",
        "manufacturing_lead_time",
        "manufacturing_costs",
        "inspection_results",
        "defect_rates",
        "transportation_modes",
        "routes",
        "costs",
    ]

    missing_columns = [col for col in columns if col not in df.columns]
    for col in missing_columns:
        df[col] = None

    return df[columns]


def load_data_from_csv(csv_path: str = CSV_FALLBACK_PATH) -> pd.DataFrame:
    """Load the fallback CSV dataset and normalize it."""
    if not os.path.exists(csv_path):
        return pd.DataFrame()

    df = pd.read_csv(csv_path)
    return normalize_csv_df(df)


def init_database():
    """Create supply chain table if it doesn't exist and seed it on first run."""
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS supply_chain_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE,
            product_type VARCHAR(50),
            sku VARCHAR(50),
            price DECIMAL(10, 2),
            availability INT,
            number_of_products_sold INT,
            revenue_generated DECIMAL(12, 2),
            customer_demographics VARCHAR(50),
            stock_levels INT,
            lead_times INT,
            order_quantities INT,
            shipping_times INT,
            shipping_carriers VARCHAR(50),
            shipping_costs DECIMAL(10, 2),
            supplier_name VARCHAR(100),
            location VARCHAR(100),
            lead_time INT,
            production_volumes INT,
            manufacturing_lead_time INT,
            manufacturing_costs DECIMAL(10, 2),
            inspection_results VARCHAR(50),
            defect_rates DECIMAL(5, 2),
            transportation_modes VARCHAR(50),
            routes VARCHAR(50),
            costs DECIMAL(10, 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY idx_unique_row (date, sku, supplier_name)
        )
        """)
        conn.commit()
    except Exception as e:
        st.error(f"Error creating table: {e}")
        return False
    finally:
        cursor.close()
        if conn.is_connected():
            conn.close()

    row_count = get_table_row_count()
    csv_rows = len(load_data_from_csv())
    if csv_rows > 0 and row_count < csv_rows:
        imported = import_csv_data()
        if imported > 0:
            st.info(f"Imported {imported} rows from CSV into MySQL.")
            return True

    return True


def get_table_row_count():
    """Return the number of rows in the supply_chain_data table."""
    conn = get_db_connection()
    if conn is None:
        return 0

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM supply_chain_data")
        count = cursor.fetchone()[0]
        cursor.close()
        return count
    except Exception as e:
        st.warning(f"Error counting rows: {e}")
        return 0
    finally:
        if conn.is_connected():
            conn.close()


def import_csv_data(csv_path: str = CSV_FALLBACK_PATH) -> int:
    """Import data from the local CSV file into the SQL table."""
    if not os.path.exists(csv_path):
        return 0

    df = load_data_from_csv(csv_path)
    if df.empty:
        return 0

    rows = [
        tuple(row[col] if pd.notna(row[col]) else None for col in df.columns)
        for _, row in df.iterrows()
    ]

    if not rows:
        return 0

    conn = get_db_connection()
    if conn is None:
        return 0

    try:
        cursor = conn.cursor()
        placeholders = ", ".join(["%s"] * len(df.columns))
        columns = ", ".join(df.columns)
        sql = f"INSERT INTO supply_chain_data ({columns}) VALUES ({placeholders})"
        cursor.executemany(sql, rows)
        conn.commit()
        cursor.close()
        return len(rows)
    except mysql.connector.Error as e:
        st.error(f"Error importing CSV data: {e}")
        return 0
    except Exception as e:
        st.error(f"Error importing CSV data: {e}")
        return 0
    finally:
        if conn.is_connected():
            conn.close()


def insert_record(data_dict):
    """Insert a single record into the database."""
    conn = get_db_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        columns = ", ".join(data_dict.keys())
        placeholders = ", ".join(["%s"] * len(data_dict))
        sql = f"INSERT INTO supply_chain_data ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(data_dict.values()))
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        st.error(f"Error inserting record: {e}")
        return False
    finally:
        if conn.is_connected():
            conn.close()


def apply_filters_to_dataframe(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    if filters is None or df.empty:
        return df

    if "product_type" in filters and filters["product_type"]:
        df = df[df["product_type"].isin(filters["product_type"])]

    if "supplier_name" in filters and filters["supplier_name"]:
        df = df[df["supplier_name"].isin(filters["supplier_name"])]

    if "start_date" in filters and filters["start_date"] is not None:
        df = df[df["date"] >= pd.to_datetime(filters["start_date"])]

    if "end_date" in filters and filters["end_date"] is not None:
        df = df[df["date"] <= pd.to_datetime(filters["end_date"])]

    return df


def load_data_from_sql(filters=None):
    """Load data from SQL with optional filters, falling back to CSV when needed."""
    df = pd.DataFrame()
    conn = get_db_connection()
    if conn is not None:
        try:
            query = "SELECT * FROM supply_chain_data WHERE 1=1"
            
            if filters:
                if "product_type" in filters and filters["product_type"]:
                    product_types = "', '".join(filters["product_type"])
                    query += f" AND product_type IN ('{product_types}')"

                if "supplier_name" in filters and filters["supplier_name"]:
                    suppliers = "', '".join(filters["supplier_name"])
                    query += f" AND supplier_name IN ('{suppliers}')"

                if "start_date" in filters and filters["start_date"] is not None:
                    query += f" AND date >= '{filters['start_date']}'"

                if "end_date" in filters and filters["end_date"] is not None:
                    query += f" AND date <= '{filters['end_date']}'"

            query += " ORDER BY date DESC"
            df = pd.read_sql(query, conn)
        except Exception as e:
            st.warning(f"Error loading SQL data: {e}")
        finally:
            if conn.is_connected():
                conn.close()

    if df.empty:
        df = load_data_from_csv()
        if not df.empty and filters:
            df = apply_filters_to_dataframe(df, filters)

    if not df.empty:
        numeric_cols = df.select_dtypes(include=["number"]).columns
        df[numeric_cols] = df[numeric_cols].fillna(0)
        df = df.fillna("N/A")

    return df


def get_unique_values(column):
    """Get unique values for a specific column."""
    values = []
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT DISTINCT {column} FROM supply_chain_data WHERE {column} IS NOT NULL ORDER BY {column}")
            values = [row[0] for row in cursor.fetchall() if row[0] is not None]
            cursor.close()
        except Exception as e:
            st.warning(f"Error fetching {column}: {e}")
        finally:
            if conn.is_connected():
                conn.close()

    if not values:
        csv_df = load_data_from_csv()
        if not csv_df.empty and column in csv_df.columns:
            values = sorted(csv_df[column].dropna().unique().tolist())

    return values


def get_date_range():
    """Get min and max dates from database."""
    min_date, max_date = None, None
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT MIN(date), MAX(date) FROM supply_chain_data WHERE date IS NOT NULL")
            result = cursor.fetchone()
            cursor.close()
            if result and len(result) == 2:
                min_date, max_date = result[0], result[1]
        except Exception as e:
            st.warning(f"Error fetching date range: {e}")
        finally:
            if conn.is_connected():
                conn.close()

    if min_date is None or max_date is None:
        csv_df = load_data_from_csv()
        if not csv_df.empty and "date" in csv_df.columns:
            min_date = csv_df["date"].min()
            max_date = csv_df["date"].max()

    return min_date, max_date
