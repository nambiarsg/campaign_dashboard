"""
Sample data generator for testing the Bloomreach Mobile Push Analytics Dashboard
This script creates sample CSV files with realistic data for demonstration purposes
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_data():
    """Generate sample CSV files for testing"""
    
    # Set random seed for reproducible data
    np.random.seed(42)
    
    # Generate date range (last 90 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    print("📊 Generating sample data files...")
    
    # 1. Revenue data
    revenue_data = []
    base_revenue = 1000
    for date in dates:
        # Add some trend and seasonality
        trend = 0.1 * (date - start_date).days / 90
        seasonality = 200 * np.sin(2 * np.pi * (date - start_date).days / 7)  # Weekly pattern
        noise = np.random.normal(0, 100)
        revenue = max(0, base_revenue + trend * 500 + seasonality + noise)
        revenue_data.append({'timestamp': date, 'Revenue from Mobile Push': revenue})
    
    revenue_df = pd.DataFrame(revenue_data)
    revenue_df.to_csv('sample_revenue.csv', index=False)
    print("✅ Generated sample_revenue.csv")
    
    # 2. Purchases data
    purchases_data = []
    base_purchases = 50
    for date in dates:
        trend = 0.05 * (date - start_date).days / 90
        seasonality = 10 * np.sin(2 * np.pi * (date - start_date).days / 7)
        noise = np.random.normal(0, 5)
        purchases = max(0, int(base_purchases + trend * 20 + seasonality + noise))
        purchases_data.append({'timestamp': date, 'Purchases (Mobile Push)': purchases})
    
    purchases_df = pd.DataFrame(purchases_data)
    purchases_df.to_csv('sample_noofpurchasesattributedtopush.csv', index=False)
    print("✅ Generated sample_noofpurchasesattributedtopush.csv")
    
    # 3. Buyers data
    buyers_data = []
    for i, date in enumerate(dates):
        # Buyers should be correlated with purchases but slightly lower
        base_buyers = purchases_data[i]['Purchases (Mobile Push)'] * 0.8
        noise = np.random.normal(0, 2)
        buyers = max(0, int(base_buyers + noise))
        buyers_data.append({'timestamp': date, '# Buyers': buyers})
    
    buyers_df = pd.DataFrame(buyers_data)
    buyers_df.to_csv('sample_noofcustomerswithpurchasesattributedtopush.csv', index=False)
    print("✅ Generated sample_noofcustomerswithpurchasesattributedtopush.csv")
    
    # 4. AOV data
    aov_data = []
    base_aov = 25
    for date in dates:
        trend = 0.02 * (date - start_date).days / 90
        seasonality = 2 * np.sin(2 * np.pi * (date - start_date).days / 14)  # Bi-weekly pattern
        noise = np.random.normal(0, 3)
        aov = max(5, base_aov + trend * 5 + seasonality + noise)
        aov_data.append({'timestamp': date, 'AOV (Mobile Push)': round(aov, 2)})
    
    aov_df = pd.DataFrame(aov_data)
    aov_df.to_csv('sample_aovmobilepush.csv', index=False)
    print("✅ Generated sample_aovmobilepush.csv")
    
    # 5. CTR data
    ctr_data = []
    base_ctr = 3.5
    for date in dates:
        trend = 0.01 * (date - start_date).days / 90
        seasonality = 0.5 * np.sin(2 * np.pi * (date - start_date).days / 30)  # Monthly pattern
        noise = np.random.normal(0, 0.3)
        ctr = max(0.5, min(8.0, base_ctr + trend * 2 + seasonality + noise))
        ctr_data.append({'timestamp': date, 'Click Through Rate From Delivered - Push Notification': round(ctr, 2)})
    
    ctr_df = pd.DataFrame(ctr_data)
    ctr_df.to_csv('sample_ctrrate.csv', index=False)
    print("✅ Generated sample_ctrrate.csv")
    
    # 6. Delivery rate data
    delivery_data = []
    base_delivery = 95
    for date in dates:
        trend = -0.005 * (date - start_date).days / 90  # Slight decline over time
        seasonality = 1 * np.sin(2 * np.pi * (date - start_date).days / 21)  # 3-week pattern
        noise = np.random.normal(0, 0.5)
        delivery = max(85, min(99, base_delivery + trend * 2 + seasonality + noise))
        delivery_data.append({'timestamp': date, 'Delivery Rate - Push Notification': round(delivery, 2)})
    
    delivery_df = pd.DataFrame(delivery_data)
    delivery_df.to_csv('sample_deliveryrate.csv', index=False)
    print("✅ Generated sample_deliveryrate.csv")
    
    # 7. Campaign performance data
    campaign_names = [
        "Summer Sale 2024", "Back to School", "Black Friday Prep", "Holiday Special",
        "New Product Launch", "Flash Sale Weekend", "Customer Retention", "Win-back Campaign",
        "Birthday Offers", "Loyalty Rewards", "Abandoned Cart", "Product Recommendations",
        "Seasonal Clearance", "Member Exclusive", "Limited Time Offer"
    ]
    
    campaign_data = []
    for campaign in campaign_names:
        sent = np.random.randint(10000, 100000)
        delivery_rate = np.random.uniform(88, 98)
        delivered = int(sent * delivery_rate / 100)
        ctr = np.random.uniform(1.5, 6.5)
        clicked = int(delivered * ctr / 100)
        
        campaign_data.append({
            'campaign_name': campaign,
            '#0 All Sent': sent,
            '#1 All Delivered': delivered,
            '#2 All Clicked': clicked,
            '#3 Delivery Rate': round(delivery_rate, 2),
            '#4 Click Through Rate': round(ctr, 2)
        })
    
    campaign_df = pd.DataFrame(campaign_data)
    campaign_df.to_csv('sample_promotionalcampaignlevelperformancepush.csv', index=False)
    print("✅ Generated sample_promotionalcampaignlevelperformancepush.csv")
    
    print("\n🎉 Sample data generation complete!")
    print("📁 Generated files:")
    print("   - sample_revenue.csv")
    print("   - sample_noofpurchasesattributedtopush.csv")
    print("   - sample_noofcustomerswithpurchasesattributedtopush.csv")
    print("   - sample_aovmobilepush.csv")
    print("   - sample_ctrrate.csv")
    print("   - sample_deliveryrate.csv")
    print("   - sample_promotionalcampaignlevelperformancepush.csv")
    print("\n💡 You can now upload these files to test the dashboard!")

if __name__ == "__main__":
    generate_sample_data()
