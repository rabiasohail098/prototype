import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
from PIL import Image
import io
import base64

# Page Configuration
st.set_page_config(
    page_title="Luxemart Supply Chain AI Agent",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with Responsive Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #5a67d8 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E") repeat;
        opacity: 0.1;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    /* Card Styles */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 16px;
        color: #1a202c;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.5);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    .metric-card h3 {
        font-size: 2.2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .metric-card p {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Alert Cards */
    .alert-card {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 4px solid #ef4444;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.15);
    }
    
    .alert-card h4 {
        color: #dc2626;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .alert-card p {
        color: #7f1d1d;
        margin-bottom: 0.25rem;
    }
    
    .success-card {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        border-left: 4px solid #22c55e;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.15);
    }
    
    .success-card h4 {
        color: #15803d;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .success-card p {
        color: #14532d;
        margin-bottom: 0.25rem;
    }
    
    /* Chat System */
    .chat-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.5rem;
        border-radius: 16px;
        max-height: 400px;
        overflow-y: auto;
        margin-bottom: 1rem;
        border: 2px solid #e2e8f0;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.04);
    }
    
    .user-message {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        border-radius: 18px 18px 4px 18px;
        margin-left: 2rem;
        color: white;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        max-width: 80%;
        margin-left: auto;
        margin-right: 0;
    }
    
    .ai-message {
        background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        border-radius: 18px 18px 18px 4px;
        margin-right: 2rem;
        color: white;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(31, 41, 55, 0.3);
        border-left: 4px solid #10b981;
        max-width: 80%;
        margin-left: 0;
    }
    
    /* Enhanced Metrics */
    .enhanced-metric {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 1.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin: 0.75rem 0;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
        transition: all 0.3s ease;
    }
    
    .enhanced-metric:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4);
    }
    
    .enhanced-metric h3 {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    
    /* Sidebar Enhancements */
    .css-1d391kg { /* This might vary, target sidebar directly if possible */
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Button Styles */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        padding: 0.75rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* DataFrames */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        .metric-card h3 {
            font-size: 1.8rem;
        }
        
        .user-message, .ai-message {
            margin-left: 0.5rem;
            margin-right: 0.5rem;
            max-width: 95%;
        }
        
        .chat-container {
            padding: 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .main-header {
            padding: 1.5rem;
        }
        
        .main-header h1 {
            font-size: 1.5rem;
        }
        
        .metric-card h3 {
            font-size: 1.5rem;
        }
        
        .user-message, .ai-message {
            padding: 0.75rem 1rem;
            font-size: 0.9rem;
        }
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 2s infinite;
    }
    
    /* Glassmorphism Effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Status Indicators */
    .status-online {
        color: #10b981;
        font-weight: 600;
    }
    
    .status-offline {
        color: #ef4444;
        font-weight: 600;
    }
    
    .status-warning {
        color: #f59e0b;
        font-weight: 600;
    }
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        margin-top: 2rem;
        text-align: center;
    }
    
    /* Progress Bars */
    .stProgress .st-bo {
        background-color: #e2e8f0;
    }
    
    .stProgress .st-bp {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame({
        'Product': ['iPhone 15 Cover', 'Samsung Charger', 'Infinix Cable', 'Realme C51', 'iPhone Charger', 'Samsung Cover'],
        'Stock': [4, 8, 15, 22, 12, 6],
        'Min_Stock': [10, 15, 20, 30, 20, 10],
        'Daily_Sales': [7, 5, 8, 12, 6, 3],
        'Price': [1500, 800, 500, 35000, 2000, 1200],
        'Supplier': ['Supplier A', 'Supplier B', 'Supplier C', 'Supplier C', 'Supplier A', 'Supplier B'],
        'Category': ['Accessories', 'Accessories', 'Accessories', 'Mobile', 'Accessories', 'Accessories']
    })

# --- FIXED: Initialize search_results, show_search_analytics, search_history, chat_messages, and last_input ---
if 'search_results' not in st.session_state:
    st.session_state.search_results = pd.DataFrame() # Initialize as an empty DataFrame
if 'show_search_analytics' not in st.session_state:
    st.session_state.show_search_analytics = False
if 'search_history' not in st.session_state: 
    st.session_state.search_history = []
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "🙋‍♂️ Assalam-o-Alaikum! Main **Luxemart** ka AI Support Agent hun. \n\n📱 Main aap ki madad kar sakta hun:\n• Order tracking\n• Product information  \n• Delivery status\n• Returns & complaints\n• Price inquiries\n\nAap kya janna chahte hain?", "timestamp": datetime.now().strftime('%H:%M')}
    ]
if 'last_input' not in st.session_state: 
    st.session_state.last_input = None
# --- END FIX ---

if 'orders' not in st.session_state:
    st.session_state.orders = []

if 'suppliers' not in st.session_state:
    st.session_state.suppliers = pd.DataFrame({
        'Supplier': ['Supplier A', 'Supplier B', 'Supplier C'],
        'Location': ['China', 'Dubai', 'Turkey'],
        'Rating': [4.5, 4.2, 4.8],
        'Lead_Time': [7, 10, 5],
        'Contact': ['+86-123-456789', '+971-987-654321', '+90-555-123456']
    })

if 'deliveries' not in st.session_state:
    st.session_state.deliveries = pd.DataFrame({
        'Delivery_ID': [f'DEL{i+1000}' for i in range(5)],
        'City': ['Karachi', 'Lahore', 'Islamabad', 'Faisalabad', 'Multan'],
        'Status': ['In Transit', 'Delivered', 'Processing', 'Delayed', 'Delivered'],
        'Courier': ['TCS', 'Leopards', 'TCS', 'Blue Ex', 'TCS'],
        'Expected': [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 6)]
    })

if 'notifications' not in st.session_state:
    st.session_state.notifications = []

if 'voice_active' not in st.session_state:
    st.session_state.voice_active = False

