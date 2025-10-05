"""
NSE Portfolio Analytics Dashboard
A simplified but fully functional portfolio risk analysis tool for NSE stocks

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import sqlite3
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="NSE Portfolio Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #1f77b4;
    margin-bottom: 1rem;
}
.stAlert > div {
    background-color: #d4edda;
    border-color: #c3e6cb;
    color: #155724;
}
</style>
""", unsafe_allow_html=True)

# Initialize database
@st.cache_resource
def init_database():
    """Initialize SQLite database for storing portfolio data"""
    conn = sqlite3.connect('portfolio_data.db', check_same_thread=False)
    
    # Create tables
    conn.execute('''
        CREATE TABLE IF NOT EXISTS portfolios (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            symbols TEXT,
            weights TEXT,
            created_date TEXT
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS price_data (
            symbol TEXT,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            PRIMARY KEY (symbol, date)
        )
    ''')
    
    conn.commit()
    return conn

# NSE Stock Data Functions
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_nse_data(symbols, period="1y"):
    """Fetch NSE stock data using yfinance"""
    try:
        # Add .NS suffix for NSE stocks
        nse_symbols = [f"{symbol}.NS" for symbol in symbols]
        
        # Download data
        data = yf.download(nse_symbols, period=period, group_by='ticker', progress=False)
        
        if len(symbols) == 1:
            # Single stock - reshape data
            symbol = symbols[0]
            df = pd.DataFrame()
            df[symbol] = data['Close']
            return df.dropna()
        else:
            # Multiple stocks
            df = pd.DataFrame()
            for symbol in symbols:
                try:
                    df[symbol] = data[f"{symbol}.NS"]['Close']
                except:
                    st.warning(f"Could not fetch data for {symbol}")
            return df.dropna()
    
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_nifty50_data(period="1y"):
    """Fetch NIFTY 50 index data"""
    try:
        nifty = yf.download("^NSEI", period=period, progress=False)
        return nifty['Close'].dropna()
    except Exception as e:
        st.error(f"Error fetching NIFTY 50 data: {e}")
        return pd.Series()

# Risk Analytics Functions
def calculate_returns(price_data):
    """Calculate daily returns"""
    return price_data.pct_change().dropna()

def calculate_var(returns, confidence_level=0.05):
    """Calculate Value at Risk"""
    if len(returns) == 0:
        return 0
    return np.percentile(returns, confidence_level * 100)

def calculate_portfolio_metrics(price_data, weights, risk_free_rate=0.07):
    """Calculate comprehensive portfolio metrics"""
    returns = calculate_returns(price_data)
    
    if returns.empty:
        return {}
    
    # Portfolio returns
    portfolio_returns = (returns * weights).sum(axis=1)
    
    # Metrics
    annual_return = portfolio_returns.mean() * 252
    annual_vol = portfolio_returns.std() * np.sqrt(252)
    
    # Sharpe Ratio
    sharpe_ratio = (annual_return - risk_free_rate) / annual_vol if annual_vol > 0 else 0
    
    # VaR
    var_95 = calculate_var(portfolio_returns, 0.05)
    var_99 = calculate_var(portfolio_returns, 0.01)
    
    # Maximum Drawdown
    cumulative = (1 + portfolio_returns).cumprod()
    rolling_max = cumulative.expanding().max()
    drawdown = (cumulative - rolling_max) / rolling_max
    max_drawdown = drawdown.min()
    
    return {
        'annual_return': annual_return,
        'annual_volatility': annual_vol,
        'sharpe_ratio': sharpe_ratio,
        'var_95': var_95,
        'var_99': var_99,
        'max_drawdown': max_drawdown,
        'portfolio_returns': portfolio_returns
    }

def calculate_correlation_matrix(price_data):
    """Calculate correlation matrix"""
    returns = calculate_returns(price_data)
    return returns.corr()

