# 🚀 Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies (1 min)
```bash
pip install -r requirements.txt
```

### Step 2: Setup MySQL (2 min)

**Option A: Using Docker (Easiest)**
```bash
docker run -d --name mysql-supply-chain -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=supply_chain -p 3306:3306 mysql:latest
```

**Option B: Local MySQL**
- Download from https://dev.mysql.com/downloads/mysql/
- Run installer and follow setup
- Default: host=localhost, user=root

### Step 3: Configure Credentials (1 min)

Create `.streamlit/secrets.toml`:
```toml
[mysql]
host = "localhost"
user = "root"
password = "root"
database = "supply_chain"
```

### Step 4: Run App (1 min)
```bash
streamlit run combined_app.py
```

✅ Done! App opens at http://localhost:8501

---

## First Time Usage

1. **Home Page** → Setup instructions
2. **Data Entry** → Add some records
3. **Dashboard** → View visualizations
4. **Filters** → Try filtering data

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Access denied` | Check username/password in secrets.toml |
| `Can't connect to MySQL` | Start MySQL service or Docker |
| `No module named 'mysql'` | Run `pip install mysql-connector-python` |
| `No data found` | Add records via Data Entry page |

---

## MySQL Quick Commands

```bash
# Connect to MySQL
mysql -u root -p

# Inside MySQL:
SHOW DATABASES;
USE supply_chain;
SHOW TABLES;
SELECT COUNT(*) FROM supply_chain_data;

# Exit
EXIT;
```

---

## Project Structure
```
portfolio_project/
├── combined_app.py           # Main app
├── pages/
│   ├── 01_data_entry.py      # Add data
│   └── 02_dashboard.py       # View analytics
├── utils/
│   └── db.py                 # Database code
├── requirements.txt          # Dependencies
└── README.md                 # Full docs
```

---

## Interview Talking Points

This project demonstrates:

✅ **Full-Stack Web Application**
- Frontend: Streamlit
- Backend: Python with MySQL
- Database: Relational SQL design

✅ **Database Skills**
- Table schema design
- Data insertion & queries
- Connection management
- NULL handling

✅ **Data Visualization**
- 6 different chart types
- Interactive filtering
- Real-time updates

✅ **Software Engineering**
- Multi-page architecture
- Secret management
- Error handling
- Code organization

✅ **User Experience**
- Form validation
- Intuitive navigation
- Professional styling
- Helpful messages

---

## Next Steps

1. ✅ Get app running
2. ✅ Add sample data via Data Entry
3. ✅ Explore Dashboard visualizations
4. ✅ Try different filters
5. ✅ Export data table (right-click)
6. ✅ Deploy to Streamlit Cloud (optional)

---

**Need Help?** Check README.md for detailed documentation.
