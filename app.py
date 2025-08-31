
import streamlit as st
import pandas as pd
import numpy as np
import json, os, datetime as dt, random

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

@st.cache_data
def load_all():
    products = pd.read_csv(os.path.join(DATA_DIR,"products.csv"))
    suppliers = pd.read_csv(os.path.join(DATA_DIR,"suppliers.csv"))
    warehouses = pd.read_csv(os.path.join(DATA_DIR,"warehouses.csv"))
    orders = pd.read_csv(os.path.join(DATA_DIR,"orders.csv"))
    shipments = pd.read_csv(os.path.join(DATA_DIR,"shipments.csv"))
    with open(os.path.join(DATA_DIR,"settings.json")) as f:
        settings = json.load(f)
    return products, suppliers, warehouses, orders, shipments, settings

def save_df(df, name):
    path = os.path.join(DATA_DIR, f"{name}.csv")
    df.to_csv(path, index=False)

def courier_picker(city, couriers):
    # Simple rule: Karachi/Lahore -> TCS; otherwise randomly pick
    if city in ("Karachi","Lahore"):
        return "TCS"
    return random.choice(couriers)

def gen_tracking(courier):
    prefix = {"TCS":"TCS","Leopards":"LEO","BlueEx":"BEX"}.get(courier, "CN")
    return f"{prefix}-{random.randint(10000,99999)}"

def daily_report(products, orders, shipments):
    low_stock = products[products["stock"] <= products["reorder_point"]][["sku","name","stock"]]
    city_counts = orders.groupby("city").size().sort_values(ascending=False).to_dict()
    delays = [s for i,s in shipments.iterrows() if "delay" in s["status"].lower()]
    return low_stock, city_counts, delays

def auto_reorder(products, suppliers, settings, log):
    actions = []
    if not settings.get("auto_reorder", True):
        return actions
    for i,row in products.iterrows():
        if row["stock"] <= row["reorder_point"]:
            sup = suppliers[suppliers["supplier_id"]==row["supplier_id"]].iloc[0]
            qty = max(row["reorder_qty"], sup["min_order_qty"])
            eta = (dt.date.today() + dt.timedelta(days=int(sup["lead_time_days"]))).isoformat()
            actions.append({
                "sku":row["sku"],
                "name":row["name"],
                "supplier":sup["name"],
                "qty":int(qty),
                "eta":eta
            })
            log.append(f'Auto-Order: {row["name"]} -> {sup["name"]} for {qty} units. ETA {eta}')
    return actions

def process_pending_orders(orders, products, settings, log):
    for i,row in orders[orders["status"]=="Pending"].iterrows():
        sku = row["sku"]
        qty = row["qty"]
        pidx = products[products["sku"]==sku].index
        if len(pidx)==0:
            log.append(f"Order {row['order_id']}: SKU {sku} not found")
            continue
        if products.loc[pidx, "stock"].iloc[0] >= qty:
            products.loc[pidx, "stock"] = products.loc[pidx, "stock"] - qty
            courier = courier_picker(row["city"], settings["couriers"])
            orders.loc[i,"courier"] = courier
            orders.loc[i,"tracking"] = gen_tracking(courier)
            orders.loc[i,"status"] = "Shipped"
            log.append(f"Order {row['order_id']} shipped via {courier} [{orders.loc[i,'tracking']}]")
        else:
            orders.loc[i,"status"] = "Backorder"
            log.append(f"Order {row['order_id']} backordered (insufficient stock)")
    return orders, products

def relocation_suggestion(products):
    # Move stock to the city with higher demand: infer via avg_daily_sales by warehouse
    pivot = products.groupby("warehouse")["avg_daily_sales"].sum().sort_values(ascending=False)
    if len(pivot)<2: 
        return None
    top, bottom = pivot.index[0], pivot.index[-1]
    # Suggest moving the highest-selling SKU from bottom to top
    bottom_skus = products[products["warehouse"]==bottom].sort_values("avg_daily_sales", ascending=False)
    if not bottom_skus.empty:
        row = bottom_skus.iloc[0]
        qty_to_move = max(1, int(row["stock"]*0.3))
        if qty_to_move>0:
            return {"sku": row["sku"], "name":row["name"], "from":bottom, "to":top, "qty":qty_to_move}
    return None

st.set_page_config(page_title="Luxemart AI Agent", page_icon="📦", layout="wide")
st.title("📦 Luxemart — Supply Chain Optimization Agent (Prototype)")

products, suppliers, warehouses, orders, shipments, settings = load_all()

with st.sidebar:
    st.header("Navigation")
    page = st.radio("Go to", ["Dashboard","Inventory","Orders","Suppliers","Logistics","Alerts","Simulator"])
    st.markdown("---")
    st.subheader("Settings")
    settings["auto_reorder"] = st.toggle("Auto Reorder", value=settings.get("auto_reorder", True))
    settings["sla_days"] = st.number_input("SLA (days)", min_value=1, max_value=10, value=settings.get("sla_days",3))
    settings["risk_regions"] = st.text_input("Risk Regions (comma)", value=",".join(settings.get("risk_regions",[]))).split(",")
    if st.button("Save Settings"):
        with open(os.path.join(DATA_DIR,"settings.json"),"w") as f:
            json.dump(settings, f, indent=2)
        st.success("Settings saved")

