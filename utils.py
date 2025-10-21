"""
Utility functions for data processing and analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from typing import Dict, List, Tuple, Optional
import streamlit as st

def parse_percentage(value: str) -> float:
    """
    Parse percentage string to float value
    Examples: "95.5%" -> 95.5, "0.5%" -> 0.5
    """
    if pd.isna(value) or value == '':
        return 0.0
    
    # Convert to string if not already
    value_str = str(value).strip()
    
    # Remove percentage sign and convert to float
    if '%' in value_str:
        value_str = value_str.replace('%', '')
    
    try:
        return float(value_str)
    except (ValueError, TypeError):
        return 0.0

def parse_timestamp(timestamp_str: str) -> datetime:
    """
    Parse various timestamp formats to datetime object
    """
    if pd.isna(timestamp_str):
        return None
    
    timestamp_str = str(timestamp_str).strip()
    
    # Common timestamp formats
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%m/%d/%Y %H:%M:%S',
        '%d/%m/%Y',
        '%d/%m/%Y %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%SZ'
    ]
    
    for fmt in formats:
        try:
            return pd.to_datetime(timestamp_str, format=fmt)
        except (ValueError, TypeError):
            continue
    
    # Fallback to pandas auto-parsing
    try:
        return pd.to_datetime(timestamp_str)
    except:
        return None

def process_csv_file(df: pd.DataFrame, filename: str) -> pd.DataFrame:
    """
    Process uploaded CSV file based on its type
    """
    if df.empty:
        return df
    
    # Get column mapping for this file type
    from config import FILE_COLUMNS
    
    if filename not in FILE_COLUMNS:
        return df
    
    column_mapping = FILE_COLUMNS[filename]
    processed_df = df.copy()
    
    # Handle timestamp files (most files)
    if 'timestamp' in column_mapping and 'value' in column_mapping:
        timestamp_col = column_mapping['timestamp']
        value_col = column_mapping['value']
        
        # Rename columns for consistency
        if timestamp_col in processed_df.columns:
            processed_df = processed_df.rename(columns={timestamp_col: 'timestamp'})
        
        if value_col in processed_df.columns:
            processed_df = processed_df.rename(columns={value_col: 'value'})
        
        # Parse timestamps
        if 'timestamp' in processed_df.columns:
            processed_df['timestamp'] = processed_df['timestamp'].apply(parse_timestamp)
            processed_df = processed_df.dropna(subset=['timestamp'])
        
        # Parse percentage values
        if 'value' in processed_df.columns:
            processed_df['value'] = processed_df['value'].apply(parse_percentage)
    
    # Handle campaign performance file
    elif filename == 'promotionalcampaignlevelperformancepush.csv':
        # Parse percentage columns
        percentage_cols = ['#3 Delivery Rate', '#4 Click Through Rate']
        for col in percentage_cols:
            if col in processed_df.columns:
                processed_df[col] = processed_df[col].apply(parse_percentage)
        
        # Parse numeric columns
        numeric_cols = ['#0 All Sent', '#1 All Delivered', '#2 All Clicked']
        for col in numeric_cols:
            if col in processed_df.columns:
                processed_df[col] = pd.to_numeric(processed_df[col], errors='coerce').fillna(0)
    
    return processed_df

def calculate_trend(current_value: float, previous_value: float) -> Tuple[float, str]:
    """
    Calculate trend percentage and direction
    Returns: (percentage_change, direction)
    """
    if previous_value == 0:
        if current_value > 0:
            return 100.0, 'up'
        else:
            return 0.0, 'neutral'
    
    percentage_change = ((current_value - previous_value) / previous_value) * 100
    
    if percentage_change > 0:
        direction = 'up'
    elif percentage_change < 0:
        direction = 'down'
    else:
        direction = 'neutral'
    
    return abs(percentage_change), direction

def get_date_range_data(df: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Filter dataframe by date range
    """
    if df.empty or 'timestamp' not in df.columns:
        return df
    
    mask = (df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)
    return df[mask].copy()

