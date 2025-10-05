# 🚀 NSE Portfolio Analytics - Complete Setup Guide

## What This Is

A **working, deployable** NSE portfolio risk analysis tool that you can run in 5 minutes. This is a simplified but fully functional version that actually works with real NSE data.

## ✅ What Actually Works

- ✅ **Real NSE stock data** via Yahoo Finance (free, no API key needed)
- ✅ **Portfolio risk analysis** - VaR, Sharpe ratio, correlations
- ✅ **Interactive dashboard** - Charts, tables, exports
- ✅ **Save/load portfolios** - SQLite database (no setup needed)
- ✅ **Multiple portfolio templates** - Ready-to-use samples
- ✅ **Export to Excel/CSV** - Download your analysis
- ✅ **Docker deployment** - One command deployment

## 🚀 Quick Start (5 Minutes)

### Option 1: Local Python Setup
```bash
# 1. Download the files
git clone <this-repo> or download ZIP

# 2. Navigate to directory
cd simple-nse-portfolio

# 3. Run setup script (Linux/Mac)
chmod +x deploy.sh
./deploy.sh

# OR Manual setup:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py

# 5. Open browser to http://localhost:8501
```

### Option 2: Docker (Even Easier)
```bash
# 1. Build and run
docker build -t nse-portfolio .
docker run -p 8501:8501 nse-portfolio

# 2. Open browser to http://localhost:8501
```

## 📊 How to Use

### 1. Start with Sample Portfolios
- Open the app at http://localhost:8501
- In sidebar, select "Sample Portfolio"
- Choose "NIFTY Top 10" for a quick demo
- Click around and explore the interface

### 2. Create Custom Portfolio
- Select "Custom Portfolio" in sidebar
- Enter NSE stock symbols (like RELIANCE, TCS, HDFCBANK)
- Adjust weights using sliders
- Save your portfolio for later use

### 3. Analyze Risk Metrics
- View key metrics: Return, Volatility, Sharpe Ratio
- Check VaR (Value at Risk) calculations
- Review correlation matrix
- Compare against NIFTY 50

### 4. Export Results
- Use export buttons to download Excel/CSV files
- Save portfolio configurations
- Generate reports for analysis

## 🎯 Key Features

### Risk Analytics
- **Value at Risk (VaR)**: 95% and 99% confidence levels
- **Sharpe Ratio**: Risk-adjusted return measurement
- **Maximum Drawdown**: Worst peak-to-trough decline
- **Volatility**: Annualized portfolio volatility
- **Correlation Analysis**: Cross-asset correlations

### Portfolio Tools
- **Stock Screening**: Filter by sectors and metrics
- **Weight Optimization**: Manual portfolio balancing
- **Sector Allocation**: View portfolio by sectors
- **Performance Comparison**: Against NIFTY 50 benchmark

### Data & Storage
- **Real-time NSE data**: Via Yahoo Finance API
- **Local database**: SQLite for portfolio storage
- **Data caching**: 1-hour cache for performance
- **Multiple timeframes**: 1Y, 2Y, 5Y, 10Y, Max

## 💡 Sample Portfolios Included

1. **NIFTY Top 10**: Equal-weighted top 10 NIFTY stocks
2. **Banking Focus**: Major banking sector stocks
3. **IT Sector**: Technology companies focus
4. **Conservative Balanced**: Low-risk diversified portfolio
5. **Growth Focused**: Higher growth potential stocks
6. **Dividend Yield**: High dividend-paying stocks

## ⚠️ Important Notes

### Data Limitations
- **Market hours**: Data may not update when markets are closed
- **Yahoo Finance**: Free data source, occasional delays possible
- **NSE symbols**: Use correct NSE symbols (RELIANCE, not RELIANCE.NS)
- **Delisted stocks**: May not have current data

### Risk Warnings
- **Educational use only**: Not for actual investment decisions
- **Past performance**: Does not guarantee future results
- **Consult professionals**: Always seek qualified financial advice
- **Market risks**: All investments carry inherent risks

