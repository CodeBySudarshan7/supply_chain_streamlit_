<<<<<<< HEAD
# Supply Chain Analytics Dashboard

A multi-page Streamlit application with MySQL integration for managing and visualizing supply chain data.

## Features

✨ **Multi-Page Application**
- Home page with navigation
- Data entry page for adding records
- Dashboard with real-time analytics

📊 **Analytics & Visualizations**
- Revenue distribution histogram
- Shipping costs box plots
- Revenue by product type bar charts
- Production volumes vs revenue scatter plots
- Correlation heatmap
- Product type distribution pie chart
- Interactive data table

💾 **MySQL Database Integration**
- Persistent data storage
- Automatic table creation
- Secure credential management
- Null value handling

🔍 **Smart Filtering**
- Filter by product type
- Filter by supplier name
- Filter by date range
- Real-time data updates

## Setup Instructions

### 1. Install Dependencies

```bash
pip install streamlit pandas plotly mysql-connector-python
```

### 2. Setup MySQL Database

#### Option A: MySQL Server (Recommended for Production)

```bash
# Install MySQL Server
# Windows: https://dev.mysql.com/downloads/mysql/
# Mac: brew install mysql
# Linux: sudo apt-get install mysql-server
```

Create database:
```sql
mysql -u root -p

CREATE DATABASE supply_chain;
EXIT;
```

#### Option B: Quick Test with Local MySQL

```bash
# Or use a Docker container
docker run -d \
  --name mysql-supply-chain \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=supply_chain \
  -p 3306:3306 \
  mysql:latest
```

### 3. Configure Credentials

Create `.streamlit/secrets.toml` (copy from `.streamlit/secrets.toml.example`):

```toml
[mysql]
host = "localhost"
user = "root"
password = "your_mysql_password"
database = "supply_chain"
```

**⚠️ IMPORTANT:** 
- Do NOT commit `secrets.toml` to version control
- This file is already in `.gitignore`
- Keep your database password secure

### 4. Run the Application

```bash
streamlit run combined_app.py
```

The app will automatically:
- Connect to MySQL
- Create the `supply_chain_data` table if it doesn't exist
- Open in your default browser at `http://localhost:8501`

## Project Structure

```
portfolio_project/
├── combined_app.py              # Main app (home page)
├── pages/
│   ├── 01_data_entry.py         # Data entry form page
│   └── 02_dashboard.py          # Analytics dashboard page
├── utils/
│   ├── __init__.py
│   └── db.py                    # Database utilities
├── .streamlit/
│   ├── config.toml              # Streamlit config
│   └── secrets.toml.example     # Credentials template
├── .gitignore                   # Git ignore file
├── requirements.txt             # Python dependencies
└── supply_chain_data.csv        # Original CSV (reference)
```

## File Descriptions

### combined_app.py
- Main entry point
- Home page with setup instructions
- Navigation to other pages
- Database initialization

### pages/01_data_entry.py
- Form to add new supply chain records
- 25 input fields for all data columns
- Automatic null value handling
- Direct MySQL insertion
- Success feedback

### pages/02_dashboard.py
- Analytics and visualizations
- Sidebar filters (product type, supplier, date range)
- 6 interactive Plotly charts
- Data metrics (total records, revenue, shipping cost)
- Detailed data table
- Null value auto-fill (0 for numbers, N/A for text)

### utils/db.py
- Database connection management
- Connection pooling with `@st.cache_resource`
- Table initialization
- Data insertion functions
- Data retrieval with filters
- Unique value fetching
- Date range queries

## Database Schema

**Table: `supply_chain_data`**

