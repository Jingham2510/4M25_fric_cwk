import pybullet as p
import os 


"""
Controls the robot URDF model of the ABB IRB6400
-In our theoretical model, this is the low level controller that performs and records
"""
class RobController():

    def __init__(self, phys_client):
        

        self.p = phys_client

        #Create a copy of the robot at the origin
        self.rob = p.loadURDF(os.getcwd() + "\models\IRB_6400.urdf")

        #-1 because the end-effector doesn't count as a joint
        self.num_jnts = p.getNumJoints(self.rob) - 1 

        #Sets the max forces
        self.max_forces = [100, 100, 1000, 100, 100, 100]

        #Set the control mode (curr - position controller)
        p.setJointMotorControlArray(self.rob, [i for i in range(self.num_jnts)], p.POSITION_CONTROL)


        #Set the end-effector to measure the forces applied to it
        p.enableJointForceTorqueSensor(self.rob, self.num_jnts)


        print("----ROBOT SPAWNED----")

        return

    #Updates the robots position for a given array of floats
    def set_jnt_angles(self, jnt_angles, forces):
        
        #Check their are the correct number of joint angles
        if(len(jnt_angles) != self.num_jnts or len(forces) != self.num_jnts):
            print("Incorrect number of joint angles/forces!")
            return
        
        p.setJointMotorControlArray(self.rob, [i for i in range(self.num_jnts)], p.POSITION_CONTROL, targetPositions = jnt_angles, forces=forces)

        return
    

    #Set the end-effector to a given xyz position
    def set_end_pos(self, xyz):

        ori = [0, 0 , 0, 1]

        jnt_angs = p.calculateInverseKinematics(self.rob, self.num_jnts, xyz, ori)


        self.set_jnt_angles(jnt_angs, self.max_forces)

        return
        
        
    #Gets each joint applied torque
    def get_joint_torques(self):

        jnt_torques = []

        #Cycles through each joint and gets the state
        for i in range(self.num_jnts):
            pos, vel, reac, torq = p.getJointState(self.rob, i)
            jnt_torques.append(torq)

        return jnt_torques

    #Gets the force applied on the end-effector
    def get_end_force(self):
        
        pos, vel, reac, torq = p.getJointState(self.rob, self.num_jnts)

        return reac