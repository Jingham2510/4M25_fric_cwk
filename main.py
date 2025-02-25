import pybullet as p
import time
import pybullet_data
import os
import rob_controller


physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version


p.setGravity(0,0,-10)


#Create visual friction plane - representation of where the plane is 
fric_plane = p.loadURDF(os.getcwd() + "\models\plane.urdf", [0,0,0])

#Create the robot and its associated controller
rob_cntrl = rob_controller.RobController(physicsClient)

desired_pos = [3.14, 3.14, 3.14, 3.14, 3.14, 3.14]
max_forces = [100, 100, 100, 100, 100, 100]

#set the center of mass frame (loadURDF sets base link frame) startPos/Ornp.resetBasePositionAndOrientation(boxId, startPos, startOrientation)
for i in range (10000):
    p.stepSimulation()
    time.sleep(1./240.)

    desired_pos = [i/10000, 3.14, 3.14, 3.14, 3.14, 3.14]

    rob_cntrl.set_position(desired_pos, max_forces)


p.disconnect()
