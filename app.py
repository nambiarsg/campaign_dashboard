"""
Bloomreach Mobile Push Performance Analytics Dashboard
A professional Streamlit dashboard for analyzing mobile push campaign performance
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io
from typing import Dict, List, Tuple

# Import custom modules
from config import COLORS, CHART_COLORS, THRESHOLDS, CUSTOM_CSS, CHART_CONFIG, DATE_RANGES
from utils import (
    process_csv_file, calculate_push_metrics_summary,
    format_currency, format_number, format_percentage, get_trend_arrow,
    get_date_range_data, parse_percentage, parse_timestamp
)

# Page configuration
st.set_page_config(
    page_title="Bloomreach Mobile Push Analytics",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache busting - force CSS reload
import time
cache_buster = int(time.time())

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize session state
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = {}
if 'last_updated' not in st.session_state:
    st.session_state.last_updated = None

def render_header():
    """Render the main header"""
    st.markdown("""
    <div class="dashboard-header">
        <h1>📱 Bloomreach Mobile Push Analytics</h1>
        <p>Professional Performance Dashboard for Mobile Push Campaigns</p>
        <p style="font-size: 0.9rem; opacity: 0.8; margin-top: 1rem;">Version 2.0 - Modern UI</p>
    </div>
    """, unsafe_allow_html=True)
    
    if hasattr(st.session_state, 'last_updated') and st.session_state.last_updated:
        st.caption(f"Last updated: {st.session_state.last_updated}")

def render_sidebar():
    """Render the sidebar with file upload and controls"""
    st.sidebar.title("📊 Dashboard Controls")
    
    # File upload section
    st.sidebar.markdown("### 📁 Upload Data Files")
    st.sidebar.markdown("""
    <div class="upload-section">
        <p><strong>Required files (any extension):</strong></p>
        <ul>
            <li><strong>pushsends</strong><br/>Columns: timestamp, sends</li>
            <li><strong>pushdeliveryrate</strong><br/>Columns: timestamp, delivery rate</li>
            <li><strong>openrate</strong><br/>Columns: timestamp, open rate</li>
            <li><strong>pushctr</strong><br/>Columns: timestamp, ctr</li>
            <li><strong>noofpurchasesattributedtopush</strong><br/>Columns: timestamp, Purchases</li>
            <li><strong>push revenue</strong><br/>Columns: timestamp, revenue</li>
            <li><strong>optout</strong><br/>Columns: timestamp, optout rate</li>
            <li><strong>campaigns</strong><br/>Campaign performance data</li>
        </ul>
        <p><em>Works with .csv, .numbers, .xlsx, etc.</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.sidebar.file_uploader(
        "Choose data files",
        type=['csv', 'xlsx', 'xls', 'numbers'],
        accept_multiple_files=True,
        help="Upload all required data files for analysis"
    )
    
    # Process uploaded files - NO VALIDATION, just process whatever is uploaded
    if uploaded_files:
        processed_data = {}
        for uploaded_file in uploaded_files:
            try:
                df = pd.read_csv(uploaded_file)
                processed_df = df.copy()
                
                # Try to parse percentage columns
                for col in processed_df.columns:
                    if processed_df[col].dtype == 'object':
                        try:
                            # Check if column contains percentage values
                            sample_values = processed_df[col].dropna().head(5)
                            if any('%' in str(val) for val in sample_values):
                                processed_df[col] = processed_df[col].apply(lambda x: parse_percentage(str(x)) if pd.notna(x) else 0)
                        except:
                            pass  # Skip if parsing fails
                
                # Try to parse timestamp columns
                for col in processed_df.columns:
                    if 'timestamp' in col.lower() or 'date' in col.lower():
                        try:
                            processed_df[col] = processed_df[col].apply(parse_timestamp)
                        except:
                            pass  # Skip if parsing fails
                
                processed_data[uploaded_file.name] = processed_df
                st.sidebar.success(f"✅ {uploaded_file.name} uploaded successfully")
                
            except Exception as e:
                st.sidebar.warning(f"⚠️ Could not process {uploaded_file.name}: {str(e)}")
                # Still add the file even if processing fails
                try:
                    processed_data[uploaded_file.name] = pd.read_csv(uploaded_file)
                except:
                    pass
        
        if processed_data:
            st.session_state.uploaded_data = processed_data
            st.session_state.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.sidebar.success("🎉 Files uploaded successfully!")
            
            # Add button to view dashboard
            if st.sidebar.button("📊 View Dashboard", type="primary"):
                st.rerun()
    
    # Date range filter
    st.sidebar.markdown("### 📅 Date Range Filter")
    
    if hasattr(st.session_state, 'uploaded_data') and st.session_state.uploaded_data:
        # Get date range from data
        all_dates = []
        for df in st.session_state.uploaded_data.values():
            if 'timestamp' in df.columns and not df.empty:
                all_dates.extend(df['timestamp'].dropna().tolist())
        
        if all_dates:
            min_date = min(all_dates)
            max_date = max(all_dates)
            
            # Quick select buttons
            col1, col2 = st.sidebar.columns(2)
            with col1:
                if st.button("7 Days"):
                    st.session_state.date_range = (max_date - timedelta(days=7), max_date)
            with col2:
                if st.button("30 Days"):
                    st.session_state.date_range = (max_date - timedelta(days=30), max_date)
            
            col3, col4 = st.sidebar.columns(2)
            with col3:
                if st.button("90 Days"):
                    st.session_state.date_range = (max_date - timedelta(days=90), max_date)
            with col4:
                if st.button("All Time"):
                    st.session_state.date_range = (min_date, max_date)
            
            # Date picker
            date_range = st.sidebar.date_input(
                "Select Date Range",
                value=(min_date.date(), max_date.date()),
                min_value=min_date.date(),
                max_value=max_date.date()
            )
            
            if len(date_range) == 2:
                start_date = datetime.combine(date_range[0], datetime.min.time())
                end_date = datetime.combine(date_range[1], datetime.max.time())
                st.session_state.date_range = (start_date, end_date)
    
    # Clear data button
    if hasattr(st.session_state, 'uploaded_data') and st.session_state.uploaded_data:
        st.sidebar.markdown("### 🗑️ Data Management")
        if st.sidebar.button("Clear All Data", type="secondary"):
            st.session_state.uploaded_data = {}
            st.session_state.last_updated = None
            if hasattr(st.session_state, 'date_range'):
                st.session_state.date_range = None
            st.rerun()

