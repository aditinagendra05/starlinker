# 🛰️ Star-Linker: LEO Mesh Network Simulator

Star-Linker is a Python-based digital twin of a Low Earth Orbit (LEO) satellite constellation. It simulates the orbital mechanics of a **Walker Delta** constellation and uses **Graph Theory (Dijkstra's Algorithm)** to calculate real-time data routing between global cities.

---

## 🚀 Why This Project Matters

In traditional satellite internet, data travels from Earth to a single satellite and back down. Star-Linker simulates the future of space-based internet: **Inter-Satellite Links (ISLs)**.

By using laser communication in the vacuum of space, data can travel **30% faster** than it does through terrestrial fiber-optic cables. This project visualizes how a "web" of moving satellites can provide high-speed, low-latency connectivity to any point on Earth.

---

## 🛠️ Installation & Setup

**1. Clone the project:**
```bash
mkdir star-linker
cd star-linker
```

**2. Install Dependencies:**
```bash
pip install numpy networkx plotly streamlit
```

**3. Run the Application:**
```bash
streamlit run app.py
```

---

## 🎮 How to Navigate the Simulator

Once the Streamlit dashboard opens, you will see a 3D Earth and a sidebar with several controls.

### 1. Route Settings
- **Start Point & End Point** — Select two global cities (e.g., London to Tokyo). The simulator will immediately attempt to find the shortest path of satellites to connect them.

### 2. Network Density (The "Grid" Controls)
- **Orbital Planes** — Think of these as the "lanes" or "hula hoops" circling the Earth.
  - *Why it matters:* Increasing planes provides better East-to-West coverage.
- **Sats per Plane** — The number of satellites in each individual lane.
  - *Why it matters:* Increasing this makes the "chain" stronger. If this is too low, satellites are too far apart to communicate, causing a **Constellation Gap**.

### 3. Motion Control
- **Time Step (Move Satellites)** — LEO satellites travel at roughly 7.5 km/s. Use this slider to advance time.
  - *What to watch for:* Notice how the "Data Path" (the green line) jumps from one satellite to another as they move out of range. This is called a **Handover**.

---

## 🧠 The Logic Behind the Simulation

### The "Physics" (Engine)

The satellites follow a **Walker Delta Constellation** geometry. We convert Latitude and Longitude into **ECEF (Earth-Centered, Earth-Fixed)** coordinates. This allows us to calculate the exact Euclidean distance between any two points in 3D space:

$$d = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2 + (z_2-z_1)^2}$$

### The "Mesh" (Graph Theory)

We use the **NetworkX** library to treat every satellite as a **Node**.

| Link Type | Condition |
|---|---|
| **ISL (Inter-Satellite Link)** | An edge is created if two satellites are within **2,000 km** of each other |
| **Ground Link** | An edge is created if a satellite is within **2,500 km** of a city |

### The "Routing" (Dijkstra's Algorithm)

The simulator runs **Dijkstra's Algorithm** every time you move a slider. It finds the path with the smallest cumulative distance — which in the vacuum of space also represents the **lowest latency path**.

---

## 📊 Reading the Results

| Element | Description |
|---|---|
| ⚪ White dots | Satellites |
| 🟠 Orange dots | Your selected cities |
| 🟢 Neon green line | Live data path |
| ⚠️ Success/Error box | Warns of a "Gap" if the constellation is too sparse |

The **Routing Table** below the map prints the exact hops taken:

```
New York ➡️ Sat_42 ➡️ Sat_18 ➡️ Bengaluru
```

---

## 📡 Performance Comparison: Space vs. Fiber

In the vacuum of space, light travels at its maximum speed ($c \approx 300{,}000$ km/s). In fiber-optic cables, light travels through glass with a refractive index of ~1.47, slowing it down by roughly 33%.

| Metric | Undersea Fiber Cable | LEO Satellite Mesh | Winner |
|---|---|---|---|
| **Signal Speed** | ~204,000 km/s | ~300,000 km/s | 🛰️ LEO (47% Faster) |
| **Propagation Medium** | Glass Core | Vacuum / Free Space | 🛰️ LEO |
| **Path Efficiency** | Fixed by cable geography | Dynamic Shortest Path | 🛰️ LEO |
| **Theoretical Latency** | ~4.9 ms per 1,000 km | ~3.3 ms per 1,000 km | 🛰️ LEO |

---

## 📂 Project Structure

```
star-linker/
├── app.py          # Main UI and visualization layer
└── src/
    ├── engine.py   # 3D math and orbital generation
    └── network.py  # Graph logic and pathfinding
```