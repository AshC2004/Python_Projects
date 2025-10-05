"""
Configuration and utilities for NSE Portfolio Analytics
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

NIFTY_50_STOCKS = [
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "HINDUNILVR", "ICICIBANK", 
    "KOTAKBANK", "BHARTIARTL", "SBIN", "LT", "ASIANPAINT", "AXISBANK",
    "MARUTI", "NESTLEIND", "HCLTECH", "BAJFINANCE", "M&M", "SUNPHARMA",
    "TITAN", "ULTRACEMCO", "WIPRO", "NTPC", "JSWSTEEL", "POWERGRID",
    "TATAMOTORS", "TECHM", "INDUSINDBK", "HEROMOTOCO", "CIPLA", "ONGC",
    "COALINDIA", "IOC", "GRASIM", "BPCL", "ADANIENT", "DRREDDY", "EICHERMOT",
    "APOLLOHOSP", "BAJAJFINSV", "DIVISLAB", "TATACONSUM", "BRITANNIA",
    "HINDALCO", "UPL", "SBILIFE", "HDFCLIFE", "BAJAJ-AUTO", "TATASTEEL", "TRENT"
]

SECTOR_MAPPING = {
    "TCS": "Information Technology",
    "INFY": "Information Technology", 
    "HCLTECH": "Information Technology",
    "WIPRO": "Information Technology",
    "TECHM": "Information Technology",
    
    "HDFCBANK": "Banking",
    "ICICIBANK": "Banking",
    "KOTAKBANK": "Banking",
    "SBIN": "Banking",
    "AXISBANK": "Banking",
    "INDUSINDBK": "Banking",
    
    "BAJFINANCE": "Financial Services",
    "BAJAJFINSV": "Financial Services",
    "SBILIFE": "Financial Services",
    "HDFCLIFE": "Financial Services",
    
    "RELIANCE": "Oil & Gas",
    "ONGC": "Oil & Gas",
    "IOC": "Oil & Gas",
    "BPCL": "Oil & Gas",
    
    "HINDUNILVR": "Consumer Goods",
    "NESTLEIND": "Consumer Goods",
    "BRITANNIA": "Consumer Goods",
    "TATACONSUM": "Consumer Goods",
    
    "MARUTI": "Automobiles",
    "M&M": "Automobiles",
    "TATAMOTORS": "Automobiles",
    "BAJAJ-AUTO": "Automobiles",
    "HEROMOTOCO": "Automobiles",
    "EICHERMOT": "Automobiles",
    
    "SUNPHARMA": "Pharmaceuticals",
    "DRREDDY": "Pharmaceuticals",
    "CIPLA": "Pharmaceuticals",
    "DIVISLAB": "Pharmaceuticals",
    "APOLLOHOSP": "Pharmaceuticals",
    
    "ULTRACEMCO": "Cement",
    "LT": "Construction",
    "GRASIM": "Cement",
    
    "TATASTEEL": "Metals",
    "HINDALCO": "Metals",
    "JSWSTEEL": "Metals",
    "COALINDIA": "Mining",
    
    "BHARTIARTL": "Telecom",
    
    "NTPC": "Power",
    "POWERGRID": "Power",
    
    "UPL": "Chemicals",
    "ADANIENT": "Chemicals",
    
    "ASIANPAINT": "Paints",
    
    "TITAN": "Consumer Discretionary",
    
    "TRENT": "Retail"
}

RISK_CONFIG = {
    'RISK_FREE_RATE': 0.07,
    'VAR_CONFIDENCE_LEVELS': [0.95, 0.99],
    'VOLATILITY_LOOKBACK': 252,
    'CORRELATION_THRESHOLD': 0.8,
    'MAX_POSITION_SIZE': 0.25,
    'MIN_PORTFOLIO_SIZE': 3,
    'MAX_PORTFOLIO_SIZE': 50
}

PORTFOLIO_TEMPLATES = {
    "Conservative Balanced": {
        "description": "Low risk, diversified portfolio with focus on large-cap stocks",
        "symbols": ["HDFCBANK", "TCS", "RELIANCE", "HINDUNILVR", "NESTLEIND", "ASIANPAINT"],
        "weights": [0.20, 0.20, 0.15, 0.15, 0.15, 0.15],
        "risk_profile": "Conservative"
    },
    
    "Growth Focused": {
        "description": "Higher growth potential with IT and financial services focus",
        "symbols": ["TCS", "INFY", "HCLTECH", "BAJFINANCE", "KOTAKBANK", "TECHM"],
        "weights": [0.20, 0.20, 0.15, 0.15, 0.15, 0.15],
        "risk_profile": "Moderate"
    },
    
    "Dividend Yield": {
        "description": "Focus on high dividend yielding stocks",
        "symbols": ["SBIN", "COALINDIA", "NTPC", "IOC", "POWERGRID", "ONGC"],
        "weights": [0.20, 0.15, 0.15, 0.15, 0.15, 0.20],
        "risk_profile": "Conservative"
    },
    
    "Aggressive Growth": {
        "description": "High growth potential with higher volatility",
        "symbols": ["BAJFINANCE", "ADANIENT", "TATAMOTORS", "JSWSTEEL", "M&M", "TRENT"],
        "weights": [0.20, 0.15, 0.15, 0.15, 0.15, 0.20],
        "risk_profile": "Aggressive"
    }
}

def get_portfolio_template(template_name):
    """Get a predefined portfolio template"""
    return PORTFOLIO_TEMPLATES.get(template_name, None)

def validate_portfolio(symbols, weights):
    """Validate portfolio composition"""
    errors = []
    warnings = []
    
    if len(symbols) != len(weights):
        errors.append("Number of symbols and weights must match")
        return errors, warnings
    
    weight_sum = sum(weights)
    if abs(weight_sum - 1.0) > 0.01:
        warnings.append(f"Weights sum to {weight_sum:.3f}, should be 1.0")
    
    max_weight = max(weights)
    if max_weight > RISK_CONFIG['MAX_POSITION_SIZE']:
        warnings.append(f"Maximum position size ({max_weight:.1%}) exceeds recommended limit ({RISK_CONFIG['MAX_POSITION_SIZE']:.1%})")
    
    num_stocks = len(symbols)
    if num_stocks < RISK_CONFIG['MIN_PORTFOLIO_SIZE']:
        warnings.append(f"Portfolio has {num_stocks} stocks, minimum recommended is {RISK_CONFIG['MIN_PORTFOLIO_SIZE']}")
    
    if num_stocks > RISK_CONFIG['MAX_PORTFOLIO_SIZE']:
        warnings.append(f"Portfolio has {num_stocks} stocks, maximum recommended is {RISK_CONFIG['MAX_PORTFOLIO_SIZE']}")
    
    if len(set(symbols)) != len(symbols):
        errors.append("Duplicate symbols found in portfolio")
    
    return errors, warnings

def calculate_sector_allocation(symbols, weights):
    """Calculate sector-wise allocation"""
    sector_allocation = {}
    
    for symbol, weight in zip(symbols, weights):
        sector = SECTOR_MAPPING.get(symbol, "Other")
        sector_allocation[sector] = sector_allocation.get(sector, 0) + weight
    
    return sector_allocation

def get_risk_profile_description(sharpe_ratio, max_drawdown, volatility):
    """Determine risk profile based on metrics"""
    
    if sharpe_ratio > 1.5 and max_drawdown > -0.05 and volatility < 0.15:
        return "Low Risk", "Excellent risk-adjusted returns with low volatility"
    elif sharpe_ratio > 1.0 and max_drawdown > -0.10 and volatility < 0.20:
        return "Moderate Risk", "Good risk-adjusted returns with manageable volatility"
    elif sharpe_ratio > 0.5 and max_drawdown > -0.20 and volatility < 0.30:
        return "High Risk", "Acceptable returns but higher volatility and drawdowns"
    else:
        return "Very High Risk", "Poor risk-adjusted returns with high volatility"

def format_currency(value, currency="INR"):
    """Format currency values for display"""
    if currency == "INR":
        if abs(value) >= 10000000:
            return f"₹{value/10000000:.1f}Cr"
        elif abs(value) >= 100000:
            return f"₹{value/100000:.1f}L"
        else:
            return f"₹{value:,.0f}"
    else:
        return f"${value:,.2f}"

def generate_risk_report(metrics, portfolio_value=1000000):
    """Generate a comprehensive risk report"""
    
    report = {
        'portfolio_value': portfolio_value,
        'annual_return': metrics.get('annual_return', 0),
        'annual_volatility': metrics.get('annual_volatility', 0),
        'sharpe_ratio': metrics.get('sharpe_ratio', 0),
        'max_drawdown': metrics.get('max_drawdown', 0),
        'var_95_percent': abs(metrics.get('var_95', 0)) * portfolio_value,
        'var_99_percent': abs(metrics.get('var_99', 0)) * portfolio_value,
    }
    
    risk_level, risk_description = get_risk_profile_description(
        report['sharpe_ratio'],
        report['max_drawdown'],
        report['annual_volatility']
    )
    
    report['risk_level'] = risk_level
    report['risk_description'] = risk_description
    
    return report

def get_market_indicators():
    """Get general market indicators (simplified)"""
    
    return {
        'nifty_pe': 22.5,
        'nifty_pb': 3.2,
        'vix_level': 15.8,
        'bond_yield_10yr': 7.2,
        'market_sentiment': 'Neutral',
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
