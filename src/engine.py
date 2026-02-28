import numpy as np

def lla_to_ecef(lat, lon, alt_km):
    R = 6371.0
    rad_lat, rad_lon = np.radians(lat), np.radians(lon)
    x = (R + alt_km) * np.cos(rad_lat) * np.cos(rad_lon)
    y = (R + alt_km) * np.cos(rad_lat) * np.sin(rad_lon)
    z = (R + alt_km) * np.sin(rad_lat)
    return np.array([x, y, z])

def generate_walker_delta(num_planes, sats_per_plane, altitude_km, time_step=0):
    r = 6371.0 + altitude_km
    inc = np.radians(53) 
    sat_positions = {}
    sat_id = 0
    for p in range(num_planes):
        raan = 2 * np.pi * (p / num_planes)
        for s in range(sats_per_plane):
            mean_anomaly = 2 * np.pi * (s / sats_per_plane) + (time_step * 0.05)
            x_orb = r * np.cos(mean_anomaly)
            y_orb = r * np.sin(mean_anomaly)
            x = x_orb * np.cos(raan) - y_orb * np.sin(raan) * np.cos(inc)
            y = x_orb * np.sin(raan) + y_orb * np.cos(raan) * np.cos(inc)
            z = y_orb * np.sin(inc)
            sat_positions[f"Sat_{sat_id}"] = np.array([x, y, z])
            sat_id += 1
    return sat_positions