import pybullet as p
import time
import pybullet_data
import os
import rob_controller


physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version


p.setGravity(0,0,-10)


#Create visual friction plane - representation of where the plane is 
fric_plane = p.loadURDF(os.getcwd() + "\models\plane.urdf", [0,0,0])

#Create the table that holds the material
table = p.loadURDF(os.getcwd() + "/models/table.urdf", [2,0,0.2])

#Create the robot and its associated controller
rob_cntrl = rob_controller.RobController(physicsClient)

desired_pos = [0, 0, 0, 0, 0, 0]
max_forces = [100, 100, 100, 100, 100, 100]

rob_cntrl.set_end_pos([1.9131330292961946, -0.01605496867055284, 0.43960405690302545])

#Steps through the simulation
for i in range (10000):
    p.stepSimulation()
    time.sleep(1./240.)

    pos = p.getLinkState(rob_cntrl.rob, 6)

    print(pos)

    
    if i > 1000:
        rob_cntrl.set_end_pos([1.9131330292961946, 0.35, 0.43960405690302545])

    
p.disconnect()
