import streamlit as st
import plotly.graph_objects as go
import numpy as np
import random
from src.engine import lla_to_ecef, generate_walker_delta
from src.network import SatelliteNetwork

st.set_page_config(page_title="Star-Linker Pro", layout="wide")

if 'broken_sats' not in st.session_state:
    st.session_state.broken_sats = []

# --- Sidebar UI ---
st.sidebar.title("🛠️ Mission Control")
weather = st.sidebar.selectbox("Atmospheric Status", ["Clear", "Cloudy", "Rainy", "Stormy"])

if st.sidebar.button("🐒 Release Chaos Monkey"):
    # Target 10% of satellites for failure
    all_sat_ids = [f"Sat_{i}" for i in range(300)] 
    st.session_state.broken_sats = random.sample(all_sat_ids, 30)

if st.sidebar.button("🔧 Reset Network"):
    st.session_state.broken_sats = []
    st.rerun()

st.sidebar.divider()
planes = st.sidebar.slider("Orbital Planes", 1, 15, 12)
sats_per_p = st.sidebar.slider("Sats per Plane", 1, 25, 20)
time_step = st.sidebar.slider("Time Offset", 0, 100, 0)

# --- Main App ---
CITY_DATA = {
    "New York": [40.71, -74.00], "Bengaluru": [12.97, 77.59], 
    "London": [51.50, -0.12], "Tokyo": [35.67, 139.65],
    "Sydney": [-33.86, 151.20], "Cape Town": [-33.92, 18.42]
}

col1, col2 = st.columns(2)
src = col1.selectbox("Source City", list(CITY_DATA.keys()), index=0)
dst = col2.selectbox("Destination City", list(CITY_DATA.keys()), index=1)

stations = {src: lla_to_ecef(*CITY_DATA[src], 0), dst: lla_to_ecef(*CITY_DATA[dst], 0)}
sats = generate_walker_delta(planes, sats_per_p, 550, time_step)

net = SatelliteNetwork()
net.update_topology(sats, stations, broken_nodes=st.session_state.broken_sats, weather=weather)
path = net.get_shortest_path(src, dst)

# --- 3D Visualization ---
fig = go.Figure()

# Earth
u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:15j]
xe, ye, ze = 6371*np.cos(u)*np.sin(v), 6371*np.sin(u)*np.sin(v), 6371*np.cos(v)
fig.add_trace(go.Surface(x=xe, y=ye, z=ze, opacity=0.1, showscale=False))

# Active Satellites
active_sats = {k: v for k, v in sats.items() if k not in st.session_state.broken_sats}
coords = np.array(list(active_sats.values()))
fig.add_trace(go.Scatter3d(x=coords[:,0], y=coords[:,1], z=coords[:,2], 
                           mode='markers', marker=dict(size=2, color='gray'), name="Sats"))

# SOURCE & DESTINATION NAMES
for name, pos in stations.items():
    fig.add_trace(go.Scatter3d(
        x=[pos[0]], y=[pos[1]], z=[pos[2]], 
        mode='markers+text', 
        text=[f"<b>{name}</b>"], 
        textposition="top center",
        marker=dict(size=12, color='orange'),
        name=name
    ))

# Routing Path
if path:
    p_coords = np.array([stations[n] if n in stations else sats[n] for n in path])
    fig.add_trace(go.Scatter3d(x=p_coords[:,0], y=p_coords[:,1], z=p_coords[:,2], 
                               mode='lines+markers', line=dict(color='cyan', width=6), name="Data Link"))
    st.success(f"Route Found! Atmospheric Latency Penalty: {weather}")
    st.markdown(" ➡️ ".join([f"**{n}**" for n in path]))
else:
    st.error("No Path Available. Satellite density too low or too many nodes offline.")

fig.update_layout(template="plotly_dark", height=800, scene=dict(aspectmode='data'))
st.plotly_chart(fig, use_container_width=True)