1.Fuzzy Logic Rules:
If the water level is low, the PSI is calculated as 1.5 times the water level.

If the water level is medium, the PSI increases faster, using a different multiplier.

If the water level is high, the PSI increases even more rapidly.

2. Membership Functions:
  Low Water Threshold (0-30%): The fuzzy system considers this as a "low" water state, activating the pump to fill the tank.
 
Medium Water Threshold (30-70%): This range is categorized as "medium," where PSI is moderately increased.

High Water Threshold (70-100%): As the water level approaches 100%, the system categorizes this as "high" and stops the pump to prevent overflow.

Implementation: In the code, these thresholds are directly used to simulate the fuzzy logic decisions through calculate_psi().

3. Simulation:
  Water Tank System: The simulation visually represents the water tank and allows user interaction with the "Open/Close Faucet" button.
 
Filling and Draining: The water level increases or decreases based on the user's interaction, while the PSI is continuously calculated and displayed in real-time.
 
Droplets Animation: Water droplets simulate the drainage when the faucet is opened, enhancing the realism of the simulation.