def calculate_metrics_summary(data: Dict[str, pd.DataFrame], date_range: Tuple[datetime, datetime] = None) -> Dict:
    """
    Calculate summary metrics from uploaded data based on specific file requirements
    """
    summary = {}
    
    # Filter data by date range if provided
    filtered_data = {}
    if date_range:
        start_date, end_date = date_range
        for key, df in data.items():
            filtered_data[key] = get_date_range_data(df, start_date, end_date)
    else:
        filtered_data = data
    
    # 1. Revenue metrics from push revenue.csv
    if 'push revenue.csv' in filtered_data and not filtered_data['push revenue.csv'].empty:
        revenue_df = filtered_data['push revenue.csv']
        # Find revenue column
        revenue_col = None
        for col in revenue_df.columns:
            if 'revenue' in col.lower() and col.lower() != 'timestamp':
                revenue_col = col
                break
        
        if revenue_col:
            summary['total_revenue'] = revenue_df[revenue_col].sum()
            if len(revenue_df) > 1:
                mid_point = len(revenue_df) // 2
                current_period = revenue_df.iloc[mid_point:][revenue_col].sum()
                previous_period = revenue_df.iloc[:mid_point][revenue_col].sum()
                trend_pct, trend_dir = calculate_trend(current_period, previous_period)
                summary['revenue_trend'] = {'percentage': trend_pct, 'direction': trend_dir}
            else:
                summary['revenue_trend'] = {'percentage': 0, 'direction': 'neutral'}
    
    # 2. CTR metrics from pushctr.csv
    if 'pushctr.csv' in filtered_data and not filtered_data['pushctr.csv'].empty:
        ctr_df = filtered_data['pushctr.csv']
        # Find CTR column
        ctr_col = None
        for col in ctr_df.columns:
            if 'ctr' in col.lower() and col.lower() != 'timestamp':
                ctr_col = col
                break
        
        if ctr_col:
            summary['avg_ctr'] = ctr_df[ctr_col].mean()
            if len(ctr_df) > 1:
                mid_point = len(ctr_df) // 2
                current_period = ctr_df.iloc[mid_point:][ctr_col].mean()
                previous_period = ctr_df.iloc[:mid_point][ctr_col].mean()
                trend_pct, trend_dir = calculate_trend(current_period, previous_period)
                summary['ctr_trend'] = {'percentage': trend_pct, 'direction': trend_dir}
            else:
                summary['ctr_trend'] = {'percentage': 0, 'direction': 'neutral'}
    
    # 3. Delivery rate metrics from pushdeliveryrate.csv
    if 'pushdeliveryrate.csv' in filtered_data and not filtered_data['pushdeliveryrate.csv'].empty:
        delivery_df = filtered_data['pushdeliveryrate.csv']
        # Find delivery rate column
        delivery_col = None
        for col in delivery_df.columns:
            if 'delivery' in col.lower() and col.lower() != 'timestamp':
                delivery_col = col
                break
        
        if delivery_col:
            summary['avg_delivery_rate'] = delivery_df[delivery_col].mean()
            if len(delivery_df) > 1:
                mid_point = len(delivery_df) // 2
                current_period = delivery_df.iloc[mid_point:][delivery_col].mean()
                previous_period = delivery_df.iloc[:mid_point][delivery_col].mean()
                trend_pct, trend_dir = calculate_trend(current_period, previous_period)
                summary['delivery_rate_trend'] = {'percentage': trend_pct, 'direction': trend_dir}
            else:
                summary['delivery_rate_trend'] = {'percentage': 0, 'direction': 'neutral'}
    
    # 4. AOV metrics from pushaov.csv
    if 'pushaov.csv' in filtered_data and not filtered_data['pushaov.csv'].empty:
        aov_df = filtered_data['pushaov.csv']
        # Find AOV column
        aov_col = None
        for col in aov_df.columns:
            if 'aov' in col.lower() and col.lower() != 'timestamp':
                aov_col = col
                break
        
        if aov_col:
            summary['avg_aov'] = aov_df[aov_col].mean()
            if len(aov_df) > 1:
                mid_point = len(aov_df) // 2
                current_period = aov_df.iloc[mid_point:][aov_col].mean()
                previous_period = aov_df.iloc[:mid_point][aov_col].mean()
                trend_pct, trend_dir = calculate_trend(current_period, previous_period)
                summary['aov_trend'] = {'percentage': trend_pct, 'direction': trend_dir}
            else:
                summary['aov_trend'] = {'percentage': 0, 'direction': 'neutral'}
    
    # 5. Purchase metrics from noofpurchasesattributedtopush.csv
    if 'noofpurchasesattributedtopush.csv' in filtered_data and not filtered_data['noofpurchasesattributedtopush.csv'].empty:
        purchases_df = filtered_data['noofpurchasesattributedtopush.csv']
        # Find purchases column
        purchases_col = None
        for col in purchases_df.columns:
            if 'purchase' in col.lower() and col.lower() != 'timestamp':
                purchases_col = col
                break
        
        if purchases_col:
            summary['total_purchases'] = purchases_df[purchases_col].sum()
            if len(purchases_df) > 1:
                mid_point = len(purchases_df) // 2
                current_period = purchases_df.iloc[mid_point:][purchases_col].sum()
                previous_period = purchases_df.iloc[:mid_point][purchases_col].sum()
                trend_pct, trend_dir = calculate_trend(current_period, previous_period)
                summary['purchases_trend'] = {'percentage': trend_pct, 'direction': trend_dir}
            else:
                summary['purchases_trend'] = {'percentage': 0, 'direction': 'neutral'}
    
    return summary

def format_currency(value: float) -> str:
    """Format value as currency"""
    if pd.isna(value):
        return "$0"
    return f"${value:,.2f}"

def format_number(value: float) -> str:
    """Format value as number with commas"""
    if pd.isna(value):
        return "0"
    return f"{value:,.0f}"

def format_percentage(value: float) -> str:
    """Format value as percentage"""
    if pd.isna(value):
        return "0%"
    return f"{value:.1f}%"

def get_trend_arrow(direction: str) -> str:
    """Get trend arrow emoji"""
    if direction == 'up':
        return "📈"
    elif direction == 'down':
        return "📉"
    else:
        return "➡️"

# Validation function removed - dashboard now accepts any CSV files
