import csv
import os
import numpy as np
from scipy.signal import butter, filtfilt

# -------------- Configuration -------------- 
csv_filename = "logs/robot_data.csv"
new_csv_filename = "logs/robot_data_filtered.csv"
order = 2            # Order of the Butterworth filter
cutoff_hz = 10.0     # Cutoff frequency in Hz
sampling_rate = 240.0  # If your simulation logs data at 240 Hz
# -------------------------------------------

# Step 1: Read the CSV, parse the columns for torque
rows = []
header = None

with open(csv_filename, "r", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)  # e.g. ["time", "pos_0", "pos_1", ..., "vel_0", "vel_1", ..., "torq_0", "torq_1", ...]
    
    # Identify torque columns
    torque_col_indices = [i for i, h in enumerate(header) if "torq_" in h]
    
    # Read rows into memory
    for row in reader:
        if not row:
            continue
        rows.append(row)

# If there's no data, or no torque columns, we can exit
if not rows or not torque_col_indices:
    print("No data or no torque columns found. Exiting.")
    exit(0)

# Step 2: Convert torque columns to arrays for filtering
# We assume each torque_col is a single time series across all rows
num_timesteps = len(rows)
num_torques = len(torque_col_indices)

# Create a (num_timesteps x num_torques) array to store torque data
torque_data = np.zeros((num_timesteps, num_torques))

for t, row in enumerate(rows):
    for j, col_idx in enumerate(torque_col_indices):
        torque_data[t, j] = float(row[col_idx])

# Step 3: Design a Butterworth low-pass filter
nyquist = 0.5 * sampling_rate
normalized_cutoff = cutoff_hz / nyquist
b, a = butter(order, normalized_cutoff, btype='low', analog=False)

# Step 4: Apply the filter to each torque column
# We'll filter along the time axis for each joint
torque_data_filtered = np.zeros_like(torque_data)
for j in range(num_torques):
    # filtfilt for zero-phase filtering
    torque_data_filtered[:, j] = filtfilt(b, a, torque_data[:, j])

# Step 5: Overwrite the torque columns in memory with the filtered values
for t in range(num_timesteps):
    for j, col_idx in enumerate(torque_col_indices):
        rows[t][col_idx] = f"{torque_data_filtered[t, j]}"

with open(new_csv_filename, "w", newline="") as f_out:
    writer = csv.writer(f_out)
    writer.writerow(header)  # same header as before
    writer.writerows(rows)

print(f"Filtered torque data saved back to {csv_filename}.")
