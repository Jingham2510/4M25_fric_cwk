import csv
import matplotlib.pyplot as plt
import numpy as np

# We'll assume the CSV columns include:
# step, ..., F_ee_x, F_ee_y, F_ee_z

csv_filename = "external_force.csv"

# 1) Read the data from CSV
time_steps = []
fx_data = []
fy_data = []
fz_data = []

with open(csv_filename, "r", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)  # read the header row

    # Find column indices for step, F_ee_x, F_ee_y, F_ee_z
    step_idx = header.index("step")
    fx_idx = header.index("F_ee_x")
    fy_idx = header.index("F_ee_y")
    fz_idx = header.index("F_ee_z")

    # Iterate through each row and parse values
    for row in reader:
        if not row:
            continue
        step_val = float(row[step_idx])
        fx_val = float(row[fx_idx])
        fy_val = float(row[fy_idx])
        fz_val = float(row[fz_idx])

        time_steps.append(step_val)
        fx_data.append(fx_val)
        fy_data.append(fy_val)
        fz_data.append(fz_val)

# 2) Plot F_ee_x, F_ee_y, F_ee_z vs time_steps

plt.figure()
plt.plot(time_steps, fx_data, label="F_ee_x")
plt.plot(time_steps, fy_data, label="F_ee_y")
plt.plot(time_steps, fz_data, label="F_ee_z")
plt.axhline(y=0, color='black', linestyle='--', linewidth=1)


plt.xlabel("Step")
plt.ylabel("End-Effector Force (N)")
plt.title("End-Effector Force vs. Time")
plt.legend()
plt.show()

# Compute the force magnitude at each time step
force_magnitude = np.sqrt(np.array(fx_data)**2 + np.array(fy_data)**2 + np.array(fz_data)**2)

# Create a new figure for force magnitude
plt.figure()
plt.plot(time_steps, force_magnitude, label="Force Magnitude", color="purple")

plt.axhline(y=0, color='black', linestyle='--', linewidth=1)  # Add reference line

plt.xlabel("Step")
plt.ylabel("Force Magnitude (N)")
plt.title("Force Magnitude vs. Time")
plt.legend()
plt.show()