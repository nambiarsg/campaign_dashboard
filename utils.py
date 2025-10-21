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
    Calculate summary metrics from all uploaded data
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
    
    # Revenue metrics
    if 'revenue.csv' in filtered_data and not filtered_data['revenue.csv'].empty:
        revenue_df = filtered_data['revenue.csv']
        summary['total_revenue'] = revenue_df['value'].sum()
        summary['avg_daily_revenue'] = revenue_df['value'].mean()
        
        # Calculate previous period for trend
        if len(revenue_df) > 1:
            mid_point = len(revenue_df) // 2
            current_period = revenue_df.iloc[mid_point:]['value'].sum()
            previous_period = revenue_df.iloc[:mid_point]['value'].sum()
            trend_pct, trend_dir = calculate_trend(current_period, previous_period)
            summary['revenue_trend'] = {'percentage': trend_pct, 'direction': trend_dir}
        else:
            summary['revenue_trend'] = {'percentage': 0, 'direction': 'neutral'}
    
    # Purchase metrics
    if 'noofpurchasesattributedtopush.csv' in filtered_data and not filtered_data['noofpurchasesattributedtopush.csv'].empty:
        purchases_df = filtered_data['noofpurchasesattributedtopush.csv']
        summary['total_purchases'] = purchases_df['value'].sum()
        summary['avg_daily_purchases'] = purchases_df['value'].mean()
        
        # Calculate trend
        if len(purchases_df) > 1:
            mid_point = len(purchases_df) // 2
            current_period = purchases_df.iloc[mid_point:]['value'].sum()
            previous_period = purchases_df.iloc[:mid_point]['value'].sum()
            trend_pct, trend_dir = calculate_trend(current_period, previous_period)
            summary['purchases_trend'] = {'percentage': trend_pct, 'direction': trend_dir}
        else:
            summary['purchases_trend'] = {'percentage': 0, 'direction': 'neutral'}
    
    # Buyer metrics
    if 'noofcustomerswithpurchasesattributedtopush.csv' in filtered_data and not filtered_data['noofcustomerswithpurchasesattributedtopush.csv'].empty:
        buyers_df = filtered_data['noofcustomerswithpurchasesattributedtopush.csv']
        summary['total_buyers'] = buyers_df['value'].sum()
        summary['avg_daily_buyers'] = buyers_df['value'].mean()
        
        # Calculate trend
        if len(buyers_df) > 1:
            mid_point = len(buyers_df) // 2
            current_period = buyers_df.iloc[mid_point:]['value'].sum()
            previous_period = buyers_df.iloc[:mid_point]['value'].sum()
            trend_pct, trend_dir = calculate_trend(current_period, previous_period)
            summary['buyers_trend'] = {'percentage': trend_pct, 'direction': trend_dir}
        else:
            summary['buyers_trend'] = {'percentage': 0, 'direction': 'neutral'}
    
    # AOV metrics
    if 'aovmobilepush.csv' in filtered_data and not filtered_data['aovmobilepush.csv'].empty:
        aov_df = filtered_data['aovmobilepush.csv']
        summary['avg_aov'] = aov_df['value'].mean()
        
        # Calculate trend
        if len(aov_df) > 1:
            mid_point = len(aov_df) // 2
            current_period = aov_df.iloc[mid_point:]['value'].mean()
            previous_period = aov_df.iloc[:mid_point]['value'].mean()
            trend_pct, trend_dir = calculate_trend(current_period, previous_period)
            summary['aov_trend'] = {'percentage': trend_pct, 'direction': trend_dir}
        else:
            summary['aov_trend'] = {'percentage': 0, 'direction': 'neutral'}
    
    # CTR metrics
    if 'ctrrate.csv' in filtered_data and not filtered_data['ctrrate.csv'].empty:
        ctr_df = filtered_data['ctrrate.csv']
        summary['avg_ctr'] = ctr_df['value'].mean()
        
        # Calculate trend
        if len(ctr_df) > 1:
            mid_point = len(ctr_df) // 2
            current_period = ctr_df.iloc[mid_point:]['value'].mean()
            previous_period = ctr_df.iloc[:mid_point]['value'].mean()
            trend_pct, trend_dir = calculate_trend(current_period, previous_period)
            summary['ctr_trend'] = {'percentage': trend_pct, 'direction': trend_dir}
        else:
            summary['ctr_trend'] = {'percentage': 0, 'direction': 'neutral'}
    
    # Delivery rate metrics
    if 'deliveryrate.csv' in filtered_data and not filtered_data['deliveryrate.csv'].empty:
        delivery_df = filtered_data['deliveryrate.csv']
        summary['avg_delivery_rate'] = delivery_df['value'].mean()
        
        # Calculate trend
        if len(delivery_df) > 1:
            mid_point = len(delivery_df) // 2
            current_period = delivery_df.iloc[mid_point:]['value'].mean()
            previous_period = delivery_df.iloc[:mid_point]['value'].mean()
            trend_pct, trend_dir = calculate_trend(current_period, previous_period)
            summary['delivery_rate_trend'] = {'percentage': trend_pct, 'direction': trend_dir}
        else:
            summary['delivery_rate_trend'] = {'percentage': 0, 'direction': 'neutral'}
    
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

def validate_uploaded_files(uploaded_files: List) -> Tuple[bool, List[str]]:
    """
    Validate uploaded files for required columns
    Returns: (is_valid, error_messages)
    """
    errors = []
    required_files = [
        'aovmobilepush.csv',
        'ctrrate.csv', 
        'deliveryrate.csv',
        'noofcustomerswithpurchasesattributedtopush.csv',
        'noofpurchasesattributedtopush.csv',
        'promotionalcampaignlevelperformancepush.csv',
        'revenue.csv'
    ]
    
    uploaded_filenames = [f.name for f in uploaded_files]
    
    # Check if all required files are uploaded
    missing_files = [f for f in required_files if f not in uploaded_filenames]
    if missing_files:
        errors.append(f"Missing required files: {', '.join(missing_files)}")
    
    # Validate each uploaded file
    for uploaded_file in uploaded_files:
        try:
            df = pd.read_csv(uploaded_file)
            filename = uploaded_file.name
            
            if filename in required_files:
                from config import FILE_COLUMNS
                # Get the actual column names that should be in the CSV files
                expected_columns = list(FILE_COLUMNS[filename].values())
                actual_columns = list(df.columns)
                missing_columns = [col for col in expected_columns if col not in actual_columns]
                
                if missing_columns:
                    errors.append(f"{filename}: Missing columns {missing_columns}. Found columns: {actual_columns}")
        
        except Exception as e:
            errors.append(f"Error reading {uploaded_file.name}: {str(e)}")
    
    return len(errors) == 0, errors
