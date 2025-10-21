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

# CSS styles
CUSTOM_CSS = """
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4 0%, #17a2b8 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin: 0;
    }
    
    .trend-up {
        color: #2ca02c;
    }
    
    .trend-down {
        color: #d62728;
    }
    
    .trend-neutral {
        color: #6c757d;
    }
    
    .upload-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px dashed #dee2e6;
        margin-bottom: 2rem;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 0.5rem 0;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin: 0.5rem 0;
    }
    
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #6c757d;
    }
    
    .empty-state h3 {
        color: #343a40;
        margin-bottom: 1rem;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #1f77b4 0%, #17a2b8 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
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
