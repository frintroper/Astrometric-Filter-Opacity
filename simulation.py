import numpy as np

def run_orion_opacity_simulation(total_years=10, steps_per_year=12, j_initial=1.005):
    """
    Simulates the tracking divergence between standard ZFC astronomy
    and the background-independent TONE framework centered on the Orion Core.
    """
    dt = 1.0 / steps_per_year
    total_steps = total_years * steps_per_year
    time_axis = np.linspace(0, total_years, total_steps)
    
    # NEW INITIALIZATION: Absolute coordinates for M42 (Orion Nebula Core)
    # RA: 83.822 deg (05h 35m 17.3s), Dec: -5.391 deg (-05d 23m 28s)
    ra_base, dec_base = 83.822083, -5.391111
    
    # Allocation matrices
    zfc_ra, zfc_dec = np.zeros(total_steps), np.zeros(total_steps)
    tone_ra, tone_dec = np.zeros(total_steps), np.zeros(total_steps)
    
    j_state = j_initial
    truncation_debt_accumulator = 0.0
    
    print(f"Year | ZFC RA (deg) | ZFC Dec (deg) | TONE RA (deg) | TONE Dec (deg) | Divergence (deg)")
    print("-" * 90)
    
    for i in range(total_steps):
        t = time_axis[i]
        
        # 1. Classical ZFC Precession Model (20.04 arcseconds/year to deg/step)
        annual_precession_deg = 20.04 / 3600.0
        zfc_drift = t * annual_precession_deg
        zfc_ra[i] = ra_base + (zfc_drift * np.sin(np.radians(ra_base)))
        zfc_dec[i] = dec_base + (zfc_drift * np.cos(np.radians(ra_base)))
        
        # 2. Non-Local TONE Layer (Integrating the j = 1/j scale invariant)
        scale_divergence = j_state - (1.0 / j_state)
        jerk_core_acceleration = (t**3 / 6.0) * 0.0125
        truncation_debt_accumulator += (scale_divergence * dt * np.exp(t / 8.0))
        
        tone_ra[i] = zfc_ra[i] + (scale_divergence * t) + (jerk_core_acceleration * np.sin(t))
        tone_dec[i] = zfc_dec[i] + (truncation_debt_accumulator * 4.5) + (jerk_core_acceleration * np.cos(t))
        
        # Calculate metric divergence vector magnitude
        divergence = np.sqrt((tone_ra[i] - zfc_ra[i])**2 + (tone_dec[i] - zfc_dec[i])**2)
        
        # Modulate field scaling component
        j_state += 0.00025 * np.sin(2.0 * np.pi * t / 5.0)
        
        if i % (2 * steps_per_year) == 0 or i == total_steps - 1:
            print(f"{t:4.1f} | {zfc_ra[i]:12.4f} | {zfc_dec[i]:13.4f} | {tone_ra[i]:13.4f} | {tone_dec[i]:14.4f} | {divergence:15.4f}")

if __name__ == "__main__":
    run_orion_opacity_simulation()