if page=="Dashboard":
    st.subheader("Daily Briefing — 9:00 AM")
    low_stock, city_counts, delays = daily_report(products, orders, shipments)
    cols = st.columns(3)
    with cols[0]:
        st.metric("Products low in stock", len(low_stock))
        st.dataframe(low_stock, use_container_width=True)
    with cols[1]:
        st.metric("Cities with orders", len(city_counts))
        st.write(pd.DataFrame([{"city":k,"orders":v} for k,v in city_counts.items()]))
    with cols[2]:
        st.metric("Shipments at risk", len(delays))
        if delays:
            st.write(pd.DataFrame(delays))
    st.markdown("**AI Note:** Lahore orders > Karachi? Adjust courier capacity accordingly.")
    st.caption("This report is auto-generated each morning.")

elif page=="Inventory":
    st.subheader("Inventory Overview")
    st.dataframe(products, use_container_width=True)
    st.markdown("### AI Suggestions")
    suggestion = relocation_suggestion(products)
    if suggestion:
        st.info(f"Move **{suggestion['qty']}x {suggestion['name']}** ({suggestion['sku']}) from **{suggestion['from']}** to **{suggestion['to']}** — demand is higher there.")
    # Manual adjustments
    st.markdown("### Manual Stock Update")
    sku = st.selectbox("SKU", products["sku"])
    delta = st.number_input("Adjust stock by (can be negative)", -1000, 1000, 0)
    if st.button("Apply Adjustment"):
        idx = products[products["sku"]==sku].index[0]
        products.loc[idx,"stock"] = max(0, products.loc[idx,"stock"] + delta)
        save_df(products, "products")
        st.success("Stock updated")

elif page=="Orders":
    st.subheader("Orders")
    st.dataframe(orders, use_container_width=True)
    st.markdown("### Process Pending Orders")
    log = []
    if st.button("Run Processing"):
        orders2, products2 = process_pending_orders(orders.copy(), products.copy(), settings, log)
        save_df(orders2, "orders")
        save_df(products2, "products")
        st.success("Processing complete")
        st.code("\n".join(log) if log else "No actions.")

elif page=="Suppliers":
    st.subheader("Suppliers")
    st.dataframe(suppliers, use_container_width=True)
    st.markdown("### Auto Reorder Check")
    log = []
    actions = auto_reorder(products, suppliers, settings, log)
    if st.button("Trigger Auto Reorder Now"):
        if actions:
            # Register as inbound shipments
            sh = pd.read_csv(os.path.join(DATA_DIR,"shipments.csv"))
            for a in actions:
                sh.loc[len(sh)] = {
                    "shipment_id": f"SHP-{random.randint(1000,9999)}",
                    "supplier_id": suppliers[suppliers['name']==a['supplier']]['supplier_id'].iloc[0],
                    "eta": a['eta'],
                    "status": "Ordered",
                    "sku": a['sku'],
                    "qty": a['qty']
                }
            sh.to_csv(os.path.join(DATA_DIR,"shipments.csv"), index=False)
            st.success(f"{len(actions)} auto-orders placed.")
        else:
            st.info("No items met the auto-reorder criteria.")
    if actions:
        st.write(pd.DataFrame(actions))

elif page=="Logistics":
    st.subheader("Shipments & Couriers")
    st.dataframe(shipments, use_container_width=True)
    st.markdown("### Create Courier Labels for Shipped Orders")
    shipped = orders[orders["status"]=="Shipped"][["order_id","city","courier","tracking","sku","qty"]]
    if not shipped.empty:
        st.download_button("Download Shipping Labels (CSV)", shipped.to_csv(index=False).encode(), file_name="labels.csv")
    else:
        st.info("No shipped orders yet.")

elif page=="Alerts":
    st.subheader("Risk & Incident Center")
    st.warning("⚠️ Hyderabad deliveries facing delays due to floods. Auto-rescheduling enabled.")
    affected = orders[orders["city"]=="Hyderabad"]
    st.write("Affected Orders:", affected if not affected.empty else "None")
    st.markdown("### Customer Notifications")
    template = "Dear Customer, due to weather conditions, your order is rescheduled and will arrive in 3 days. — Luxemart"
    st.text_area("Message Preview", template, height=80)
    st.button("Send Notifications (Simulated)")

elif page=="Simulator":
    st.subheader("Ek Din Luxemart ke AI Agent ke Saath")
    steps = [
        ("9:00 AM", "Daily Report bheji gayi: low stock items, city-wise orders, and shipment risks."),
        ("10:00 AM", "Auto Reorder Trigger: low SKUs reordered to best supplier with ETA."),
        ("11:30 AM", "Order Processing: confirm, invoice, pack, courier pickup, customer SMS."),
        ("2:00 PM", "Dashboard Update: Days-of-Stock and relocation suggestion."),
        ("4:00 PM", "Strategic Alert: Realme demand spike — propose adding Realme C51."),
        ("6:00 PM", "Emergency Alert: Hyderabad delay — customers informed & routes rescheduled."),
        ("9:00 PM", "End-of-Day Summary: orders processed, suppliers contacted, delays handled, top product.")
    ]
    st.timeline = getattr(st, "timeline", None)
    for t,msg in steps:
        st.markdown(f"**{t}** — {msg}")
    st.markdown("---")
    st.markdown("**End-of-Day Summary (Generated)**")
    total_orders = len(pd.read_csv(os.path.join(DATA_DIR,"orders.csv")))
    st.write({
        "orders_processed": total_orders,
        "suppliers_contacted": 2,
        "delays_handled": 1,
        "top_product": "Infinix Fast Cable",
        "suggestions": [
            "Add Realme category",
            "Put Samsung M20 cover on sale"
        ]
    })
