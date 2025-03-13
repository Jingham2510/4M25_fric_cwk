import pybullet as p
import numpy as np

class RobController:
    def __init__(self, phys_client, robot_id):
        self.p = phys_client
        self.rob = robot_id

        # Get number of joints (excluding end-effector)
        self.num_jnts = p.getNumJoints(self.rob) - 1  

        # End-effector index
        self.ee_index = self.num_jnts

        # Impedance control gains
        self.K = np.array([500, 500, 500])  # Stiffness (N/m)
        self.D = np.array([10, 10, 10])  # Damping (Ns/m)

        # Set all joints to torque control mode (they are free to move)
        for i in range(self.num_jnts):
            p.setJointMotorControl2(self.rob, i, controlMode=p.TORQUE_CONTROL, force=0)

        # Enable force/torque sensing on the end-effector
        p.enableJointForceTorqueSensor(self.rob, self.ee_index)

        print("---- ROBOT SPAWNED WITH TRUE END-EFFECTOR IMPEDANCE CONTROL ----")

    def set_end_pos(self, target_pos):
        """
        Implements impedance control for the end-effector.
        The controller applies forces at the end-effector as if it is connected to the target position
        via a virtual spring-damper system, while allowing all other joints to move freely.
        """
        # Get current end-effector position and velocity
        ee_state = p.getLinkState(self.rob, self.ee_index, computeLinkVelocity=True)
        current_pos = np.array(ee_state[0])  # Extract (x, y, z)
        current_vel = np.array(ee_state[6])  # Extract velocity (vx, vy, vz)

        # Compute spring-damper forces
        force_spring = -self.K * (current_pos - target_pos)
        force_damping = -self.D * current_vel
        control_force = force_spring + force_damping  # Total force applied

        # Apply the force only at the end-effector
        p.applyExternalForce(self.rob, self.ee_index, control_force.tolist(), current_pos.tolist(), p.WORLD_FRAME)

    def get_joint_torques(self):
        """
        Retrieves the torque applied at each joint.
        """
        torques = [p.getJointState(self.rob, i)[3] for i in range(self.num_jnts)]
        return torques

    def get_end_force(self):
        """
        Retrieves the force being applied to the end-effector.
        """
        return p.getJointState(self.rob, self.ee_index)[2]
    
    #Updates the robots position for a given array of floats
    def set_jnt_angles(self, jnt_angles, forces):
        
        #Check their are the correct number of joint angles
        if(len(jnt_angles) != self.num_jnts or len(forces) != self.num_jnts):
            print("Incorrect number of joint angles/forces!")
            return
        
        p.setJointMotorControlArray(self.rob, [i for i in range(self.num_jnts)], p.POSITION_CONTROL, targetPositions = jnt_angles, forces=forces)

        return
    

    #Uses Inverse Kinematics to set the robots end-effector position
    def IK_set_end_pos(self, xyz):

        ori = [0, 0 , 0, 1]

        jnt_angs = p.calculateInverseKinematics(self.rob, self.num_jnts, xyz, ori)


        self.set_jnt_angles(jnt_angs, self.max_forces)

        return