## 🐛 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# If you get import errors:
pip install --upgrade pip
pip install -r requirements.txt
```

**2. No Data Loading**
```bash
# Test data connection:
python test_basic.py
```

**3. Streamlit Won't Start**
```bash
# Check if port is free:
netstat -tulpn | grep :8501

# Try different port:
streamlit run app.py --server.port 8502
```

**4. Database Errors**
```bash
# Remove old database:
rm portfolio_data.db

# Restart application
```

### Data Issues
- **Empty charts**: Market might be closed, try sample data
- **Missing stocks**: Check NSE symbol spelling
- **Old data**: Restart app to refresh cache
- **Slow loading**: Normal for first-time data fetch

## 🔧 Customization

### Adding New Stocks
Edit `config.py` to add more stocks to the universe:
```python
NIFTY_50_STOCKS = [
    "RELIANCE", "TCS", "HDFCBANK", 
    "YOUR_STOCK_HERE"  # Add here
]
```

### Changing Risk Parameters
Modify risk settings in `config.py`:
```python
RISK_CONFIG = {
    'RISK_FREE_RATE': 0.07,  # Change risk-free rate
    'VAR_CONFIDENCE_LEVELS': [0.95, 0.99],  # VaR levels
    'MAX_POSITION_SIZE': 0.25,  # Maximum 25% position
}
```

### Adding New Portfolio Templates
Add templates in `config.py`:
```python
PORTFOLIO_TEMPLATES = {
    "Your Strategy": {
        "symbols": ["STOCK1", "STOCK2"],
        "weights": [0.5, 0.5],
        "risk_profile": "Moderate"
    }
}
```

## 📈 Performance

### Expected Performance
- **Startup time**: 10-30 seconds first run
- **Data loading**: 5-15 seconds per portfolio
- **Chart rendering**: 1-3 seconds
- **Export time**: 2-5 seconds

### Optimization Tips
- Use smaller time periods for faster loading
- Clear browser cache if charts seem slow
- Restart app daily to refresh data cache
- Use Docker for consistent performance

## 🚀 Production Deployment

### For Personal Use
```bash
# Run locally with auto-restart
streamlit run app.py --server.runOnSave true
```

### For Team Use
```bash
# Deploy with Docker on server
docker run -d -p 8501:8501 \
  --restart unless-stopped \
  --name nse-portfolio \
  nse-portfolio
```

### For Cloud Deployment
- **Heroku**: Use `streamlit run app.py` as startup command
- **AWS**: Deploy using Elastic Beanstalk or ECS
- **GCP**: Use Cloud Run with Docker container
- **DigitalOcean**: App Platform with Docker

## 📞 Support

### If You Need Help
1. **Run tests first**: `python test_basic.py`
2. **Check logs**: Look for error messages in terminal
3. **Try sample data**: Use built-in portfolios first
4. **Restart app**: Often fixes temporary issues

### Common Questions

**Q: Can I use this for real trading?**
A: No, this is for analysis and education only.

**Q: How accurate is the data?**
A: Yahoo Finance data is generally reliable but can have delays.

**Q: Can I add more advanced features?**
A: Yes, the code is modular and extensible.

**Q: Does this work outside India?**
A: Yes, but it's optimized for NSE stocks.

## 🎯 What Makes This Different

### vs Complex Solutions
- ✅ **Actually works** out of the box
- ✅ **No API keys** or complex setup required
- ✅ **Simple deployment** - one command
- ✅ **Real data** from reliable sources

### vs Simple Solutions
- ✅ **Professional analytics** - institutional-grade calculations
- ✅ **Interactive interface** - not just static charts
- ✅ **Persistent storage** - save and load portfolios
- ✅ **Export capabilities** - professional reports

## 🎉 Success Criteria

After setup, you should be able to:
- ✅ Open the dashboard in your browser
- ✅ Load a sample portfolio (NIFTY Top 10)
- ✅ See real stock prices and charts
- ✅ Calculate risk metrics (VaR, Sharpe ratio)
- ✅ Export analysis to Excel
- ✅ Save and load custom portfolios

**If you can do all the above, congratulations! You have a working NSE portfolio analytics platform.**
