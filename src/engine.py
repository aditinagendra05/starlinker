import numpy as np

def lla_to_ecef(lat, lon, alt_km):
    """Converts Latitude, Longitude, Altitude to 3D Cartesian (x, y, z)."""
    R = 6371.0  # Earth radius in km
    rad_lat = np.radians(lat)
    rad_lon = np.radians(lon)
    
    x = (R + alt_km) * np.cos(rad_lat) * np.cos(rad_lon)
    y = (R + alt_km) * np.cos(rad_lat) * np.sin(rad_lon)
    z = (R + alt_km) * np.sin(rad_lat)
    
    return np.array([x, y, z])

def generate_walker_delta(num_planes, sats_per_plane, inclination_deg, altitude_km, time_step=0):
    """Generates x, y, z coordinates for a Walker Delta constellation."""
    earth_radius = 6371.0
    r = earth_radius + altitude_km
    inc = np.radians(inclination_deg)
    
    sat_positions = {}
    sat_id = 0
    
    for p in range(num_planes):
        raan = 2 * np.pi * (p / num_planes) # Twist of the plane
        for s in range(sats_per_plane):
            # Move satellites over time (approx 7.5km/s)
            time_offset = time_step * 0.05 
            mean_anomaly = 2 * np.pi * (s / sats_per_plane) + time_offset
            
            # Position in orbital plane
            x_orb = r * np.cos(mean_anomaly)
            y_orb = r * np.sin(mean_anomaly)
            
            # Rotate to ECEF 3D space
            x = x_orb * (np.cos(raan)) - y_orb * (np.sin(raan) * np.cos(inc))
            y = x_orb * (np.sin(raan)) + y_orb * (np.cos(raan) * np.cos(inc))
            z = y_orb * np.sin(inc)
            
            sat_positions[f"Sat_{sat_id}"] = np.array([x, y, z])
            sat_id += 1
            
    return sat_positions