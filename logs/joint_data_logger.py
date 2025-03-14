import datetime
import csv
import os
import pybullet as p

class JointDataLogger:
    """
    Logs time, joint positions, velocities, and torques for a given robot controller.
    Saves data to CSV, and can read it back later.
    """

    def __init__(self, filename, robot_controller):
        """
        :param filename: The path to the CSV file for saving data.
        :param robot_controller: The robot controller instance that provides:
               - num_jnts
               - get_joint_torques()
               - A method to get positions & velocities (or we can call p.getJointState() directly)
        """
        self.filename = filename
        self.rob = robot_controller

        # We'll store data in lists before writing out
        self.records = []  # Each element is a dict: {time, jnt_positions, jnt_velocities, jnt_torques}

        print(f"Data logger initialized. Will save to {self.filename}")

    def record_data(self):
        """
        Records the time, joint positions, velocities, and torques at the current moment.
        """
        # We'll use datetime timestamp or you can use sim step if you prefer
        current_time = datetime.datetime.now().time()  # or p.getRealTimeSimulation()

        jnt_positions, jnt_velocities = self.rob.get_joint_position_velocity()  # from your controller
        jnt_torques = self.rob.get_joint_torques()

        # Create a record
        record = {
            "time": current_time,
            "positions": jnt_positions,
            "velocities": jnt_velocities,
            "torques": jnt_torques
        }
        self.records.append(record)

    def save_data(self):
        """
        Saves all recorded data to a CSV file.
        Rows: time, pos0, pos1, ..., vel0, vel1, ..., torq0, torq1, ...
        """
        # Make sure directory exists
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        with open(self.filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            # Write header
            header = ["time"]
            # The number of joints
            n_joints = self.rob.num_jnts
            header += [f"pos_{i}" for i in range(n_joints)]
            header += [f"vel_{i}" for i in range(n_joints)]
            header += [f"torq_{i}" for i in range(n_joints)]
            writer.writerow(header)

            # Write each record
            for rec in self.records:
                row = []
                row.append(rec["time"])
                row.extend(rec["positions"])  # each joint position
                row.extend(rec["velocities"]) # each joint velocity
                row.extend(rec["torques"])    # each joint torque
                writer.writerow(row)

        print(f"Data saved to {self.filename}")

    @staticmethod
    def read_data(filename):
        """
        Reads previously saved CSV data from 'filename' and returns a list of records.
        Each record is a dict with: time, positions[], velocities[], torques[].
        """
        data = []
        with open(filename, "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # read the header

            # Identify how many joints by counting pos_, vel_, torq_ columns
            # but we can also parse them from the header
            # We'll do a simple approach: the number of columns minus 1 for time, then /3 for pos,vel,torq sets
            n_columns = len(header)
            # time col is 1, so the rest are positions, velocities, torques
            # We know num_joints = (n_columns - 1) // 3
            # But let's parse them more robustly:
            pos_indices = [i for i, h in enumerate(header) if "pos_" in h]
            vel_indices = [i for i, h in enumerate(header) if "vel_" in h]
            torq_indices = [i for i, h in enumerate(header) if "torq_" in h]

            for row in reader:
                if not row:
                    continue

                # time is row[0]
                rec_time = row[0]
                # gather positions
                rec_pos = [float(row[i]) for i in pos_indices]
                rec_vel = [float(row[i]) for i in vel_indices]
                rec_torq = [float(row[i]) for i in torq_indices]

                record_dict = {
                    "time": rec_time,
                    "positions": rec_pos,
                    "velocities": rec_vel,
                    "torques": rec_torq
                }
                data.append(record_dict)

        return data
