import pybullet as p
import time
import pybullet_data
import os
physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0,0,-10)


#Create visual friction plane - representation of where the plane is 
fric_plane = p.loadURDF(os.getcwd() + "\models\plane.urdf")




#set the center of mass frame (loadURDF sets base link frame) startPos/Ornp.resetBasePositionAndOrientation(boxId, startPos, startOrientation)
for i in range (10000):
    p.stepSimulation()
    time.sleep(1./240.)

p.disconnect()
