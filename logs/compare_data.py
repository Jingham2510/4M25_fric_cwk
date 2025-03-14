import matplotlib.pyplot as plt
from joint_data_logger import JointDataLogger  # Or wherever you defined read_data

def compare_robot_data(file_with, file_without):
    """
    Compares two datasets: one with friction/stiffness (file_with),
    one without friction/stiffness (file_without).
    Plots positions, velocities, and torques for each joint,
    showing how the data differs.
    """

    # 1. Load data from both CSV files
    data_with = JointDataLogger.read_data(file_with)
    data_without = JointDataLogger.read_data(file_without)

    # 2. Determine how many joints by inspecting the first record of each
    #    (Assuming both logs have the same number of joints)
    n_joints = len(data_with[0]["positions"])

    # 3. Convert each record to an index-based timescale
    #    or if you prefer, parse them as actual timestamps
    timesteps_with = range(len(data_with))
    timesteps_without = range(len(data_without))

    # ------------------------------
    # PLOT JOINT POSITIONS
    # ------------------------------
    plt.figure()
    for j in range(n_joints):
        # Extract position of joint j from both logs
        pos_with = [record["positions"][j] for record in data_with]
        pos_without = [record["positions"][j] for record in data_without]

        # Plot "with friction" log
        plt.plot(timesteps_with, pos_with, label=f"Pos_J{j}_with", linewidth=1)

        # Plot "no friction" log
        plt.plot(timesteps_without, pos_without, label=f"Pos_J{j}_noFric", linestyle="--", linewidth=1)

    plt.xlabel("Time Step")
    plt.ylabel("Position (rad)")
    plt.title("Joint Positions: With vs. Without Friction")
    plt.legend()
    plt.show()

    # ------------------------------
    # PLOT JOINT VELOCITIES
    # ------------------------------
    plt.figure()
    for j in range(n_joints):
        vel_with = [record["velocities"][j] for record in data_with]
        vel_without = [record["velocities"][j] for record in data_without]

        plt.plot(timesteps_with, vel_with, label=f"Vel_J{j}_with", linewidth=1)
        plt.plot(timesteps_without, vel_without, label=f"Vel_J{j}_noFric", linestyle="--", linewidth=1)

    plt.xlabel("Time Step")
    plt.ylabel("Velocity (rad/s)")
    plt.title("Joint Velocities: With vs. Without Friction")
    plt.legend()
    plt.show()

    # ------------------------------
    # PLOT JOINT TORQUES
    # ------------------------------
    plt.figure()
    for j in range(n_joints):
        torq_with = [record["torques"][j] for record in data_with]
        torq_without = [record["torques"][j] for record in data_without]

        plt.plot(timesteps_with, torq_with, label=f"Torq_J{j}_with", linewidth=1)
        plt.plot(timesteps_without, torq_without, label=f"Torq_J{j}_noFric", linestyle="--", linewidth=1)

    plt.xlabel("Time Step")
    plt.ylabel("Torque (Nm)")
    plt.title("Joint Torques: With vs. Without Friction")
    #plt.legend()
    plt.show()


compare_robot_data("logs/robot_data.csv", "logs/robot_data_noblock.csv")
