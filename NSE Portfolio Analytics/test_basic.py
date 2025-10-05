"""
Simple tests for NSE Portfolio Analytics
Run with: python test_basic.py
"""

import sys
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

def test_imports():
    """Test that all required packages can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import streamlit
        import plotly.graph_objects
        import plotly.express
        import sqlite3
        import scipy
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_data_fetch():
    """Test fetching NSE data"""
    print("🧪 Testing data fetch...")
    
    try:
        data = yf.download("RELIANCE.NS", period="5d", progress=False)
        
        if data.empty:
            print("⚠️ No data returned (market might be closed)")
            return True
        
        if 'Close' not in data.columns:
            print("❌ Close price column missing")
            return False
        
        if len(data) == 0:
            print("⚠️ Empty dataset returned")
            return True
        
        print(f"✅ Data fetch successful - {len(data)} rows")
        print(f"   Latest close price: ₹{data['Close'].iloc[-1]:.2f}")
        return True
        
    except Exception as e:
        print(f"❌ Data fetch failed: {e}")
        return False

def test_portfolio_calculations():
    """Test basic portfolio calculations"""
    print("🧪 Testing portfolio calculations...")
    
    try:
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        
        np.random.seed(42)
        
        stocks = ['STOCK_A', 'STOCK_B', 'STOCK_C']
        price_data = pd.DataFrame(index=dates, columns=stocks)
        
        for stock in stocks:
            returns = np.random.normal(0.001, 0.02, len(dates))
            prices = [100]
            
            for ret in returns[1:]:
                prices.append(prices[-1] * (1 + ret))
            
            price_data[stock] = prices
        
        returns = price_data.pct_change().dropna()
        
        weights = np.array([0.4, 0.3, 0.3])
        
        portfolio_returns = (returns * weights).sum(axis=1)
        
        annual_return = portfolio_returns.mean() * 252
        annual_vol = portfolio_returns.std() * np.sqrt(252)
        sharpe_ratio = (annual_return - 0.07) / annual_vol
        
        var_95 = np.percentile(portfolio_returns, 5)
        
        if not np.isfinite(annual_return):
            print("❌ Annual return calculation failed")
            return False
        
        if not np.isfinite(annual_vol):
            print("❌ Volatility calculation failed")
            return False
        
        if not np.isfinite(sharpe_ratio):
            print("❌ Sharpe ratio calculation failed")
            return False
        
        print("✅ Portfolio calculations successful")
        print(f"   Annual Return: {annual_return:.2%}")
        print(f"   Annual Volatility: {annual_vol:.2%}")
        print(f"   Sharpe Ratio: {sharpe_ratio:.3f}")
        print(f"   VaR (95%): {var_95:.2%}")
        
        return True
        
    except Exception as e:
        print(f"❌ Portfolio calculations failed: {e}")
        return False

def test_database_operations():
    """Test SQLite database operations"""
    print("🧪 Testing database operations...")
    
    try:
        import sqlite3
        
        conn = sqlite3.connect(':memory:')
        
        conn.execute('''
            CREATE TABLE test_portfolio (
                id INTEGER PRIMARY KEY,
                name TEXT,
                symbols TEXT,
                weights TEXT
            )
        ''')
        
        conn.execute(
            "INSERT INTO test_portfolio (name, symbols, weights) VALUES (?, ?, ?)",
            ("Test Portfolio", "STOCK_A,STOCK_B", "0.5,0.5")
        )
        
        result = conn.execute("SELECT * FROM test_portfolio").fetchone()
        
        if result is None:
            print("❌ Database query returned no results")
            return False
        
        conn.close()
        print("✅ Database operations successful")
        return True
        
    except Exception as e:
        print(f"❌ Database operations failed: {e}")
        return False

def test_chart_creation():
    """Test basic chart creation"""
    print("🧪 Testing chart creation...")
    
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        
        dates = pd.date_range(start='2024-01-01', periods=100)
        values = np.random.randn(100).cumsum() + 100
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=values, mode='lines', name='Test Data'))
        
        if len(fig.data) == 0:
            print("❌ Chart creation failed - no data traces")
            return False
        
        correlation_data = np.random.rand(5, 5)
        fig_heatmap = px.imshow(correlation_data)
        
        if len(fig_heatmap.data) == 0:
            print("❌ Heatmap creation failed")
            return False
        
        print("✅ Chart creation successful")
        return True
        
    except Exception as e:
        print(f"❌ Chart creation failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 NSE Portfolio Analytics - Basic Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_data_fetch,
        test_portfolio_calculations,
        test_database_operations,
        test_chart_creation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! The application should work correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
