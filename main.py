import os
import pybullet_data
import pybullet as p
import time
#import rob_controller_impedance as controller
import rob_controller_inversekinematics as controller
import logs.joint_data_logger as joint_data_logger

def main(fric, stiffness, folder):

    print("RUN STARTED")

    physicsClient = p.connect(p.DIRECT)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.8)

    plane_id = p.loadURDF("plane.urdf")

    robot_position = [0,0,0]
    robot_id = p.loadURDF(os.path.join("models", "IRB_6400.urdf"), robot_position, useFixedBase=True)
    p.changeDynamics(
        bodyUniqueId=robot_id,
        linkIndex=6,                 # This is the "end-effecter" link
        lateralFriction=0.7,         # Friction when sliding
        spinningFriction=0.2,        # Friction for rotation around the contact normal
        rollingFriction=0.1,         # Friction for rolling behavior
        contactStiffness=1500,        # Spring-like stiffness of the robot's link
        contactDamping=0.1,          # Damping to reduce bounce
        frictionAnchor=False          # Keeps the friction force stable
    )
    rob_cntrl = controller.RobController(physicsClient, robot_id)

    block_position = [2, 0, 0] 
    block_id = p.loadURDF(os.path.join("models", "block.urdf"), block_position, useFixedBase=True)
    p.changeDynamics(
        bodyUniqueId=block_id,
        linkIndex=-1,                  # -1 for the base link of the block
        lateralFriction=fric,           # Sliding friction coefficient
        spinningFriction=0.2,          # Friction against in-place rotation
        rollingFriction=0.1,           # Friction against rolling
        restitution=0.1,               # Bounciness of the block (elasticity)
        frictionAnchor=False,           # Keeps friction stable
        contactStiffness=stiffness,         # Spring stiffness (N/m)
        contactDamping=0.1             # Damping to reduce oscillations
    )

    logger = joint_data_logger.JointDataLogger(f"{os.getcwd()}/logs/{folder}/fric_{fric}_stiff_{stiffness}_robot_data.csv", rob_cntrl)


    for step in range(1500):
        p.stepSimulation()
        time.sleep(1/240)  # Match the real-time simulation speed, 240 steps for 1 second of simulation

        if step < 500:
            rob_cntrl.set_end_pos([2, 0, 0.3]) 
        elif step < 1000:
            rob_cntrl.set_end_pos([2, 0, 0.2 + 0.02])
        else:
            rob_cntrl.set_end_pos([2, 1, 0.2 + 0.02])

        if step > 250:
            logger.record_data()

    logger.save_data()  
    p.disconnect()


    print("RUN COMPLETE")

if __name__ == "__main__":

    """
    The current test is one where the stiffness of the material is changed and the friction is held the same
    The idea being to test how our friciton estimation performs if the stiffness of the material changes
    """
    current_test = "sweep_fric"

    
    stiffness = 1500

    for i in range(20, 100, 5):

        main((i/100), stiffness, current_test)



    

