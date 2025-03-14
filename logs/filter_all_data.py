import csv
import os
import numpy as np
from scipy.signal import butter, filtfilt

#########################################
# Configuration
#########################################
input_csv = "logs/robot_data.csv"
output_csv = "logs/robot_data_filtered.csv"

sampling_rate = 240.0   # e.g., 240 Hz
cutoff_hz = 10.0        # cutoff frequency in Hz
filter_order = 2        # Butterworth filter order

#########################################
# Step 1: Read the CSV, parse columns
#########################################
rows = []
header = None

with open(input_csv, "r", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)  # e.g. ["time", "pos_0", "pos_1", ..., "vel_0", ... "torq_0", ...]

    # Identify columns for positions, velocities, torques
    pos_indices = [i for i, h in enumerate(header) if "pos_"  in h]
    vel_indices = [i for i, h in enumerate(header) if "vel_"  in h]
    torq_indices= [i for i, h in enumerate(header) if "torq_" in h]

    # Read rows into memory
    for row in reader:
        if not row:
            continue
        rows.append(row)

if not rows:
    print("No data found in CSV, exiting.")
    exit(0)

num_timesteps = len(rows)

# If you want to keep 'time' or other text columns unaltered, that's fine. 
# We'll only filter numeric columns matching pos_, vel_, torq_.


#########################################
# Step 2: Convert columns to arrays
#########################################
def extract_column_data(rows, col_indices):
    """
    Returns a (num_timesteps x num_columns) array for the specified col_indices.
    """
    num_cols = len(col_indices)
    arr = np.zeros((num_timesteps, num_cols))
    for t, row in enumerate(rows):
        for j, c_idx in enumerate(col_indices):
            arr[t, j] = float(row[c_idx])
    return arr

pos_data  = extract_column_data(rows, pos_indices)
vel_data  = extract_column_data(rows, vel_indices)
torq_data = extract_column_data(rows, torq_indices)

#########################################
# Step 3: Design and apply Butterworth filter
#########################################
nyquist = 0.5 * sampling_rate
normalized_cutoff = cutoff_hz / nyquist
b, a = butter(filter_order, normalized_cutoff, btype='low', analog=False)

def filter_time_series(data_2d):
    """
    Applies filtfilt to each column of data_2d.
    data_2d: shape (num_timesteps, num_cols)
    returns the same shape with filtered data
    """
    data_filt = np.zeros_like(data_2d)
    for col_idx in range(data_2d.shape[1]):
        data_filt[:, col_idx] = filtfilt(b, a, data_2d[:, col_idx])
    return data_filt

pos_data_filt  = filter_time_series(pos_data)
vel_data_filt  = filter_time_series(vel_data)
torq_data_filt = filter_time_series(torq_data)

#########################################
# Step 4: Write results to a new CSV
#########################################
with open(output_csv, "w", newline="") as f_out:
    writer = csv.writer(f_out)
    writer.writerow(header)  # keep the same header

    for t in range(num_timesteps):
        row = rows[t].copy()  # start with original row to preserve other columns (time, etc.)

        # Overwrite pos_*, vel_*, torq_* columns with filtered data
        for j, c_idx in enumerate(pos_indices):
            row[c_idx] = f"{pos_data_filt[t, j]}"

        for j, c_idx in enumerate(vel_indices):
            row[c_idx] = f"{vel_data_filt[t, j]}"

        for j, c_idx in enumerate(torq_indices):
            row[c_idx] = f"{torq_data_filt[t, j]}"

        writer.writerow(row)

print(f"Filtered data saved to {output_csv}")
