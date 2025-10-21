# 📱 Bloomreach Mobile Push Performance Analytics Dashboard

A professional Streamlit dashboard for analyzing mobile push campaign performance data from Bloomreach. This dashboard provides comprehensive insights into campaign metrics, trends, and performance analytics.

## 🚀 Features

### 📊 Key Metrics Dashboard
- **Total Revenue** with trend indicators
- **Total Purchases** with performance tracking
- **Total Buyers** with growth metrics
- **Average AOV** (Average Order Value) analysis
- **Average CTR** (Click Through Rate) monitoring
- **Average Delivery Rate** tracking

### 📈 Interactive Visualizations
- **Revenue Trend Chart** - Line chart showing revenue over time
- **Purchases & Buyers Chart** - Dual-axis chart for purchase and buyer trends
- **CTR & Delivery Rate Chart** - Performance metrics over time
- **AOV Trend Chart** - Area chart for average order value analysis
- **Campaign Performance Table** - Sortable table with conditional formatting
- **Top Campaigns Bar Chart** - Horizontal bar chart of top performing campaigns

### 🎯 Advanced Features
- **Date Range Filtering** - Filter data by custom date ranges or quick presets
- **File Upload Validation** - Ensures all required files are uploaded with correct columns
- **Download Reports** - Export summary reports as CSV or complete data as Excel
- **Responsive Design** - Mobile-friendly layout with professional styling
- **Real-time Updates** - Live data processing and visualization updates

## 📁 Required Data Files

The dashboard requires the following CSV files to be uploaded:

1. **aovmobilepush.csv**
   - Columns: `timestamp`, `AOV (Mobile Push)`

2. **ctrrate.csv**
   - Columns: `timestamp`, `Click Through Rate From Delivered - Push Notification`

3. **deliveryrate.csv**
   - Columns: `timestamp`, `Delivery Rate - Push Notification`

4. **noofcustomerswithpurchasesattributedtopush.csv**
   - Columns: `timestamp`, `# Buyers`

5. **noofpurchasesattributedtopush.csv**
   - Columns: `timestamp`, `Purchases (Mobile Push)`

6. **promotionalcampaignlevelperformancepush.csv**
   - Columns: `campaign_name`, `#0 All Sent`, `#1 All Delivered`, `#2 All Clicked`, `#3 Delivery Rate`, `#4 Click Through Rate`

7. **revenue.csv**
   - Columns: `timestamp`, `Revenue from Mobile Push`

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project files**
   ```bash
   # Navigate to your project directory
   cd "campaign dashboard"
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the dashboard**
   - Open your web browser
   - Navigate to `http://localhost:8501`
   - The dashboard will load automatically

## 📖 Usage Guide

### 1. Upload Data Files
- Use the sidebar to upload all required CSV files
- The system will validate file formats and required columns
- Success/error messages will guide you through the process

### 2. Filter Data by Date Range
- Use the date range selector in the sidebar
- Choose from quick presets: "Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"
- Or select custom date ranges using the date picker

### 3. Analyze Performance Metrics
- View key metrics cards at the top of the dashboard
- Each metric shows current value and trend indicators
- Green arrows (📈) indicate positive trends, red arrows (📉) indicate negative trends

### 4. Explore Visualizations
- Interactive charts allow zooming and hovering for detailed information
- All charts are responsive and update based on date range filters
- Use the legend to toggle data series on/off

### 5. Review Campaign Performance
- The campaign performance table shows all campaigns with conditional formatting
- Green highlighting indicates high performance (>5% CTR, >95% delivery rate)
- Red highlighting indicates areas needing attention (<2% CTR, <80% delivery rate)

### 6. Download Reports
- Generate summary reports as CSV files
- Download complete datasets as Excel files with multiple sheets
- Reports include filtered data based on selected date ranges

## 🎨 Customization

### Color Scheme
The dashboard uses a professional color palette defined in `config.py`:
- Primary: Blue (#1f77b4)
- Success: Green (#2ca02c)
- Danger: Red (#d62728)
- Warning: Orange (#ff7f0e)

### Performance Thresholds
Customize performance thresholds in `config.py`:
- High CTR: >5%
- Low CTR: <2%
- High Delivery Rate: >95%
- Low Delivery Rate: <80%

### Styling
Custom CSS styles are defined in `config.py` and can be modified to match your brand colors and preferences.

## 🔧 Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS styling
- **Data Processing**: Pandas for data manipulation and analysis
- **Visualizations**: Plotly for interactive charts
- **File Handling**: Built-in Streamlit file uploader with validation

### Performance Optimizations
- Data caching with `@st.cache_data` decorators
- Efficient pandas operations for large datasets
- Optimized chart rendering with Plotly
- Responsive design for fast loading

### Error Handling
- Comprehensive file validation
- Graceful handling of missing data
- User-friendly error messages
- Data type validation and conversion

## 📊 Data Processing

The dashboard automatically:
- Parses percentage strings (e.g., "95.5%" → 95.5)
- Converts timestamp strings to datetime objects
- Handles missing data gracefully
- Validates column names and data types
- Applies date range filtering across all datasets

## 🚨 Troubleshooting

### Common Issues

1. **File Upload Errors**
   - Ensure all required files are uploaded
   - Check that column names match exactly (case-sensitive)
   - Verify CSV files are properly formatted

2. **Date Range Issues**
   - Ensure timestamp columns contain valid date formats
   - Check for missing or invalid date values
   - Verify date range selection is logical

3. **Performance Issues**
   - Large datasets may take time to process
   - Use date range filtering to reduce data volume
   - Clear browser cache if charts don't load properly

4. **Missing Data**
   - Some metrics may show "0" or "N/A" if data is missing
   - Check that all required files contain data for the selected date range
   - Verify data quality in source files

## 📝 File Structure

```
campaign dashboard/
├── app.py                 # Main Streamlit application
├── utils.py              # Data processing utilities
├── config.py             # Configuration and styling
├── requirements.txt      # Python dependencies
├── README.md            # This documentation
└── .gitignore           # Git ignore file
```

## 🤝 Support

For technical support or feature requests:
1. Check the troubleshooting section above
2. Verify all requirements are met
3. Ensure data files are properly formatted
4. Review error messages in the dashboard sidebar

## 📄 License

This project is designed for internal use with Bloomreach mobile push campaign data. Please ensure compliance with your organization's data handling policies.

---

**Built with ❤️ using Streamlit, Pandas, and Plotly**
# campaign_dashboard
