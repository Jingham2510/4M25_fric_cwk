import pybullet as p
import os 


"""
Controls the robot URDF model of the ABB IRB6400
"""
class RobController():

    def __init__(self, phys_client):
        

        self.p = phys_client

        #Create a copy of the robot at the origin
        self.rob = p.loadURDF(os.getcwd() + "\models\IRB_6400.urdf")

        self.num_jnts = p.getNumJoints(self.rob)

        #Set the control mode (curr - position controller)
        p.setJointMotorControlArray(self.rob, [i for i in range(self.num_jnts)], p.POSITION_CONTROL)

        print("----ROBOT SPAWNED----")

        return
    


    #Updates the robots position for a given array of floats
    def set_position(self, jnt_angles, forces):
        
        #Check their are the correct number of joint angles
        if(len(jnt_angles) != self.num_jnts or len(forces) != self.num_jnts):
            print("Incorrect number of joint angles/forces!")
            return
        
        p.setJointMotorControlArray(self.rob, [i for i in range(self.num_jnts)], p.POSITION_CONTROL, targetPositions = jnt_angles, forces=forces)

        return
        

