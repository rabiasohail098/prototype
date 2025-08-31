
# Luxemart — Supply Chain Optimization Agent (Streamlit Prototype)

A simple end‑to‑end prototype that demonstrates:
- Daily report (low stock, city-wise orders, shipment risks)
- Auto‑reorder to best supplier (lead time + MOQ rules)
- Order processing workflow (confirm → ship → tracking)
- Logistics: generate courier labels (CSV) and view inbound shipments
- Inventory suggestions (warehouse relocation)
- Alerts center (incident messaging)
- Day-in-the-life simulator

## Run locally
1) Install Python 3.10+ and then:
```bash
pip install streamlit pandas numpy
```
2) Start the app:
```bash
streamlit run app.py
```
3) Data lives in `data/` (CSV + JSON). Edit freely; app hot‑reloads.

## Files
- `app.py` — the Streamlit app
- `data/products.csv`, `data/suppliers.csv`, `data/warehouses.csv`, `data/orders.csv`, `data/shipments.csv`
- `data/settings.json`
