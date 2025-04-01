import matplotlib.pyplot as plt
from joint_data_logger import JointDataLogger  # Or wherever you defined read_data

def plot_robot_data(csv_filename):
    # 1. Load data from CSV
    loaded_data = JointDataLogger.read_data(csv_filename)
    
    # If you prefer a numeric timeline instead of the string time from CSV,
    # we can just treat each record index as a pseudo-time:
    time_steps = range(len(loaded_data))

    # 2. Determine how many joints from the first record
    n_joints = len(loaded_data[0]["positions"])

    # 3. Plot Joint Positions over Time
    plt.figure()
    for j in range(n_joints):
        # Gather position of joint j at each time step
        jnt_positions = [record["positions"][j] for record in loaded_data]
        plt.plot(time_steps, jnt_positions, label=f"Joint {j}")
    plt.xlabel("Time Step")
    plt.ylabel("Position (rad)")
    plt.legend()
    plt.show()

    # 4. Plot Joint Velocities over Time
    plt.figure()
    for j in range(n_joints):
        jnt_vels = [record["velocities"][j] for record in loaded_data]
        plt.plot(time_steps, jnt_vels, label=f"Joint {j}")
    plt.xlabel("Time Step")
    plt.ylabel("Velocity (rad/s)")
    plt.legend()
    plt.show()

    # 5. Plot Joint Torques over Time
    plt.figure()
    for j in range(n_joints):
        jnt_torques = [record["torques"][j] for record in loaded_data]
        plt.plot(time_steps, jnt_torques, label=f"Joint {j}")
    plt.title("Joint Torques")
    plt.xlabel("Time Step")
    plt.ylabel("Torque (Nm)")
    plt.legend()
    plt.show()


plot_robot_data("logs/robot_data_filtered.csv")
