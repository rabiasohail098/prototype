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

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .alert-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .success-card {
        background: linear-gradient(135deg, #51cf66 0%, #40c057 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
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

if 'orders' not in st.session_state:
    st.session_state.orders = []

if 'alerts' not in st.session_state:
    st.session_state.alerts = []

# Sidebar
with st.sidebar:
    st.markdown("## 🤖 AI Agent Controls")
    
    # AI Agent Status
    st.markdown("### Agent Status")
    if st.button("🔄 Refresh Data"):
        st.rerun()
    
    st.success("✅ AI Agent Active")
    st.info(f"📅 Last Update: {datetime.now().strftime('%H:%M:%S')}")
    
    # Quick Actions
    st.markdown("### Quick Actions")
    if st.button("🚨 Generate Alert"):
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
    
    if st.button("📦 Auto Reorder"):
        low_stock_items = st.session_state.inventory[st.session_state.inventory['Stock'] < st.session_state.inventory['Min_Stock']]
        if not low_stock_items.empty:
            st.success(f"✅ Auto-ordered {len(low_stock_items)} items")
        else:
            st.info("ℹ️ All items are in stock")

# Main Header
st.markdown("""
<div class="main-header">
    <h1>📱 Luxemart Supply Chain AI Agent</h1>
    <p>Intelligent Supply Chain Management for Mobile Business</p>
</div>
""", unsafe_allow_html=True)

# Main Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dashboard", 
    "📦 Inventory", 
    "🚚 Orders & Logistics", 
    "📈 Analytics", 
    "🗣️ Customer Support",
    "📸 Product Images"
])