if 'customers' not in st.session_state:
    st.session_state.customers = pd.DataFrame({
        'Customer_ID': [f'CUST{i+1001}' for i in range(5)],
        'Name': ['Ahmed Ali', 'Fatima Khan', 'Hassan Sheikh', 'Ayesha Malik', 'Usman Tariq'],
        'City': ['Karachi', 'Lahore', 'Islamabad', 'Karachi', 'Faisalabad'],
        'Phone': ['0300-1234567', '0321-9876543', '0333-1122334', '0345-5566778', '0301-9988776'],
        'Total_Orders': [12, 8, 15, 6, 10],
        'Status': ['VIP', 'Regular', 'VIP', 'New', 'Regular']
    })

if 'alerts' not in st.session_state:
    st.session_state.alerts = []

# Enhanced Responsive Sidebar
with st.sidebar:
    st.markdown("## 🤖 AI Agent Controls")
    
    # System Status with better indicators
    st.markdown("### System Status")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="status-online">🟢 Online</p>', unsafe_allow_html=True)
    with col2:
        st.markdown('<p class="status-online">🔄 Active</p>', unsafe_allow_html=True)
    
    # Progress indicators
    st.progress(0.95, "System Health: 95%")
    st.progress(0.88, "Performance: 88%")
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()
    
    st.success("✅ AI Agent Active")
    st.info(f"📅 Last Update: {datetime.now().strftime('%H:%M:%S')}")
    
    # Quick Actions with better layout
    st.markdown("### Quick Actions")
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        if st.button("🚨 Alert", use_container_width=True):
            alert = random.choice([
                "⚠️ iPhone Cover stock critically low!",
                "📦 New shipment arriving tomorrow",
                "🚚 Delivery delay in Karachi route",
                "💰 Price drop alert for Samsung products"
            ])
            st.session_state.alerts.append({
                'time': datetime.now().strftime('%H:%M'),
                'message': alert,
                'type': 'warning'
            })
            st.rerun()
    
    with action_col2:
        if st.button("📦 Reorder", use_container_width=True):
            low_stock_items = st.session_state.inventory[st.session_state.inventory['Stock'] < st.session_state.inventory['Min_Stock']]
            if not low_stock_items.empty:
                st.success(f"✅ Auto-ordered {len(low_stock_items)} items")
            else:
                st.info("ℹ️ All items in stock")

# Main Header with enhanced design
st.markdown("""
<div class="main-header">
    <h1>📱 Luxemart Supply Chain AI Agent</h1>
    <p>Next-Generation Intelligent Supply Chain Management Platform</p>
</div>
""", unsafe_allow_html=True)

# Enhanced Main Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Dashboard", 
    "📦 Inventory", 
    "🚚 Orders & Logistics", 
    "📈 Analytics", 
    "🗣️ Customer Support",
    "📸 Product Images",
    "🏢 Suppliers",
    "👥 Customer Management"
])