# Predefined Portfolios
SAMPLE_PORTFOLIOS = {
    "NIFTY Top 10": {
        "symbols": ["RELIANCE", "TCS", "HDFCBANK", "INFY", "HINDUNILVR", 
                   "ICICIBANK", "KOTAKBANK", "BHARTIARTL", "SBIN", "LT"],
        "weights": [0.1] * 10
    },
    "Banking Focus": {
        "symbols": ["HDFCBANK", "ICICIBANK", "KOTAKBANK", "SBIN", "AXISBANK"],
        "weights": [0.2] * 5
    },
    "IT Sector": {
        "symbols": ["TCS", "INFY", "HCLTECH", "WIPRO", "TECHM"],
        "weights": [0.2] * 5
    }
}

# Main Application
def main():
    st.markdown('<div class="main-header">📈 NSE Portfolio Analytics</div>', 
                unsafe_allow_html=True)
    
    # Initialize database
    conn = init_database()
    
    # Sidebar
    st.sidebar.title("Portfolio Configuration")
    
    # Portfolio selection
    portfolio_option = st.sidebar.selectbox(
        "Choose Portfolio Type",
        ["Sample Portfolio", "Custom Portfolio", "Load Saved Portfolio"]
    )
    
    if portfolio_option == "Sample Portfolio":
        selected_portfolio = st.sidebar.selectbox(
            "Select Sample Portfolio",
            list(SAMPLE_PORTFOLIOS.keys())
        )
        
        portfolio_data = SAMPLE_PORTFOLIOS[selected_portfolio]
        symbols = portfolio_data["symbols"]
        weights = portfolio_data["weights"]
        
        st.sidebar.success(f"Loaded: {selected_portfolio}")
        
    elif portfolio_option == "Custom Portfolio":
        st.sidebar.subheader("Build Custom Portfolio")
        
        # Stock input
        stock_input = st.sidebar.text_area(
            "Enter NSE Stock Symbols (one per line)",
            value="RELIANCE\nTCS\nHDFCBANK\nINFY\nHINDUNILVR",
            height=150
        )
        
        symbols = [s.strip().upper() for s in stock_input.split('\n') if s.strip()]
        
        if symbols:
            st.sidebar.write("**Adjust Weights:**")
            weights = []
            
            for symbol in symbols:
                weight = st.sidebar.slider(
                    f"{symbol}",
                    min_value=0.0,
                    max_value=1.0,
                    value=1.0/len(symbols),
                    step=0.05,
                    key=f"weight_{symbol}"
                )
                weights.append(weight)
            
            # Normalize weights
            total_weight = sum(weights)
            if total_weight > 0:
                weights = [w/total_weight for w in weights]
                
                if abs(sum(weights) - 1.0) > 0.01:
                    st.sidebar.warning(f"Weights sum to {sum(weights):.2f}. Auto-normalized to 1.0")
            
            # Save portfolio option
            if st.sidebar.button("💾 Save Portfolio"):
                portfolio_name = st.sidebar.text_input("Portfolio Name")
                if portfolio_name:
                    try:
                        conn.execute(
                            "INSERT OR REPLACE INTO portfolios (name, symbols, weights, created_date) VALUES (?, ?, ?, ?)",
                            (portfolio_name, ','.join(symbols), ','.join(map(str, weights)), str(datetime.now().date()))
                        )
                        conn.commit()
                        st.sidebar.success("Portfolio saved!")
                    except Exception as e:
                        st.sidebar.error(f"Error saving portfolio: {e}")
        else:
            st.sidebar.error("Please enter at least one symbol")
            return
    
    else:  # Load Saved Portfolio
        try:
            saved_portfolios = pd.read_sql_query("SELECT name FROM portfolios", conn)
            if not saved_portfolios.empty:
                selected_saved = st.sidebar.selectbox(
                    "Select Saved Portfolio",
                    saved_portfolios['name'].tolist()
                )
                
                portfolio_row = pd.read_sql_query(
                    "SELECT * FROM portfolios WHERE name = ?", 
                    conn, 
                    params=[selected_saved]
                ).iloc[0]
                
                symbols = portfolio_row['symbols'].split(',')
                weights = [float(w) for w in portfolio_row['weights'].split(',')]
                
                st.sidebar.success(f"Loaded: {selected_saved}")
                st.sidebar.write(f"Created: {portfolio_row['created_date']}")
            else:
                st.sidebar.info("No saved portfolios found")
                return
        except Exception as e:
            st.sidebar.error(f"Error loading portfolios: {e}")
            return
    
    # Analysis period
    st.sidebar.subheader("Analysis Period")
    period = st.sidebar.selectbox(
        "Select Period",
        ["1y", "2y", "5y", "10y", "max"],
        index=0
    )
    
    # Auto-refresh
    auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)")
    if auto_refresh:
        st.experimental_rerun()
    
    # Main Dashboard
    if symbols and weights:
        st.subheader(f"Portfolio Analysis - {len(symbols)} Stocks")
        
        # Show portfolio composition
        portfolio_df = pd.DataFrame({
            'Stock': symbols,
            'Weight': [f"{w:.1%}" for w in weights]
        })
        
        col1, col2 = st.columns([2, 1])
        with col2:
            st.write("**Portfolio Composition:**")
            st.dataframe(portfolio_df, use_container_width=True)
        
        # Fetch data
        with st.spinner("Fetching NSE data..."):
            price_data = get_nse_data(symbols, period)
            nifty_data = get_nifty50_data(period)
        
        if price_data.empty:
            st.error("Could not fetch price data. Please check stock symbols.")
            return
        
        # Calculate metrics
        with st.spinner("Calculating risk metrics..."):
            metrics = calculate_portfolio_metrics(price_data, weights)
        
        if not metrics:
            st.error("Could not calculate portfolio metrics.")
            return
        
        # Key Metrics Display
        st.subheader("📊 Key Performance Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Annual Return",
                f"{metrics['annual_return']:.2%}",
                delta=None
            )
        
        with col2:
            st.metric(
                "Volatility",
                f"{metrics['annual_volatility']:.2%}",
                delta=None
            )
        
        with col3:
            st.metric(
                "Sharpe Ratio",
                f"{metrics['sharpe_ratio']:.3f}",
                delta=None
            )
        
        with col4:
            st.metric(
                "Max Drawdown",
                f"{metrics['max_drawdown']:.2%}",
                delta=None
            )
        
        # Risk Metrics
        st.subheader("⚠️ Risk Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("VaR (95%)", f"{metrics['var_95']:.2%}")
        with col2:
            st.metric("VaR (99%)", f"{metrics['var_99']:.2%}")
        with col3:
            # Portfolio value for VaR in INR
            portfolio_value = st.number_input("Portfolio Value (₹)", value=1000000, step=50000)
            var_inr = abs(metrics['var_95']) * portfolio_value
            st.metric("Daily VaR (₹)", f"₹{var_inr:,.0f}")
        
        # Charts Section
        st.subheader("📈 Performance Analysis")
        
        # Performance Chart
        fig_perf = go.Figure()
        
        # Portfolio cumulative returns
        portfolio_returns = metrics['portfolio_returns']
        portfolio_cumulative = (1 + portfolio_returns).cumprod()
        
        fig_perf.add_trace(go.Scatter(
            x=portfolio_cumulative.index,
            y=portfolio_cumulative.values,
            mode='lines',
            name='Portfolio',
            line=dict(color='#1f77b4', width=3)
        ))
        
        # NIFTY 50 comparison
        if not nifty_data.empty:
            nifty_aligned = nifty_data.reindex(price_data.index, method='ffill')
            nifty_returns = nifty_aligned.pct_change().dropna()
            nifty_cumulative = (1 + nifty_returns).cumprod()
            
            fig_perf.add_trace(go.Scatter(
                x=nifty_cumulative.index,
                y=nifty_cumulative.values,
                mode='lines',
                name='NIFTY 50',
                line=dict(color='#ff7f0e', width=2)
            ))
        
        fig_perf.update_layout(
            title="Cumulative Returns Comparison",
            xaxis_title="Date",
            yaxis_title="Cumulative Return",
            hovermode='x unified',
            template='plotly_white',
            height=500
        )
        
        st.plotly_chart(fig_perf, use_container_width=True)
        
        # Correlation Heatmap
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Correlation Matrix")
            corr_matrix = calculate_correlation_matrix(price_data)
            
            fig_corr = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                color_continuous_scale="RdBu_r",
                color_continuous_midpoint=0,
                title="Stock Correlations"
            )
            fig_corr.update_layout(height=400)
            st.plotly_chart(fig_corr, use_container_width=True)
        
        with col2:
            st.subheader("📊 Returns Distribution")
            
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(
                x=portfolio_returns,
                nbinsx=50,
                name='Daily Returns',
                opacity=0.7,
                marker_color='#1f77b4'
            ))
            
            fig_hist.update_layout(
                title="Daily Returns Distribution",
                xaxis_title="Daily Return",
                yaxis_title="Frequency",
                template='plotly_white',
                height=400
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        # Individual Stock Performance
        st.subheader("📈 Individual Stock Performance")
        
        # Calculate individual stock metrics
        individual_metrics = []
        returns_data = calculate_returns(price_data)
        
        for i, symbol in enumerate(symbols):
            stock_returns = returns_data[symbol]
            annual_ret = stock_returns.mean() * 252
            annual_vol = stock_returns.std() * np.sqrt(252)
            sharpe = (annual_ret - 0.07) / annual_vol if annual_vol > 0 else 0
            
            individual_metrics.append({
                'Stock': symbol,
                'Weight': f"{weights[i]:.1%}",
                'Annual Return': f"{annual_ret:.2%}",
                'Volatility': f"{annual_vol:.2%}",
                'Sharpe Ratio': f"{sharpe:.3f}",
                'Current Price': f"₹{price_data[symbol].iloc[-1]:.2f}"
            })
        
        metrics_df = pd.DataFrame(individual_metrics)
        st.dataframe(metrics_df, use_container_width=True)
        
        # Export Options
        st.subheader("📤 Export Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Export Portfolio Data"):
                export_data = {
                    'Portfolio Composition': portfolio_df,
                    'Performance Metrics': pd.DataFrame([{
                        'Metric': k.replace('_', ' ').title(),
                        'Value': f"{v:.2%}" if 'return' in k or 'vol' in k or 'drawdown' in k else f"{v:.3f}"
                    } for k, v in metrics.items() if k != 'portfolio_returns']),
                    'Individual Stocks': metrics_df,
                    'Price Data': price_data.tail(10)
                }
                
                # Create Excel file
                with pd.ExcelWriter('portfolio_analysis.xlsx') as writer:
                    for sheet_name, data in export_data.items():
                        data.to_excel(writer, sheet_name=sheet_name, index=False)
                
                st.success("Data exported to portfolio_analysis.xlsx")
        
        with col2:
            if st.button("📈 Export Price Data"):
                price_data.to_csv('price_data.csv')
                st.success("Price data exported to price_data.csv")
        
        with col3:
            if st.button("📊 Export Returns Data"):
                returns_data.to_csv('returns_data.csv')
                st.success("Returns data exported to returns_data.csv")
        
        # Footer
        st.markdown("---")
        st.markdown("""
        **Data Source:** Yahoo Finance | **Risk-Free Rate:** 7% (10-year Government Bond)
        
        **Disclaimer:** This tool is for educational purposes only. Past performance does not guarantee future results. 
        Always consult with qualified financial advisors before making investment decisions.
        """)
    
    conn.close()

if __name__ == "__main__":
    main()
