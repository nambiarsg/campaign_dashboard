"""
Configuration file for Bloomreach Mobile Push Analytics Dashboard
Contains color schemes, thresholds, and styling constants
"""

# Color scheme for the dashboard
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e', 
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ff7f0e',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40',
    'white': '#ffffff',
    'gray': '#6c757d',
    'light_gray': '#e9ecef'
}

# Chart colors
CHART_COLORS = {
    'revenue': '#1f77b4',
    'purchases': '#ff7f0e',
    'buyers': '#2ca02c',
    'ctr': '#d62728',
    'delivery_rate': '#9467bd',
    'aov': '#8c564b'
}

# Performance thresholds
THRESHOLDS = {
    'ctr_high': 5.0,  # High CTR threshold (%)
    'ctr_low': 2.0,   # Low CTR threshold (%)
    'delivery_rate_high': 95.0,  # High delivery rate threshold (%)
    'delivery_rate_low': 80.0,   # Low delivery rate threshold (%)
}

# File column mappings
FILE_COLUMNS = {
    'aovmobilepush.csv': {
        'timestamp': 'timestamp',
        'value': 'AOV (Mobile Push)'
    },
    'ctrrate.csv': {
        'timestamp': 'timestamp', 
        'value': 'Click Through Rate From Delivered - Push Notification'
    },
    'deliveryrate.csv': {
        'timestamp': 'timestamp',
        'value': 'Delivery Rate - Push Notification'
    },
    'noofcustomerswithpurchasesattributedtopush.csv': {
        'timestamp': 'timestamp',
        'value': '# Buyers'
    },
    'noofpurchasesattributedtopush.csv': {
        'timestamp': 'timestamp',
        'value': 'Purchases (Mobile Push)'
    },
    'promotionalcampaignlevelperformancepush.csv': {
        'campaign_name': 'campaign_name',
        'sent': '#0 All Sent',
        'delivered': '#1 All Delivered', 
        'clicked': '#2 All Clicked',
        'delivery_rate': '#3 Delivery Rate',
        'ctr': '#4 Click Through Rate'
    },
    'revenue.csv': {
        'timestamp': 'timestamp',
        'value': 'Revenue from Mobile Push'
    }
}

# Date range presets
DATE_RANGES = {
    'Last 7 Days': 7,
    'Last 30 Days': 30,
    'Last 90 Days': 90,
    'All Time': None
}

# CSS styles - Modern Professional Dashboard (Updated: 2024-11-21)
CUSTOM_CSS = """
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Sidebar styling - Dark theme */
    .css-1d391kg {
        background-color: #2d1b69;
    }
    
    .css-1d391kg .css-1v0mbdj {
        background-color: #2d1b69;
    }
    
    /* Sidebar text */
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3, 
    .css-1d391kg p, .css-1d391kg div, .css-1d391kg label {
        color: white !important;
    }
    
    /* Sidebar file uploader */
    .css-1d391kg .stFileUploader {
        background-color: #3d2a79;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Main content area */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header styling */
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .dashboard-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .dashboard-header p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Modern metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2d1b69;
        margin: 0;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin: 0 0 0.5rem 0;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-trend {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    
    .trend-up {
        color: #28a745;
        font-weight: 600;
    }
    
    .trend-down {
        color: #dc3545;
        font-weight: 600;
    }
    
    .trend-neutral {
        color: #6c757d;
        font-weight: 600;
    }
    
    .trend-arrow {
        font-size: 1.2rem;
    }
    
    /* Chart containers */
    .chart-container {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #e9ecef;
        margin-bottom: 2rem;
    }
    
    .chart-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2d1b69;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* Upload section */
    .upload-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        border-radius: 12px;
        border: 2px dashed #dee2e6;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .upload-section h3 {
        color: #2d1b69;
        margin-bottom: 1rem;
    }
    
    /* Success/Error messages */
    .success-message {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 0.5rem 0;
        font-weight: 500;
    }
    
    .error-message {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
        margin: 0.5rem 0;
        font-weight: 500;
    }
    
    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        color: #6c757d;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    .empty-state h3 {
        color: #2d1b69;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    .empty-state p {
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2d1b69;
        margin: 2rem 0 1.5rem 0;
        text-align: center;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 2px;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .metric-value {
            font-size: 1.8rem;
        }
        
        .dashboard-header h1 {
            font-size: 2rem;
        }
        
        .chart-container {
            padding: 1rem;
        }
    }
</style>
"""

# Chart configuration
CHART_CONFIG = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'bloomreach_analytics',
        'height': 500,
        'width': 700,
        'scale': 2
    }
}
