import pybullet as p
import os

class RobotModel:
    def __init__(self, physics_client):
        self.p = physics_client

        # Load the robot URDF at the origin
        self.robot_id = p.loadURDF(os.path.join(os.getcwd(), "models", "IRB_6400.urdf"), useFixedBase=True)

        # Get number of joints (excluding end-effector)
        self.num_joints = p.getNumJoints(self.robot_id) - 1  

        # Enable force/torque sensing on the end-effector
        self.p.enableJointForceTorqueSensor(self.robot_id, self.num_joints)

        # Set friction and stiffness properties for the end-effector
        self.p.changeDynamics(
            bodyUniqueId=self.robot_id,
            linkIndex=self.num_joints,  # End-effector index
            lateralFriction=0.8,
            spinningFriction=0.3,
            rollingFriction=0.1,
            contactStiffness=1000,
            contactDamping=0.1
        )

        print("---- ROBOT MODEL LOADED ----")

    def get_robot_id(self):
        return self.robot_id

    def get_end_effector_index(self):
        return self.num_joints  # The last joint is the end-effector