def render_metric_card(title: str, value: str, trend: Dict = None, icon: str = "📊"):
    """Render a modern metric card with trend indicator"""
    if trend:
        trend_arrow = get_trend_arrow(trend['direction'])
        trend_class = f"trend-{trend['direction']}"
        trend_text = f"{trend_arrow} {trend['percentage']:.1f}%"
    else:
        trend_class = "trend-neutral"
        trend_text = "➡️ No data"
    
    st.markdown(f"""
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div style="flex: 1;">
                <p class="metric-label">{title}</p>
                <p class="metric-value">{value}</p>
                <div class="metric-trend">
                    <span class="{trend_class}">{trend_text}</span>
                </div>
            </div>
            <div style="font-size: 2.5rem; opacity: 0.7; margin-left: 1rem;">
                {icon}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_metrics_cards():
    """Render the 8 key push notification metrics"""
    if not hasattr(st.session_state, 'uploaded_data') or not st.session_state.uploaded_data:
        return
    
    # Calculate metrics
    date_range = st.session_state.get('date_range', None)
    summary = calculate_push_metrics_summary(st.session_state.uploaded_data, date_range)
    
    # Create 4 columns for 8 metrics (2 rows of 4)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # 1. Total Push Sends
        sends = summary.get('total_sends', 0)
        sends_trend = summary.get('sends_trend', {})
        render_metric_card(
            "Total Push Sends",
            format_number(sends),
            sends_trend,
            "📤"
        )
        
        # 5. Conversion Rate
        conversion_rate = summary.get('conversion_rate', 0)
        conversion_trend = summary.get('conversion_trend', {})
        render_metric_card(
            "Conversion Rate (%)",
            format_percentage(conversion_rate),
            conversion_trend,
            "🎯"
        )
    
    with col2:
        # 2. Delivery Rate
        delivery_rate = summary.get('delivery_rate', 0)
        delivery_trend = summary.get('delivery_trend', {})
        render_metric_card(
            "Delivery Rate (%)",
            format_percentage(delivery_rate),
            delivery_trend,
            "📨"
        )
        
        # 6. Revenue from Push
        revenue = summary.get('revenue_from_push', 0)
        revenue_trend = summary.get('revenue_trend', {})
        render_metric_card(
            "Revenue from Push (AED)",
            format_currency(revenue),
            revenue_trend,
            "💰"
        )
    
    with col3:
        # 3. Open Rate
        open_rate = summary.get('open_rate', 0)
        open_trend = summary.get('open_trend', {})
        render_metric_card(
            "Open Rate (%)",
            format_percentage(open_rate),
            open_trend,
            "👁️"
        )
        
        # 7. Opt-out Rate
        optout_rate = summary.get('optout_rate', 0)
        optout_trend = summary.get('optout_trend', {})
        render_metric_card(
            "Opt-out Rate (%)",
            format_percentage(optout_rate),
            optout_trend,
            "🚫"
        )
    
    with col4:
        # 4. Click-Through Rate
        ctr = summary.get('ctr', 0)
        ctr_trend = summary.get('ctr_trend', {})
        render_metric_card(
            "Click-Through Rate (%)",
            format_percentage(ctr),
            ctr_trend,
            "👆"
        )
        
        # 8. Top Performing Campaigns
        top_campaigns = summary.get('top_campaigns_count', 0)
        campaigns_trend = summary.get('campaigns_trend', {})
        render_metric_card(
            "Top Performing Campaigns",
            f"{top_campaigns} Active",
            campaigns_trend,
            "🏆"
        )

def render_revenue_trend_chart():
    """Render revenue trend chart for last 60 days"""
    if not hasattr(st.session_state, 'uploaded_data'):
        return
    
    # Find revenue file
    revenue_file = None
    for filename in st.session_state.uploaded_data.keys():
        if 'push revenue' in filename.lower():
            revenue_file = filename
            break
    
    if not revenue_file:
        return
    
    revenue_df = st.session_state.uploaded_data[revenue_file]
    
    # Find revenue and timestamp columns
    revenue_col = None
    timestamp_col = None
    
    for col in revenue_df.columns:
        if 'revenue' in col.lower() and col.lower() != 'timestamp':
            revenue_col = col
        elif 'timestamp' in col.lower():
            timestamp_col = col
    
    if revenue_col is None or timestamp_col is None:
        return
    
    # Get last 60 days of data
    if not revenue_df.empty and timestamp_col in revenue_df.columns:
        # Remove any rows with null timestamps first
        revenue_df_clean = revenue_df.dropna(subset=[timestamp_col])
        
        # Sort by timestamp and get last 60 days
        revenue_df_sorted = revenue_df_clean.sort_values(timestamp_col)
        if len(revenue_df_sorted) > 60:
            revenue_df_sorted = revenue_df_sorted.tail(60)
    
    if revenue_df_sorted.empty:
        return
    
    fig = px.line(
        revenue_df_sorted,
        x=timestamp_col,
        y=revenue_col,
        title='Revenue Trend - Last 60 Days',
        color_discrete_sequence=[CHART_COLORS['revenue']]
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Revenue (AED)",
        hovermode='x unified',
        showlegend=False,
        height=400,
        xaxis=dict(
            type='date',
            tickformat='%b %d, %Y',
            tickmode='auto',
            nticks=8
        )
    )
    
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=6)
    )
    
    st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)

def render_purchases_trend_chart():
    """Render purchases trend chart for last 60 days"""
    if not hasattr(st.session_state, 'uploaded_data'):
        return
    
    # Find purchases file
    purchases_file = None
    for filename in st.session_state.uploaded_data.keys():
        if 'noofpurchasesattributedtopush' in filename.lower():
            purchases_file = filename
            break
    
    if not purchases_file:
        return
    
    purchases_df = st.session_state.uploaded_data[purchases_file]
    
    # Find purchases and timestamp columns
    purchases_col = None
    timestamp_col = None
    
    for col in purchases_df.columns:
        if 'purchase' in col.lower() and col.lower() != 'timestamp':
            purchases_col = col
        elif 'timestamp' in col.lower():
            timestamp_col = col
    
    if purchases_col is None or timestamp_col is None:
        return
    
    # Get last 60 days of data
    if not purchases_df.empty and timestamp_col in purchases_df.columns:
        # Remove any rows with null timestamps first
        purchases_df_clean = purchases_df.dropna(subset=[timestamp_col])
        
        # Sort by timestamp and get last 60 days
        purchases_df_sorted = purchases_df_clean.sort_values(timestamp_col)
        if len(purchases_df_sorted) > 60:
            purchases_df_sorted = purchases_df_sorted.tail(60)
    
    if purchases_df_sorted.empty:
        return
    
    fig = px.line(
        purchases_df_sorted,
        x=timestamp_col,
        y=purchases_col,
        title='Conversion Trend - Last 60 Days',
        color_discrete_sequence=[CHART_COLORS['purchases']]
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Purchases",
        hovermode='x unified',
        showlegend=False,
        height=400,
        xaxis=dict(
            type='date',
            tickformat='%b %d, %Y',
            tickmode='auto',
            nticks=8
        )
    )
    
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=6)
    )
    
    st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)

def render_purchases_buyers_chart():
    """Render purchases and buyers dual-axis chart"""
    if not hasattr(st.session_state, 'uploaded_data'):
        return
    purchases_df = st.session_state.uploaded_data.get('noofpurchasesattributedtopush.csv', pd.DataFrame())
    buyers_df = st.session_state.uploaded_data.get('noofcustomerswithpurchasesattributedtopush.csv', pd.DataFrame())
    
    if purchases_df.empty and buyers_df.empty:
        return
    
    # Apply date filter if set
    if st.session_state.get('date_range'):
        start_date, end_date = st.session_state.date_range
        if not purchases_df.empty:
            purchases_df = get_date_range_data(purchases_df, start_date, end_date)
        if not buyers_df.empty:
            buyers_df = get_date_range_data(buyers_df, start_date, end_date)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add purchases line
    if not purchases_df.empty:
        fig.add_trace(
            go.Scatter(
                x=purchases_df['timestamp'],
                y=purchases_df['value'],
                name='Purchases',
                line=dict(color=CHART_COLORS['purchases'], width=3),
                marker=dict(size=6)
            ),
            secondary_y=False,
        )
    
    # Add buyers line
    if not buyers_df.empty:
        fig.add_trace(
            go.Scatter(
                x=buyers_df['timestamp'],
                y=buyers_df['value'],
                name='Buyers',
                line=dict(color=CHART_COLORS['buyers'], width=3),
                marker=dict(size=6)
            ),
            secondary_y=True,
        )
    
    # Update layout
    fig.update_layout(
        title_text="Purchases & Buyers Over Time",
        height=400,
        hovermode='x unified'
    )
    
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Purchases", secondary_y=False)
    fig.update_yaxes(title_text="Buyers", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)

def render_ctr_delivery_chart():
    """Render CTR and delivery rate chart"""
    if not hasattr(st.session_state, 'uploaded_data'):
        return
    ctr_df = st.session_state.uploaded_data.get('ctrrate.csv', pd.DataFrame())
    delivery_df = st.session_state.uploaded_data.get('deliveryrate.csv', pd.DataFrame())
    
    if ctr_df.empty and delivery_df.empty:
        return
    
    # Apply date filter if set
    if st.session_state.get('date_range'):
        start_date, end_date = st.session_state.date_range
        if not ctr_df.empty:
            ctr_df = get_date_range_data(ctr_df, start_date, end_date)
        if not delivery_df.empty:
            delivery_df = get_date_range_data(delivery_df, start_date, end_date)
    
    fig = go.Figure()
    
    # Add CTR line
    if not ctr_df.empty:
        fig.add_trace(go.Scatter(
            x=ctr_df['timestamp'],
            y=ctr_df['value'],
            name='Click Through Rate',
            line=dict(color=CHART_COLORS['ctr'], width=3),
            marker=dict(size=6)
        ))
    
    # Add delivery rate line
    if not delivery_df.empty:
        fig.add_trace(go.Scatter(
            x=delivery_df['timestamp'],
            y=delivery_df['value'],
            name='Delivery Rate',
            line=dict(color=CHART_COLORS['delivery_rate'], width=3),
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title="CTR & Delivery Rate Over Time",
        xaxis_title="Date",
        yaxis_title="Percentage (%)",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)

def render_aov_chart():
    """Render AOV area chart"""
    if not hasattr(st.session_state, 'uploaded_data') or 'aovmobilepush.csv' not in st.session_state.uploaded_data:
        return
    
    aov_df = st.session_state.uploaded_data['aovmobilepush.csv']
    
    # Apply date filter if set
    if st.session_state.get('date_range'):
        start_date, end_date = st.session_state.date_range
        aov_df = get_date_range_data(aov_df, start_date, end_date)
    
    if aov_df.empty:
        return
    
    fig = px.area(
        aov_df,
        x='timestamp',
        y='value',
        title='Average Order Value (AOV) Over Time',
        color_discrete_sequence=[CHART_COLORS['aov']]
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="AOV ($)",
        hovermode='x unified',
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)

def render_campaign_performance_table():
    """Render campaign performance table"""
    if not hasattr(st.session_state, 'uploaded_data') or 'promotionalcampaignlevelperformancepush.csv' not in st.session_state.uploaded_data:
        return
    
    campaign_df = st.session_state.uploaded_data['promotionalcampaignlevelperformancepush.csv']
    
    if campaign_df.empty:
        return
    
    # Apply conditional formatting
    def highlight_ctr(val):
        if pd.isna(val):
            return ''
        if val > THRESHOLDS['ctr_high']:
            return 'background-color: #d4edda; color: #155724'
        elif val < THRESHOLDS['ctr_low']:
            return 'background-color: #f8d7da; color: #721c24'
        return ''
    
    def highlight_delivery_rate(val):
        if pd.isna(val):
            return ''
        if val > THRESHOLDS['delivery_rate_high']:
            return 'background-color: #d4edda; color: #155724'
        elif val < THRESHOLDS['delivery_rate_low']:
            return 'background-color: #f8d7da; color: #721c24'
        return ''
    
    # Format the dataframe for display
    display_df = campaign_df.copy()
    
    # Format percentage columns
    if '#3 Delivery Rate' in display_df.columns:
        display_df['#3 Delivery Rate'] = display_df['#3 Delivery Rate'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
    if '#4 Click Through Rate' in display_df.columns:
        display_df['#4 Click Through Rate'] = display_df['#4 Click Through Rate'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
    
    # Sort by delivered messages (descending)
    if '#1 All Delivered' in display_df.columns:
        display_df = display_df.sort_values('#1 All Delivered', ascending=False)
    
    st.markdown("### 📊 Campaign Performance Table")
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

def render_campaign_performance_chart():
    """Render top campaigns bar chart"""
    if not hasattr(st.session_state, 'uploaded_data') or 'promotionalcampaignlevelperformancepush.csv' not in st.session_state.uploaded_data:
        return
    
    campaign_df = st.session_state.uploaded_data['promotionalcampaignlevelperformancepush.csv']
    
    if campaign_df.empty or 'campaign_name' not in campaign_df.columns or '#1 All Delivered' not in campaign_df.columns:
        return
    
    # Get top 10 campaigns by delivered messages
    top_campaigns = campaign_df.nlargest(10, '#1 All Delivered')
    
    fig = px.bar(
        top_campaigns,
        x='#1 All Delivered',
        y='campaign_name',
        orientation='h',
        title='Top 10 Campaigns by Delivered Messages',
        color='#1 All Delivered',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        xaxis_title="Messages Delivered",
        yaxis_title="Campaign Name",
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True, config=CHART_CONFIG)

def render_download_section():
    """Render download reports section"""
    if not hasattr(st.session_state, 'uploaded_data') or not st.session_state.uploaded_data:
        return
    
    st.markdown("### 📥 Download Reports")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Download Summary Report (CSV)"):
            # Create summary report
            date_range = st.session_state.get('date_range', None)
            summary = calculate_metrics_summary(st.session_state.uploaded_data, date_range)
            
            # Convert to DataFrame
            summary_df = pd.DataFrame([summary])
            
            # Convert to CSV
            csv = summary_df.to_csv(index=False)
            
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"bloomreach_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📈 Download All Data (Excel)"):
            # Create Excel file with multiple sheets
            output = io.BytesIO()
            
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                for filename, df in st.session_state.uploaded_data.items():
                    sheet_name = filename.replace('.csv', '')[:31]  # Excel sheet name limit
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            output.seek(0)
            
            st.download_button(
                label="Download Excel",
                data=output.getvalue(),
                file_name=f"bloomreach_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

def render_empty_state():
    """Render empty state when no data is uploaded"""
    st.markdown("""
    <div class="empty-state">
        <h3>📱 Welcome to Bloomreach Mobile Push Analytics</h3>
        <p>Upload your data files to get started with comprehensive mobile push campaign analysis.</p>
        <p>Use the sidebar to upload the required data files and begin exploring your campaign performance.</p>
        <p><strong>Get insights into push sends, delivery rates, open rates, CTR, conversions, revenue, opt-outs, and top campaigns.</strong></p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    render_header()
    render_sidebar()
    
    # Check if data is uploaded
    if not hasattr(st.session_state, 'uploaded_data') or not st.session_state.uploaded_data:
        render_empty_state()
        return
    
    # Render dashboard content
    st.markdown('<h2 class="section-header">📱 PUSH NOTIFICATIONS — Daily Metrics</h2>', unsafe_allow_html=True)
    render_metrics_cards()
    
    st.markdown('<h2 class="section-header">📈 Performance Trends</h2>', unsafe_allow_html=True)
    
    # Charts in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        render_revenue_trend_chart()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        render_purchases_trend_chart()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Download section
    render_download_section()

if __name__ == "__main__":
    main()