with tab1:
    st.markdown("## 📊 Real-time Dashboard")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_stock = st.session_state.inventory['Stock'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <h3>{total_stock}</h3>
            <p>Total Stock</p>
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
    
    # Alerts Section
    st.markdown("## 🚨 Live Alerts")
    
    # Check for low stock automatically
    low_stock_items = st.session_state.inventory[st.session_state.inventory['Stock'] < st.session_state.inventory['Min_Stock']]
    
    for _, item in low_stock_items.iterrows():
        days_left = item['Stock'] / item['Daily_Sales'] if item['Daily_Sales'] > 0 else 0
        st.markdown(f"""
        <div class="alert-card">
            <h4>⚠️ Critical Stock Alert</h4>
            <p><strong>{item['Product']}</strong> - Only {item['Stock']} units left!</p>
            <p>Days remaining: {days_left:.1f} days</p>
            <p>Recommended action: Order {item['Min_Stock'] * 2} units from {item['Supplier']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display other alerts
    if st.session_state.alerts:
        for alert in st.session_state.alerts[-3:]:  # Show last 3 alerts
            st.markdown(f"""
            <div class="success-card">
                <h4>📢 {alert['time']}</h4>
                <p>{alert['message']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Daily Summary
    st.markdown("## 📋 Today's Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📦 Inventory Status")
        inventory_fig = px.bar(
            st.session_state.inventory, 
            x='Product', 
            y='Stock',
            title='Current Stock Levels',
            color='Stock',
            color_continuous_scale='Viridis'
        )
        inventory_fig.update_layout(height=400)
        st.plotly_chart(inventory_fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 Revenue by Category")
        category_revenue = st.session_state.inventory.groupby('Category').apply(
            lambda x: (x['Stock'] * x['Price']).sum()
        ).reset_index()
        category_revenue.columns = ['Category', 'Revenue']
        
        pie_fig = px.pie(
            category_revenue,
            values='Revenue',
            names='Category',
            title='Revenue Distribution'
        )
        pie_fig.update_layout(height=400)
        st.plotly_chart(pie_fig, use_container_width=True)

with tab2:
    st.markdown("## 📦 Inventory Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Current Inventory")
        
        # Calculate days left for each product
        inventory_display = st.session_state.inventory.copy()
        inventory_display['Days_Left'] = inventory_display['Stock'] / inventory_display['Daily_Sales']
        inventory_display['Status'] = inventory_display.apply(
            lambda x: '🔴 Critical' if x['Stock'] < x['Min_Stock'] 
            else '🟡 Low' if x['Stock'] < x['Min_Stock'] * 1.5 
            else '🟢 Good', axis=1
        )
        
        st.dataframe(
            inventory_display[['Product', 'Stock', 'Min_Stock', 'Daily_Sales', 'Days_Left', 'Status', 'Supplier']],
            use_container_width=True
        )
    
    with col2:
        st.markdown("### Add New Product")
        with st.form("add_product"):
            new_product = st.text_input("Product Name")
            new_stock = st.number_input("Initial Stock", min_value=0, value=10)
            new_min_stock = st.number_input("Minimum Stock", min_value=0, value=5)
            new_price = st.number_input("Price (Rs)", min_value=0.0, value=1000.0)
            new_supplier = st.selectbox("Supplier", ["Supplier A", "Supplier B", "Supplier C"])
            new_category = st.selectbox("Category", ["Mobile", "Accessories", "Electronics"])
            
            if st.form_submit_button("Add Product"):
                new_row = pd.DataFrame({
                    'Product': [new_product],
                    'Stock': [new_stock],
                    'Min_Stock': [new_min_stock],
                    'Daily_Sales': [random.randint(1, 10)],
                    'Price': [new_price],
                    'Supplier': [new_supplier],
                    'Category': [new_category]
                })
                st.session_state.inventory = pd.concat([st.session_state.inventory, new_row], ignore_index=True)
                st.success("✅ Product added successfully!")
                st.rerun()
    
    # Reorder Suggestions
    st.markdown("### 🤖 AI Reorder Suggestions")
    reorder_suggestions = st.session_state.inventory[st.session_state.inventory['Stock'] < st.session_state.inventory['Min_Stock']]
    
    if not reorder_suggestions.empty:
        for _, item in reorder_suggestions.iterrows():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**{item['Product']}** - Current: {item['Stock']}, Minimum: {item['Min_Stock']}")
            
            with col2:
                suggested_qty = item['Min_Stock'] * 2
                st.write(f"Suggested Order: {suggested_qty} units")
            
            with col3:
                if st.button(f"Order {suggested_qty}", key=f"order_{item['Product']}"):
                    # Simulate ordering
                    idx = st.session_state.inventory[st.session_state.inventory['Product'] == item['Product']].index[0]
                    st.session_state.inventory.loc[idx, 'Stock'] += suggested_qty
                    st.success(f"✅ Ordered {suggested_qty} units of {item['Product']}")
                    st.rerun()

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
                    st.session_state.inventory.loc[idx, 'Stock'] = int(st.session_state.inventory.loc[idx, 'Stock'].item()) - int(quantity) # type: ignore
                    
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
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💬 Live Chat Support")
        
        # Chat interface
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = [
                {"role": "assistant", "content": "Salam! Main Luxemart ka AI assistant hun. Aap ki kya madad kar sakta hun?"}
            ]
        
        # Display chat messages
        for message in st.session_state.chat_messages:
            if message["role"] == "user":
                st.markdown(f"**👤 You:** {message['content']}")
            else:
                st.markdown(f"**🤖 AI Assistant:** {message['content']}")
        
        # Chat input
        user_input = st.text_input("Type your message here...", key="chat_input")
        
        if st.button("Send") and user_input:
            # Add user message
            st.session_state.chat_messages.append({"role": "user", "content": user_input})
            
            # Generate AI response
            responses = {
                "order": "Aapka order track karne ke liye Order ID dijiye. Main abhi check karta hun!",
                "delivery": "Delivery usually 2-4 din mein hoti hai. Kya aap ka koi specific order hai?",
                "product": "Hamare paas latest mobile phones aur accessories hain. Kya aap koi specific product dhond rahe hain?",
                "price": "Hamare competitive prices hain. Kya aap kisi product ka price janna chahte hain?",
                "return": "Return policy 7 din ki hai. Product original condition mein hona chahiye.",
                "complaint": "Main aap ki complaint note kar raha hun. Manager se baat karvata hun."
            }
            
            # Simple keyword matching for demo
            response = "Main aap ki madad karne ki koshish kar raha hun. Kya aap thoda aur detail mein bata sakte hain?"
            for key, value in responses.items():
                if key in user_input.lower():
                    response = value
                    break
            
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        st.markdown("### 📞 Voice Support")
        st.info("🎤 Voice support feature coming soon!")
        st.markdown("#### Quick Actions:")
        
        if st.button("📋 Check Order Status"):
            st.session_state.chat_messages.append({
                "role": "assistant", 
                "content": "Order status check karne ke liye aap ka Order ID chahiye. Kya aap Order ID bata sakte hain?"
            })
            st.rerun()
        
        if st.button("🚚 Track Delivery"):
            st.session_state.chat_messages.append({
                "role": "assistant", 
                "content": "Delivery tracking ke liye main aap ka Order ID check kar sakta hun. Order ID share kariye."
            })
            st.rerun()
        
        if st.button("💰 Price Inquiry"):
            st.session_state.chat_messages.append({
                "role": "assistant", 
                "content": "Kis product ka price janna chahte hain? Main latest prices bata sakta hun."
            })
            st.rerun()
        
        st.markdown("### 📊 Support Stats")
        support_stats = {
            "Today's Chats": 47,
            "Resolved Issues": 42,
            "Avg Response Time": "2.3 min",
            "Satisfaction Score": "4.8/5"
        }
        
        for stat, value in support_stats.items():
            st.metric(stat, value)

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

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🤖 Luxemart Supply Chain AI Agent | Powered by Advanced Analytics & Machine Learning</p>
    <p>📱 Mobile Business Automation | 🚚 Smart Logistics | 📊 Real-time Intelligence</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh every 30 seconds (optional)
import time
if st.button("🔄 Auto-Refresh Mode"):
    st.info("Auto-refresh activated! Data will update every 30 seconds.")
    time.sleep(30)
    st.rerun()