| Column | Type | Description |
|--------|------|-------------|
| id | INT AUTO_INCREMENT PRIMARY KEY | Unique record ID |
| date | DATE | Transaction date |
| product_type | VARCHAR(50) | haircare, skincare, cosmetics |
| sku | VARCHAR(50) | Stock keeping unit |
| price | DECIMAL(10, 2) | Unit price |
| availability | INT | Stock availability |
| number_of_products_sold | INT | Units sold |
| revenue_generated | DECIMAL(12, 2) | Total revenue |
| customer_demographics | VARCHAR(50) | Customer segment |
| stock_levels | INT | Current stock |
| lead_times | INT | Lead time in days |
| order_quantities | INT | Order quantity |
| shipping_times | INT | Shipping time in days |
| shipping_carriers | VARCHAR(50) | Carrier name |
| shipping_costs | DECIMAL(10, 2) | Shipping cost |
| supplier_name | VARCHAR(100) | Supplier name |
| location | VARCHAR(100) | Geographic location |
| production_volumes | INT | Production quantity |
| manufacturing_lead_time | INT | Manufacturing lead time |
| manufacturing_costs | DECIMAL(10, 2) | Manufacturing cost |
| inspection_results | VARCHAR(50) | QA result |
| defect_rates | DECIMAL(5, 2) | Defect percentage |
| transportation_modes | VARCHAR(50) | Transport method |
| routes | VARCHAR(50) | Delivery route |
| costs | DECIMAL(10, 2) | Total cost |
| created_at | TIMESTAMP | Record creation time |

## Usage Examples

### Adding Data
1. Click "📝 Go to Data Entry" from home
2. Fill all form fields
3. Click "✅ Submit Entry"
4. Data is immediately saved to MySQL

### Viewing Analytics
1. Click "📊 Go to Dashboard" from home
2. Use sidebar filters to drill down
3. View 6 different visualization types
4. Export data table if needed

### Filtering Data
- **Product Type**: Select one or multiple products
- **Supplier Name**: Select one or multiple suppliers
- **Date Range**: Pick start and end dates
- Filters automatically update all visualizations

## Null Value Handling

The app automatically handles missing values:

| Data Type | Null Handling |
|-----------|---------------|
| Numeric | Filled with `0` |
| Text | Filled with `N/A` |
| Date | Skipped in aggregations |

## Troubleshooting

### Connection Errors
```
Database connection failed: Access denied for user 'root'@'localhost'
```
✅ Check credentials in `.streamlit/secrets.toml`

### Table Already Exists
```
Error creating table: (1050, "Table 'supply_chain_data' already exists")
```
✅ Normal message - table exists and is ready to use

### No Data Display
```
No data found. Please add data using the Data Entry page.
```
✅ Add records via Data Entry page first

### MySQL Not Running
```
Connection Error: Can't connect to MySQL server
```
✅ Start MySQL service or Docker container

## Performance Notes

- **Connection Caching**: Uses `@st.cache_resource` for MySQL connections
- **Data Caching**: Uses `@st.cache_data` for query results
- **Null Filling**: Happens on query retrieval for efficiency
- **Indexing**: Consider adding indexes on frequently filtered columns (date, product_type, supplier_name)

## Security Best Practices

1. ✅ Credentials stored in `secrets.toml` (not in code)
2. ✅ `.gitignore` prevents accidental commits
3. ✅ Parameterized SQL queries prevent injection
4. ✅ Connection validation on startup
5. ⚠️ Use strong database passwords
6. ⚠️ Restrict database access to trusted networks
7. ⚠️ Use SSL for remote database connections

## Future Enhancements

- [ ] User authentication
- [ ] Data export to CSV/PDF
- [ ] Advanced analytics (forecasting)
- [ ] Real-time alerts
- [ ] Bulk data import
- [ ] Dashboard customization
- [ ] Email notifications
- [ ] API endpoints

## License

Your Project Name - MIT License

## Support

For issues or questions:
1. Check `.streamlit/config.toml` settings
2. Verify MySQL is running
3. Review error messages in terminal
4. Check `.streamlit/secrets.toml` credentials

---

**Ready to interview?** This app demonstrates:
✓ Multi-page web application architecture
✓ Database design and integration
✓ Real-time data visualization
✓ Form handling and validation
✓ Data persistence and null handling
✓ Professional UI/UX
=======
# supply_chain
📊 End-to-End Supply Chain Analytics Dashboard built using Python, Pandas, NumPy, MySQL, SQL, Streamlit, Plotly, Matplotlib, Seaborn, and Machine Learning. Features real-time data entry, automated weekly/monthly analysis, KPI tracking, interactive visualizations, and business insights for product, supplier, and logistics performance.
>>>>>>> c769753643822cb32746b9bae4ce9aa912b9df3a
