"""
Demo script to run the Bloomreach Mobile Push Analytics Dashboard
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit dashboard"""
    print("🚀 Starting Bloomreach Mobile Push Analytics Dashboard...")
    print("📱 Dashboard will be available at: http://localhost:8501")
    print("📊 Upload your CSV files using the sidebar to get started")
    print("=" * 60)
    
    try:
        # Run streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running dashboard: {e}")
        print("💡 Make sure you have installed all requirements: pip install -r requirements.txt")
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install it: pip install streamlit")

if __name__ == "__main__":
    main()