with tab1:
    st.markdown("## 📊 Real-time Dashboard")
    
    # Enhanced Key Metrics with responsive grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_stock = st.session_state.inventory['Stock'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <h3>{total_stock}</h3>
            <p>Total Stock Units</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        low_stock_count = len(st.session_state.inventory[st.session_state.inventory['Stock'] < st.session_state.inventory['Min_Stock']])
        st.markdown(f"""
        <div class="metric-card">
            <h3>{low_stock_count}</h3>
            <p>Low Stock Alerts</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_value = (st.session_state.inventory['Stock'] * st.session_state.inventory['Price']).sum()
        st.markdown(f"""
        <div class="metric-card">
            <h3>Rs {total_value:,}</h3>
            <p>Total Inventory Value</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_daily_sales = st.session_state.inventory['Daily_Sales'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>{avg_daily_sales:.1f}</h3>
            <p>Avg Daily Sales</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced Alerts Section
    st.markdown("## 🚨 Live Alerts & Notifications")
    
    # Check for low stock automatically
    low_stock_items = st.session_state.inventory[st.session_state.inventory['Stock'] < st.session_state.inventory['Min_Stock']]
    
    if not low_stock_items.empty:
        alert_col1, alert_col2 = st.columns([2, 1])
        
        with alert_col1:
            for _, item in low_stock_items.iterrows():
                days_left = item['Stock'] / item['Daily_Sales'] if item['Daily_Sales'] > 0 else 0
                st.markdown(f"""
                <div class="alert-card">
                    <h4>⚠️ Critical Stock Alert</h4>
                    <p><strong>{item['Product']}</strong> - Only {item['Stock']} units remaining</p>
                    <p>📅 Days remaining: {days_left:.1f} days</p>
                    <p>💡 Recommended: Order {item['Min_Stock'] * 2} units from {item['Supplier']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with alert_col2:
            st.markdown("### ⚡ Quick Actions")
            if st.button("🔄 Auto-Reorder All", use_container_width=True):
                st.success("✅ Auto-reorder initiated for all low stock items!")
                st.balloons()
            
            if st.button("📧 Notify Suppliers", use_container_width=True):
                st.success("📧 Suppliers notified successfully!")
    else:
        st.markdown("""
        <div class="success-card">
            <h4>✅ All Stock Levels Normal</h4>
            <p>No immediate action required. All products are above minimum stock levels.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display other alerts
    if st.session_state.alerts:
        st.markdown("### 📢 Recent Notifications")
        for alert in st.session_state.alerts[-3:]:
            st.markdown(f"""
            <div class="success-card">
                <h4>📢 {alert['time']}</h4>
                <p>{alert['message']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced Dashboard Charts
    st.markdown("## 📋 Analytics Overview")
    
    # Responsive chart layout
    chart_col1, chart_col2 = st.columns([3, 2])
    
    with chart_col1:
        st.markdown("### 📦 Current Stock Levels")
        inventory_fig = px.bar(
            st.session_state.inventory, 
            x='Product', 
            y='Stock',
            title='Real-time Inventory Status',
            color='Stock',
            color_continuous_scale='Viridis',
            text='Stock'
        )
        inventory_fig.update_traces(texttemplate='%{text}', textposition='outside')
        inventory_fig.update_layout(
            height=400,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif"),
            title_font_size=16
        )
        st.plotly_chart(inventory_fig, use_container_width=True)
    
    with chart_col2:
        st.markdown("### 💰 Revenue Distribution")
        category_revenue = st.session_state.inventory.groupby('Category').apply(
            lambda x: (x['Stock'] * x['Price']).sum()
        ).reset_index()
        category_revenue.columns = ['Category', 'Revenue']
        
        pie_fig = px.pie(
            category_revenue,
            values='Revenue',
            names='Category',
            title='Revenue by Category',
            hole=0.4
        )
        pie_fig.update_layout(
            height=400,
            font=dict(family="Inter, sans-serif"),
            title_font_size=16
        )
        st.plotly_chart(pie_fig, use_container_width=True)
        
        # Additional metrics in this column
        st.markdown("### 🎯 Performance KPIs")
        st.metric("Order Fulfillment", "94%", "2%")
        st.metric("Customer Satisfaction", "4.8/5", "0.1")
        st.metric("Delivery Time", "3.2 days", "-0.3")

with tab2:
    st.markdown("## 🔍 Smart Search & Advanced Filters")
    
    # Advanced Search Interface
    st.markdown("### 🎯 Advanced Product Search")
    
    search_main_col1, search_main_col2 = st.columns([2, 1])
    
    with search_main_col1:
        # Helper function for product search
        def search_products(query):
            df = st.session_state.inventory
            query = query.lower()
            mask = (
                df['Product'].str.lower().str.contains(query)
                | df['Category'].str.lower().str.contains(query)
                | df['Supplier'].str.lower().str.contains(query)
            )
            return df[mask]

        # Main search bar
        advanced_search = st.text_input(
            "🔍 Enter search query",
            value="",
            placeholder="Search by product name, category, supplier, or any keyword...",
            key="advanced_search_main"
        )
        
        # Search options
        search_opt_col1, search_opt_col2, search_opt_col3 = st.columns(3)
        
        with search_opt_col1:
            search_category = st.selectbox(
                "Category Filter",
                ["All Categories"] + st.session_state.inventory['Category'].unique().tolist(), # type: ignore
                key="adv_category"
            )
        
        with search_opt_col2:
            search_supplier = st.selectbox(
                "Supplier Filter", 
                ["All Suppliers"] + st.session_state.inventory['Supplier'].unique().tolist(), # type: ignore
                key="adv_supplier"
            )
        
        with search_opt_col3:
            price_range = st.select_slider(
                "Price Range (Rs)",
                options=["All", "0-1K", "1K-5K", "5K-20K", "20K-50K", "50K+"],
                value="All",
                key="adv_price"
            )
    
    with search_main_col2:
        st.markdown("#### 🎛️ Search Controls")
        
        if st.button("🔍 Advanced Search", use_container_width=True, key="do_advanced_search"):
            # Perform advanced search
            search_results = st.session_state.inventory.copy()
            
            # Apply text search
            if advanced_search:
                search_results = search_products(advanced_search)
                # Add to history only if a search query was actually entered
                if advanced_search not in st.session_state.search_history:
                    st.session_state.search_history.insert(0, advanced_search) # Add to front
                    st.session_state.search_history = st.session_state.search_history[:5] # Keep last 5
            
            # Apply category filter
            if search_category != "All Categories":
                search_results = search_results[search_results['Category'] == search_category]
            
            # Apply supplier filter
            if search_supplier != "All Suppliers":
                search_results = search_results[search_results['Supplier'] == search_supplier]
            
            # Apply price filter
            if price_range != "All":
                if price_range == "0-1K":
                    search_results = search_results[search_results['Price'] <= 1000]
                elif price_range == "1K-5K":
                    search_results = search_results[(search_results['Price'] > 1000) & (search_results['Price'] <= 5000)]
                elif price_range == "5K-20K":
                    search_results = search_results[(search_results['Price'] > 5000) & (search_results['Price'] <= 20000)]
                elif price_range == "20K-50K":
                    search_results = search_results[(search_results['Price'] > 20000) & (search_results['Price'] <= 50000)]
                elif price_range == "50K+":
                    search_results = search_results[search_results['Price'] > 50000]
            
            st.session_state.search_results = search_results
        
        if st.button("🔄 Reset Filters", use_container_width=True):
            st.session_state.search_results = pd.DataFrame()
            st.session_state.show_search_analytics = False
            st.rerun()
        
        if st.button("📊 Search Analytics", use_container_width=True):
            st.session_state.show_search_analytics = True
    
    # Quick Search Buttons
    st.markdown("### ⚡ Quick Searches")
    quick_search_cols = st.columns(6)
    
    quick_searches = [
        ("📱 iPhones", "iPhone"),
        ("🔌 Chargers", "charger"),
        ("📶 Samsung", "Samsung"),
        ("🔴 Low Stock", "low_stock"),
        ("💰 Under 5K", "under_5k"),
        ("🎯 Best Sellers", "best_sellers")
    ]
    
    for i, (label, search_term) in enumerate(quick_searches):
        with quick_search_cols[i]:
            if st.button(label, key=f"quick_{search_term}", use_container_width=True):
                if search_term == "low_stock":
                    search_results = st.session_state.inventory[
                        st.session_state.inventory['Stock'] < st.session_state.inventory['Min_Stock']
                    ]
                    st.session_state.search_history.insert(0, "Low Stock Items")
                elif search_term == "under_5k":
                    search_results = st.session_state.inventory[st.session_state.inventory['Price'] < 5000]
                    st.session_state.search_history.insert(0, "Products Under 5K")
                elif search_term == "best_sellers":
                    search_results = st.session_state.inventory.nlargest(5, 'Daily_Sales')
                    st.session_state.search_history.insert(0, "Best Sellers")
                else:
                    search_results = search_products(search_term)
                    st.session_state.search_history.insert(0, f"'{search_term}'")
                
                st.session_state.search_history = st.session_state.search_history[:5] # Keep last 5
                st.session_state.search_results = search_results
                st.rerun()
    
    # Display Search Results
    if not st.session_state.search_results.empty:
        st.markdown("---")
        st.markdown(f"### 📋 Search Results ({len(st.session_state.search_results)} items found)")
        
        # Search results with enhanced display
        results_display = st.session_state.search_results.copy()
        results_display['Stock_Status'] = results_display.apply(
            lambda x: '🔴 Critical' if x['Stock'] < x['Min_Stock'] 
            else '🟡 Low' if x['Stock'] < x['Min_Stock'] * 1.5 
            else '🟢 Good', axis=1
        )
        results_display['Days_Left'] = results_display['Stock'] / results_display['Daily_Sales']
        results_display['Total_Value'] = results_display['Stock'] * results_display['Price']
        
        # Interactive table
        st.dataframe(
            results_display[['Product', 'Category', 'Stock', 'Stock_Status', 'Price', 'Total_Value', 'Supplier', 'Days_Left']],
            use_container_width=True
        )
        
        # Results summary
        col_summary1, col_summary2, col_summary3, col_summary4 = st.columns(4)
        
        with col_summary1:
            st.metric("Products Found", len(results_display))
        with col_summary2:
            st.metric("Total Stock Value", f"Rs {results_display['Total_Value'].sum():,}")
        with col_summary3:
            st.metric("Avg Price", f"Rs {results_display['Price'].mean():,.0f}")
        with col_summary4:
            critical_count = len(results_display[results_display['Stock_Status'] == '🔴 Critical'])
            st.metric("Critical Stock Items", critical_count)
        
        # Action buttons for search results
        st.markdown("#### 🎯 Actions on Search Results")
        action_cols = st.columns(5)
        
        with action_cols[0]:
            if st.button("📦 Bulk Reorder Selected", key="bulk_reorder_results"):
                reorder_items = results_display[results_display['Stock_Status'] == '🔴 Critical']
                if not reorder_items.empty:
                    st.success(f"✅ Bulk reorder initiated for {len(reorder_items)} critical items")
                else:
                    st.info("No critical stock items to reorder")
        
        with action_cols[1]:
            if st.button("📊 Detailed Report", key="detailed_report"):
                st.info("📋 Generating detailed analysis report...")
                # You could expand this to show more detailed analytics
        
        with action_cols[2]:
            if st.button("📤 Export Results", key="export_results"):
                csv = results_display.to_csv(index=False)
                st.download_button(
                    "💾 Download CSV",
                    csv,
                    f"search_results_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    "text/csv",
                    key="download_search_csv"
                )
        
        with action_cols[3]:
            if st.button("📱 Share Results", key="share_results"):
                st.success("🔗 Shareable link generated for search results")
        
        with action_cols[4]:
            if st.button("📈 Visual Analysis", key="visual_analysis"):
                st.session_state.show_search_analytics = True # Set flag to show analytics
    
    # Show Search Analytics if flag is true
    if st.session_state.show_search_analytics:
        st.markdown("#### 📊 Search Results Visualization")
        
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            # Stock status pie chart
            status_counts = results_display['Stock_Status'].value_counts() # type: ignore
            fig_status = px.pie(
                values=status_counts.values,
                names=status_counts.index,
                title="Stock Status Distribution"
            )
            st.plotly_chart(fig_status, use_container_width=True)
        
        with viz_col2:
            # Price distribution bar chart
            fig_price = px.bar(
                results_display.head(10), # type: ignore
                x='Product',
                y='Price',
                title="Price Comparison (Top 10)",
                color='Price'
            )
            fig_price.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_price, use_container_width=True)
    
    # Search History
    st.markdown("---")
    st.markdown("### 🕘 Search History")
    if st.session_state.search_history:
        for i, query in enumerate(st.session_state.search_history):
            st.markdown(f"🔍 {i+1}. {query}")
    else:
        st.info("No search history yet.")


with tab3:
    st.markdown("## 🚚 Orders & Logistics Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Create New Order")
        with st.form("new_order"):
            customer_name = st.text_input("Customer Name")
            customer_city = st.selectbox("City", ["Karachi", "Lahore", "Islamabad", "Faisalabad", "Multan"])
            selected_product = st.selectbox("Product", st.session_state.inventory['Product'].tolist())
            quantity = st.number_input("Quantity", min_value=1, value=1)
            
            if st.form_submit_button("Create Order"):
                # Check if stock is available
                product_stock = st.session_state.inventory[st.session_state.inventory['Product'] == selected_product]['Stock'].iloc[0]
                
                if quantity <= product_stock:
                    # Create order
                    order_id = f"LUX{random.randint(1000, 9999)}"
                    new_order = {
                        'Order_ID': order_id,
                        'Customer': customer_name,
                        'City': customer_city,
                        'Product': selected_product,
                        'Quantity': quantity,
                        'Status': 'Processing',
                        'Created': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'Delivery_Date': (datetime.now() + timedelta(days=random.randint(2, 5))).strftime('%Y-%m-%d')
                    }
                    
                    st.session_state.orders.append(new_order)
                    
                    # Update inventory
                    idx = st.session_state.inventory[st.session_state.inventory['Product'] == selected_product].index[0]
                    st.session_state.inventory.loc[idx, 'Stock'] -= quantity # type: ignore
                    
                    st.success(f"✅ Order {order_id} created successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ Insufficient stock! Only {product_stock} units available.")
    
    with col2:
        st.markdown("### 📊 Delivery Analytics")
        
        # Simulate delivery data
        delivery_cities = ['Karachi', 'Lahore', 'Islamabad', 'Faisalabad', 'Multan']
        delivery_data = pd.DataFrame({
            'City': delivery_cities,
            'Orders': [random.randint(5, 25) for _ in delivery_cities],
            'Avg_Delivery_Time': [random.randint(2, 7) for _ in delivery_cities]
        })
        
        fig = px.bar(delivery_data, x='City', y='Orders', title='Orders by City')
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent Orders
    st.markdown("### 📦 Recent Orders")
    if st.session_state.orders:
        orders_df = pd.DataFrame(st.session_state.orders)
        st.dataframe(orders_df, use_container_width=True)
        
        # Order tracking
        st.markdown("### 🔍 Order Tracking")
        if orders_df.shape[0] > 0:
            selected_order = st.selectbox("Select Order to Track", orders_df['Order_ID'].tolist())
            order_details = orders_df[orders_df['Order_ID'] == selected_order].iloc[0]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"**Order ID:** {order_details['Order_ID']}")
                st.info(f"**Customer:** {order_details['Customer']}")
            with col2:
                st.info(f"**Product:** {order_details['Product']}")
                st.info(f"**Quantity:** {order_details['Quantity']}")
            with col3:
                st.info(f"**Status:** {order_details['Status']}")
                st.info(f"**Delivery Date:** {order_details['Delivery_Date']}")
    else:
        st.info("📋 No orders yet. Create your first order above!")

with tab4:
    st.markdown("## 📈 Supply Chain Analytics")
    
    # Sales Forecast
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Sales Forecast")
        
        # Generate forecast data
        dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
        forecast_data = pd.DataFrame({
            'Date': dates,
            'Predicted_Sales': [random.randint(15, 45) for _ in range(30)],
            'Confidence_Lower': [random.randint(10, 25) for _ in range(30)],
            'Confidence_Upper': [random.randint(35, 55) for _ in range(30)]
        })
        
        forecast_fig = go.Figure()
        forecast_fig.add_trace(go.Scatter(
            x=forecast_data['Date'],
            y=forecast_data['Predicted_Sales'],
            mode='lines',
            name='Predicted Sales',
            line=dict(color='blue')
        ))
        
        forecast_fig.add_trace(go.Scatter(
            x=forecast_data['Date'],
            y=forecast_data['Confidence_Upper'],
            mode='lines',
            line=dict(width=0),
            showlegend=False
        ))
        
        forecast_fig.add_trace(go.Scatter(
            x=forecast_data['Date'],
            y=forecast_data['Confidence_Lower'],
            mode='lines',
            fill='tonexty',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(width=0),
            name='Confidence Interval'
        ))
        
        forecast_fig.update_layout(title='30-Day Sales Forecast', height=400)
        st.plotly_chart(forecast_fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Performance Metrics")
        
        # Performance metrics
        metrics = {
            'Order Fulfillment Rate': '94%',
            'Average Delivery Time': '3.2 days',
            'Stock Accuracy': '98%',
            'Customer Satisfaction': '4.7/5',
            'Cost Reduction': '12%',
            'Inventory Turnover': '8.5x'
        }
        
        for metric, value in metrics.items():
            st.metric(metric, value)
    
    # Trend Analysis
    st.markdown("### 📈 Trend Analysis")
    
    # Generate trend data
    trend_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Revenue': [120000, 135000, 148000, 162000, 175000, 189000],
        'Orders': [450, 520, 580, 640, 710, 780],
        'Customer_Satisfaction': [4.2, 4.3, 4.5, 4.6, 4.7, 4.8]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        revenue_fig = px.line(trend_data, x='Month', y='Revenue', title='Monthly Revenue Trend')
        st.plotly_chart(revenue_fig, use_container_width=True)
    
    with col2:
        orders_fig = px.line(trend_data, x='Month', y='Orders', title='Monthly Orders Trend', color_discrete_sequence=['orange'])
        st.plotly_chart(orders_fig, use_container_width=True)

with tab5:
    st.markdown("## 🗣️ Customer Support AI Assistant")
    
    # chat_messages initialized at the top now
    
    # Helper function for intelligent responses
    def get_ai_response(user_message):
        message_lower = user_message.lower()
        
        # Order tracking
        if any(word in message_lower for word in ['order', 'track', 'tracking', 'lux', 'status']):
            if st.session_state.orders:
                order_list = "\n".join([f"• {order['Order_ID']} - {order['Status']}" for order in st.session_state.orders[-3:]])
                return f"📦 **Recent Orders:**\n{order_list}\n\nKya aap koi specific Order ID track karna chahte hain?"
            else:
                return "📋 Abhi tak koi order nahi hai. Kya aap naya order place karna chahte hain?"
        
        # Product inquiries
        elif any(word in message_lower for word in ['product', 'mobile', 'phone', 'cover', 'charger', 'cable']):
            available_products = st.session_state.inventory[['Product', 'Stock', 'Price']].head(3)
            product_info = ""
            for _, product in available_products.iterrows():
                stock_status = "✅ Available" if product['Stock'] > 0 else "❌ Out of Stock"
                product_info += f"• **{product['Product']}** - Rs {product['Price']:,} ({stock_status})\n"
            return f"📱 **Available Products:**\n{product_info}\nKya aap koi specific product ke bare mein janna chahte hain?"
        
        # Price inquiries
        elif any(word in message_lower for word in ['price', 'cost', 'rate', 'kitna', 'paisa']):
            return "💰 **Price List:**\n• iPhone Accessories: Rs 1,500 - 2,000\n• Samsung Products: Rs 800 - 1,500\n• Cables & Chargers: Rs 500 - 800\n• Mobile Phones: Rs 35,000+\n\nKis product ka exact price chahiye?"
        
        # Delivery inquiries
        elif any(word in message_lower for word in ['delivery', 'deliver', 'shipping', 'transport', 'pohanchana']):
            return "🚚 **Delivery Information:**\n• Karachi: 1-2 days\n• Lahore: 2-3 days\n• Islamabad: 2-3 days\n• Other cities: 3-5 days\n\n📦 Free delivery on orders above Rs 5,000!\nKya aap apna city bata sakte hain?"
        
        # Return/complaint
        elif any(word in message_lower for word in ['return', 'complaint', 'problem', 'issue', 'defect', 'kharab']):
            return "🔄 **Return Policy:**\n• 7 days return guarantee\n• Product original condition mein hona chahiye\n• Bill/receipt zaroori hai\n\n📞 Complaint ke liye:\n• Call: 0300-LUXEMART\n• WhatsApp: Same number\n\nMain aap ki complaint forward kar deta hun manager ko."
        
        # Greetings
        elif any(word in message_lower for word in ['salam', 'hello', 'hi', 'hey', 'assalam']):
            return "🙋‍♂️ Wa alaikum assalam! Luxemart mein aap ka swagat hai. Main aap ki kya madad kar sakta hun?"
        
        # Thanks
        elif any(word in message_lower for word in ['thanks', 'thank you', 'shukriya', 'dhanyawad']):
            return "😊 Aap ka bahut shukriya! Kya aur koi madad chahiye? Main hamesha yahan hun!"
        
        # Default response with suggestions
        else:
            return f"🤔 Main samajh gaya ke aap **'{user_message}'** ke bare mein pooch rahe hain.\n\n💡 **Main yeh madad kar sakta hun:**\n• Order status check karna\n• Product information dena\n• Delivery time batana\n• Return process explain karna\n\nKya aap koi specific cheez poochna chahte hain?"
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Live Chat Support")
        
        # Chat container with custom styling
        chat_container = st.container()
        
        with chat_container:
            # Display chat messages with enhanced styling
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            for i, message in enumerate(st.session_state.chat_messages):
                timestamp = message.get('timestamp', datetime.now().strftime('%H:%M'))
                
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>👤 You ({timestamp}):</strong><br>
                        <span style="color: white; font-size: 14px;">{message['content']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="ai-message">
                        <strong>🤖 Luxemart AI ({timestamp}):</strong><br>
                        <span style="color: white; font-size: 14px;">{message['content']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input with better UX
        st.markdown("---")
        col_input, col_send = st.columns([4, 1])
        
        with col_input:
            user_input = st.text_input(
                "Type your message...", 
                key="chat_input",
                placeholder="Jaise: 'Order track karna hai' ya 'iPhone cover ka price?'"
            )
        
        with col_send:
            send_clicked = st.button("📤 Send", use_container_width=True)
        
        # Process user input
        if (send_clicked and user_input) or (user_input and st.session_state.get('last_input') != user_input and user_input.strip() != ''): # Added check for empty string
            if user_input.strip():
                # Add user message
                timestamp = datetime.now().strftime('%H:%M')
                st.session_state.chat_messages.append({
                    "role": "user", 
                    "content": user_input,
                    "timestamp": timestamp
                })
                
                # Generate AI response
                ai_response = get_ai_response(user_input)
                st.session_state.chat_messages.append({
                    "role": "assistant", 
                    "content": ai_response,
                    "timestamp": timestamp
                })
                
                st.session_state.last_input = user_input
                st.rerun()
        
        # Quick action buttons
        st.markdown("### ⚡ Quick Actions")
        quick_col1, quick_col2, quick_col3 = st.columns(3)
        
        with quick_col1:
            if st.button("📦 Track My Order"):
                timestamp = datetime.now().strftime('%H:%M')
                st.session_state.chat_messages.append({
                    "role": "user", 
                    "content": "Track my order",
                    "timestamp": timestamp
                })
                response = get_ai_response("track my order")
                st.session_state.chat_messages.append({
                    "role": "assistant", 
                    "content": response,
                    "timestamp": timestamp
                })
                st.rerun()
        
        with quick_col2:
            if st.button("💰 Check Prices"):
                timestamp = datetime.now().strftime('%H:%M')
                st.session_state.chat_messages.append({
                    "role": "user", 
                    "content": "Price list chahiye",
                    "timestamp": timestamp
                })
                response = get_ai_response("price list")
                st.session_state.chat_messages.append({
                    "role": "assistant", 
                    "content": response,
                    "timestamp": timestamp
                })
                st.rerun()
        
        with quick_col3:
            if st.button("🚚 Delivery Info"):
                timestamp = datetime.now().strftime('%H:%M')
                st.session_state.chat_messages.append({
                    "role": "user", 
                    "content": "Delivery time batao",
                    "timestamp": timestamp
                })
                response = get_ai_response("delivery time")
                st.session_state.chat_messages.append({
                    "role": "assistant", 
                    "content": response,
                    "timestamp": timestamp
                })
                st.rerun()
        
        # Clear chat option
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_messages = [
                {"role": "assistant", "content": "🙋‍♂️ Chat history clear ho gaya! Main dobara aap ki madad ke liye hazir hun.", "timestamp": datetime.now().strftime('%H:%M')}
            ]
            st.rerun()
    
    with col2:
        st.markdown("### 🎯 Support Dashboard")
        
        # Real-time support stats
        total_messages = len(st.session_state.chat_messages)
        user_messages = len([msg for msg in st.session_state.chat_messages if msg['role'] == 'user'])
        
        st.metric("Chat Messages", total_messages)
        st.metric("User Queries", user_messages)
        st.metric("Response Rate", "100%")
        
        st.markdown("---")
        
        st.markdown("### 📞 Contact Options")
        
        contact_info = """
        **📱 WhatsApp:** 0300-LUXEMART
        **☎️ Call Center:** 021-LUXEMART  
        **✉️ Email:** support@luxemart.pk
        **🕒 Hours:** 9 AM - 9 PM (7 days)
        """
        st.markdown(contact_info)
        
        st.markdown("---")
        
        st.markdown("### 🎤 Advanced Voice Support")
        
        col_voice1, col_voice2 = st.columns(2)
        with col_voice1:
            if st.button("🎵 Start Voice Chat", key="voice_start", use_container_width=True):
                st.session_state.voice_active = True
                timestamp = datetime.now().strftime('%H:%M')
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": "🎤 **Voice Support Activated!**\n\n✅ Main ab aap ki voice sun sakta hun\n🗣️ Clearly boliye main samjhunga\n📱 Voice-to-text conversion active hai\n\n*Demo mode: Voice integration complete karne ke liye microphone API setup karni hogi*",
                    "timestamp": timestamp
                })
                st.success("🎤 Voice activated!")
                st.rerun()
        
        with col_voice2:
            if st.button("⏹️ Stop Voice", key="voice_stop", use_container_width=True):
                st.session_state.voice_active = False
                st.info("🔇 Voice deactivated")
        
        if st.session_state.voice_active:
            st.success("🎤 **LIVE** - Voice listening mode active")
            
            # Simulate voice input (in real implementation, you'd use speech recognition)
            voice_commands = [
                "Order track karo",
                "Price list batao", 
                "Delivery time kya hai",
                "Return policy explain karo"
            ]
            
            selected_voice_cmd = st.selectbox(
                "🎤 Voice Command Simulation:", 
                ["Select a command..."] + voice_commands,
                key="voice_sim"
            )
            
            if selected_voice_cmd != "Select a command..." and st.button("🎵 Process Voice"):
                timestamp = datetime.now().strftime('%H:%M')
                st.session_state.chat_messages.append({
                    "role": "user",
                    "content": f"🎤 [Voice]: {selected_voice_cmd}",
                    "timestamp": timestamp
                })
                
                response = get_ai_response(selected_voice_cmd)
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": f"🔊 [Voice Response]: {response}",
                    "timestamp": timestamp
                })
                st.rerun()
        
        st.markdown("### 📊 Live Support Stats")
        
        # Dynamic stats based on actual chat
        current_hour = datetime.now().hour
        support_stats = {
            "Active Chats": random.randint(15, 45),
            "Queue Wait": f"{random.randint(0, 3)} min",
            "Satisfaction": "4.9/5 ⭐",
            "Online Agents": random.randint(8, 12)
        }
        
        for stat, value in support_stats.items():
            st.metric(stat, value)
        
        # FAQ Section
        st.markdown("### ❓ Common Questions")
        
        faqs = [
            ("Order tracking kaise kare?", "Order ID aur mobile number chahiye"),
            ("Return policy kya hai?", "7 days return guarantee"),
            ("Delivery charges kitne?", "Rs 150, free above Rs 5000"),
            ("Payment methods?", "Cash, Card, JazzCash, EasyPaisa")
        ]
        
        for question, answer in faqs:
            if st.button(f"❓ {question}", key=f"faq_{question}"):
                timestamp = datetime.now().strftime('%H:%M')
                st.session_state.chat_messages.append({
                    "role": "user",
                    "content": question,
                    "timestamp": timestamp
                })
                st.session_state.chat_messages.append({
                    "role": "assistant", 
                    "content": f"📋 **{question}**\n\n✅ {answer}",
                    "timestamp": timestamp
                })
                st.rerun()

with tab6:
    st.markdown("## 📸 Product Image Management")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📷 Upload Product Images")
        
        selected_product_img = st.selectbox("Select Product for Image", st.session_state.inventory['Product'].tolist(), key="img_product")
        
        uploaded_file = st.file_uploader(
            "Choose product image", 
            type=['png', 'jpg', 'jpeg'],
            help="Upload high quality product images for better customer experience"
        )
        
        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Image for {selected_product_img}", use_column_width=True)
            
            if st.button("Save Image"):
                st.success(f"✅ Image saved for {selected_product_img}")
        
        st.markdown("### 🔍 AI Image Analysis")
        if uploaded_file is not None:
            st.markdown("**AI Analysis:**")
            analysis = {
                "Image Quality": "High ✅",
                "Background": "Clean ✅", 
                "Product Visibility": "Clear ✅",
                "Lighting": "Good ✅",
                "Recommendation": "Perfect for e-commerce listing!"
            }
            
            for key, value in analysis.items():
                st.write(f"**{key}:** {value}")
    
    with col2:
        st.markdown("### 🖼️ Product Gallery")
        
        # Sample product images (placeholder)
        sample_products = [
            "iPhone 15 Cover",
            "Samsung Charger", 
            "Infinix Cable",
            "Realme C51"
        ]
        
        for product in sample_products:
            with st.expander(f"📱 {product}"):
                st.write("📸 Image placeholder - Upload actual product image")
                st.write(f"**Category:** {st.session_state.inventory[st.session_state.inventory['Product'] == product]['Category'].iloc[0] if product in st.session_state.inventory['Product'].values else 'N/A'}")
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    if st.button(f"Edit", key=f"edit_{product}"):
                        st.info(f"Opening editor for {product}")
                with col_b:
                    if st.button(f"Delete", key=f"delete_{product}"):
                        st.warning(f"Image deleted for {product}")
                with col_c:
                    if st.button(f"Share", key=f"share_{product}"):
                        st.success(f"Sharing link generated for {product}")
        
        st.markdown("### 📊 Image Statistics")
        img_stats = {
            "Total Images": 24,
            "High Quality": 18,
            "Needs Update": 3,
            "Missing Images": 3
        }
        
        for stat, value in img_stats.items():
            st.metric(stat, value)

with tab7:
    st.markdown("## 🏢 Supplier Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 Supplier Database")
        
        # Display suppliers with enhanced info
        supplier_display = st.session_state.suppliers.copy()
        supplier_display['Performance'] = supplier_display['Rating'].apply(
            lambda x: '🟢 Excellent' if x >= 4.5 else '🟡 Good' if x >= 4.0 else '🔴 Needs Improvement'
        )
        
        st.dataframe(
            supplier_display[['Supplier', 'Location', 'Rating', 'Lead_Time', 'Performance', 'Contact']],
            use_container_width=True
        )
        
        st.markdown("### 📞 Supplier Communication")
        selected_supplier = st.selectbox("Select Supplier", st.session_state.suppliers['Supplier'].tolist())
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("📧 Send Email"):
                st.success(f"✅ Email sent to {selected_supplier}")
        with col_b:
            if st.button("📱 WhatsApp"):
                supplier_contact = st.session_state.suppliers[st.session_state.suppliers['Supplier'] == selected_supplier]['Contact'].iloc[0]
                st.success(f"✅ WhatsApp opened: {supplier_contact}")
        with col_c:
            if st.button("📋 New Order"):
                st.info(f"📦 Opening order form for {selected_supplier}")
    
    with col2:
        st.markdown("### 📊 Supplier Analytics")
        
        # Supplier performance chart
        perf_fig = px.bar(
            st.session_state.suppliers,
            x='Supplier',
            y='Rating',
            title='Supplier Performance Ratings',
            color='Rating',
            color_continuous_scale='Viridis'
        )
        perf_fig.update_layout(height=300)
        st.plotly_chart(perf_fig, use_container_width=True)
        
        st.markdown("### ⏱️ Lead Times")
        lead_fig = px.pie(
            st.session_state.suppliers,
            values='Lead_Time',
            names='Supplier',
            title='Lead Time Distribution'
        )
        lead_fig.update_layout(height=300)
        st.plotly_chart(lead_fig, use_container_width=True)
        
        st.markdown("### 📈 Quick Stats")
        avg_rating = st.session_state.suppliers['Rating'].mean()
        avg_lead_time = st.session_state.suppliers['Lead_Time'].mean()
        
        st.metric("Average Rating", f"{avg_rating:.1f}/5.0")
        st.metric("Average Lead Time", f"{avg_lead_time:.0f} days")
        st.metric("Total Suppliers", len(st.session_state.suppliers))

with tab8:
    st.markdown("## 👥 Customer Management & CRM")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 👤 Customer Database")
        
        # Enhanced customer display
        customer_display = st.session_state.customers.copy()
        customer_display['Loyalty_Level'] = customer_display['Total_Orders'].apply(
            lambda x: '🌟 VIP' if x >= 15 else '💎 Premium' if x >= 10 else '🥉 Regular' if x >= 5 else '🆕 New'
        )
        
        st.dataframe(
            customer_display[['Customer_ID', 'Name', 'City', 'Phone', 'Total_Orders', 'Loyalty_Level', 'Status']],
            use_container_width=True
        )
        
        st.markdown("### 📞 Customer Communication")
        selected_customer = st.selectbox("Select Customer", st.session_state.customers['Name'].tolist())
        
        customer_info = st.session_state.customers[st.session_state.customers['Name'] == selected_customer].iloc[0]
        
        col_x, col_y, col_z = st.columns(3)
        with col_x:
            st.info(f"📱 **Phone:** {customer_info['Phone']}")
        with col_y:
            st.info(f"🏢 **City:** {customer_info['City']}")  
        with col_z:
            st.info(f"📦 **Orders:** {customer_info['Total_Orders']}")
        
        # Communication options
        comm_col1, comm_col2, comm_col3 = st.columns(3)
        with comm_col1:
            if st.button("📞 Call Customer"):
                st.success(f"📞 Calling {customer_info['Phone']}")
        with comm_col2:
            if st.button("💬 Send SMS"):
                st.success(f"📱 SMS sent to {selected_customer}")
        with comm_col3:
            if st.button("✉️ Email"):
                st.success(f"📧 Email sent to {selected_customer}")
    
    with col2:
        st.markdown("### 📊 Customer Analytics")
        
        # Customer distribution by city
        city_dist = st.session_state.customers['City'].value_counts().reset_index()
        city_dist.columns = ['City', 'Customers']
        
        city_fig = px.bar(
            city_dist,
            x='City',
            y='Customers', 
            title='Customers by City',
            color='Customers',
            color_continuous_scale='Blues'
        )
        city_fig.update_layout(height=250)
        st.plotly_chart(city_fig, use_container_width=True)
        
        # Customer status distribution  
        status_dist = st.session_state.customers['Status'].value_counts().reset_index()
        status_dist.columns = ['Status', 'Count']
        
        status_fig = px.pie(
            status_dist,
            values='Count',
            names='Status',
            title='Customer Status Distribution'
        )
        status_fig.update_layout(height=250)
        st.plotly_chart(status_fig, use_container_width=True)
        
        st.markdown("### 🎯 Customer Insights")
        
        total_customers = len(st.session_state.customers)
        avg_orders = st.session_state.customers['Total_Orders'].mean()
        vip_customers = len(st.session_state.customers[st.session_state.customers['Status'] == 'VIP'])
        
        st.markdown(f"""
        <div class="enhanced-metric">
            <h3>{total_customers}</h3>
            <p>Total Customers</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="enhanced-metric">
            <h3>{avg_orders:.1f}</h3>
            <p>Avg Orders per Customer</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="enhanced-metric">
            <h3>{vip_customers}</h3>
            <p>VIP Customers</p>
        </div>
        """, unsafe_allow_html=True)

# Enhanced Footer with System Status
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 1rem;">
    <h3>🤖 Luxemart Supply Chain AI Agent</h3>
    <p><strong>Powered by Advanced Analytics & Machine Learning</strong></p>
    <p>📱 Mobile Business Automation | 🚚 Smart Logistics | 📊 Real-time Intelligence</p>
    <p>🎤 Voice Support | 👥 Customer Management | 🏢 Supplier Integration</p>
    <br>
    <p style="font-size: 12px;">
        ✅ System Status: <span style="color: green;">Online</span> | 
        🔄 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
        📊 Version: 2.0 Enhanced
    </p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh functionality with enhanced features
st.markdown("### 🔄 System Controls")
col_sys1, col_sys2, col_sys3, col_sys4 = st.columns(4)

with col_sys1:
    if st.button("🔄 Refresh All Data"):
        st.success("✅ All systems refreshed!")
        st.rerun()

with col_sys2:
    if st.button("🚨 System Health Check"):
        st.success("✅ All systems operational")
        st.balloons()

with col_sys3:
    if st.button("📊 Generate Report"):
        st.info("📋 System report generated")
        st.download_button(
            "Download Report",
            "Luxemart System Report - All systems operational",
            "luxemart_report.txt"
        )

with col_sys4:
    if st.button("🎯 Auto-Optimize"):
        st.success("🚀 System auto-optimization complete!")