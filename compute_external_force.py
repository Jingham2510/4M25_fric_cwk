import pybullet as p
import pybullet_data
import numpy as np
import csv
from logs.joint_data_logger import JointDataLogger

data_filename = "logs/sweep_fric/fric_0.95_stiff_1500_robot_data.csv"
urdf_path = "models/IRB_6400.urdf"
output_csv = "external_force.csv"

p.connect(p.DIRECT)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
robot_id = p.loadURDF(urdf_path, useFixedBase=True)
p.setGravity(0, 0, -9.8)

data_list = JointDataLogger.read_data(data_filename)
num_timesteps = len(data_list)
num_joints = len(data_list[0]["positions"])
link_ee_index = 6

results = []
for t in range(num_timesteps - 1):

    record_curr = data_list[t]
    record_next = data_list[t + 1]

    dt = 1.0/240 
    q  = record_curr["positions"]
    qd = record_curr["velocities"]
    tau_meas = record_curr["torques"]
    qd_next = record_next["velocities"]
    qdd = []
    for j in range(num_joints):
        qdd.append((qd_next[j] - qd[j]) / dt)

    tau_no_contact = p.calculateInverseDynamics(
        bodyUniqueId=robot_id,
        objPositions=q,
        objVelocities=qd,
        objAccelerations=qdd
    )

    tau_ext = []
    for j in range(num_joints):
        tau_ext.append( - tau_meas[j] + tau_no_contact[j])

    lin_jac, ang_jac = p.calculateJacobian(
        bodyUniqueId=robot_id,
        linkIndex=link_ee_index,
        localPosition=[0,0,0],
        objPositions=q,
        objVelocities=[0.0]*num_joints,
        objAccelerations=[0.0]*num_joints
    )
    # Convert lin_jac => np.array of shape (3, num_joints)
    J_lin = np.array(lin_jac)

    tau_ext_vec = np.array(tau_ext)   # shape (num_joints,)

    # F_ee = (J_lin^T)^{-1} * tau_ext
    # or more robustly use np.linalg.lstsq(J_lin.T, tau_ext_vec, rcond=None)
    # Typically (3 x n) with n >= 3 => we do least-squares if n > 3
    # or direct invert if n==3
    if J_lin.shape[1] == 3:
        # direct invert
        F_ee = np.linalg.inv(J_lin.T) @ tau_ext_vec
    else:
        # nJoints > 3 => do least squares
        F_ee, residuals, rank, s = np.linalg.lstsq(J_lin.T, tau_ext_vec, rcond=None)


    results.append({
        "step": t,
        "positions": q,
        "velocities": qd,
        "accelerations": qdd,
        "tau_measured": tau_meas,
        "tau_no_contact": tau_no_contact,
        "tau_external": tau_ext,
        "force_ee": F_ee.tolist()
        
    })



# Write out to CSV
with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    # header
    header = ["step"]
    for j in range(num_joints):
        header.append(f"pos_{j}")
    for j in range(num_joints):
        header.append(f"vel_{j}")
    for j in range(num_joints):
        header.append(f"acc_{j}")
    for j in range(num_joints):
        header.append(f"tau_meas_{j}")
    for j in range(num_joints):
        header.append(f"tau_no_contact_{j}")
    for j in range(num_joints):
        header.append(f"tau_ext_{j}")
    header += ["F_ee_x", "F_ee_y", "F_ee_z"]

    writer.writerow(header)

    # rows
    for rec in results:
        row = [rec["step"]]
        row.extend(rec["positions"])
        row.extend(rec["velocities"])
        row.extend(rec["accelerations"])
        row.extend(rec["tau_measured"])
        row.extend(rec["tau_no_contact"])
        row.extend(rec["tau_external"])
        row.extend(rec["force_ee"])  # 3 values
        writer.writerow(row)

print(f"External torque & force data saved to {output_csv}")
p.disconnect()