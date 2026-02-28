import streamlit as st
import plotly.graph_objects as go
import numpy as np
from src.engine import lla_to_ecef, generate_walker_delta
from src.network import SatelliteNetwork

st.set_page_config(layout="wide")
st.title("🛰️ Star-Linker: Dynamic LEO Mesh Simulator")

# --- 1. Global City Data ---
CITY_DATA = {
    "New York (USA)": [40.7128, -74.0060],
    "Bengaluru (India)": [12.9716, 77.5946],
    "London (UK)": [51.5074, -0.1278],
    "Tokyo (Japan)": [35.6762, 139.6503],
    "Sydney (Australia)": [-33.8688, 151.2093],
    "Cape Town (South Africa)": [-33.9249, 18.4241]
}

# --- 2. Sidebar Controls ---
st.sidebar.header("Route Settings")
source_city = st.sidebar.selectbox("Start Point", list(CITY_DATA.keys()), index=0)
dest_city = st.sidebar.selectbox("End Point", list(CITY_DATA.keys()), index=1)

st.sidebar.divider()
st.sidebar.header("Network Density")
planes = st.sidebar.slider("Orbital Planes", 1, 15, 10)
sats_per_p = st.sidebar.slider("Sats per Plane", 1, 20, 15)
time_step = st.sidebar.slider("Move Satellites", 0, 100, 0)

# --- 3. Calculation ---
# Setup Stations
stations = {
    source_city: lla_to_ecef(CITY_DATA[source_city][0], CITY_DATA[source_city][1], 0),
    dest_city: lla_to_ecef(CITY_DATA[dest_city][0], CITY_DATA[dest_city][1], 0)
}

# Setup Constellation
sats = generate_walker_delta(planes, sats_per_p, 53, 550, time_step=time_step)

# Find Path
net = SatelliteNetwork(isl_threshold=2200, gs_threshold=2800)
net.update_topology(sats, stations)
path = net.get_shortest_path(source_city, dest_city)

# --- 4. Visualization ---
fig = go.Figure()

# Add Earth
u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:15j]
x_e, y_e, z_e = 6371*np.cos(u)*np.sin(v), 6371*np.sin(u)*np.sin(v), 6371*np.cos(v)
fig.add_trace(go.Surface(x=x_e, y=y_e, z=z_e, opacity=0.1, showscale=False))

# Add Satellites
sat_coords = np.array(list(sats.values()))
fig.add_trace(go.Scatter3d(x=sat_coords[:,0], y=sat_coords[:,1], z=sat_coords[:,2], 
                           mode='markers', marker=dict(size=2, color='white'), name="Sats"))

# Add Selected Cities
for name, pos in stations.items():
    fig.add_trace(go.Scatter3d(x=[pos[0]], y=[pos[1]], z=[pos[2]], 
                               mode='markers+text', text=[name], marker=dict(size=8, color='orange')))

# Draw Data Path and PRINT HOPS
if path:
    p_coords = np.array([stations[n] if n in stations else sats[n] for n in path])
    fig.add_trace(go.Scatter3d(x=p_coords[:,0], y=p_coords[:,1], z=p_coords[:,2], 
                               mode='lines+markers', line=dict(color='lime', width=6), name="Active Path"))
    
    st.success(f"✅ Connection Established via {len(path)-2} Hops")
    
    # --- PRINTING THE PATH BELOW ---
    st.subheader("📡 Network Routing Table")
    
    # Create a nice visual arrow path
    hop_string = " ➡️ ".join([f"**{node}**" for node in path])
    st.markdown(hop_string)
    
    # Detail View in a table
    with st.expander("See Detailed Node Data"):
        st.write("Each hop represents a laser link transfer:")
        for i, node in enumerate(path):
            node_type = "Ground Station" if node in stations else "LEO Satellite"
            st.text(f"Hop {i}: {node} ({node_type})")
else:
    st.error("❌ No Path Found. Increase satellite density to bridge the gap.")

fig.update_layout(template="plotly_dark", scene=dict(aspectmode='data'), height=600)
st.plotly_chart(fig, use_container_width=True)