import os
import pybullet_data
import pybullet as p
import time
#import rob_controller_impedance as controller
import rob_controller_inversekinematics as controller
import torque_recorder

def main():

    physicsClient = p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.8)

    plane_id = p.loadURDF("plane.urdf")

    robot_position = [0,0,0]
    robot_id = p.loadURDF(os.path.join("models", "IRB_6400.urdf"), robot_position, useFixedBase=True)
    p.changeDynamics(
        bodyUniqueId=robot_id,
        linkIndex=6,                 # This is the "end-effecter" link
        lateralFriction=0.6,         # Friction when sliding
        spinningFriction=0.2,        # Friction for rotation around the contact normal
        rollingFriction=0.1,         # Friction for rolling behavior
        contactStiffness=500,        # Spring-like stiffness of the robot's link
        contactDamping=0.1,          # Damping to reduce bounce
        frictionAnchor=False          # Keeps the friction force stable
    )
    rob_cntrl = controller.RobController(physicsClient, robot_id)

    block_position = [2, 0, 0] 
    block_id = p.loadURDF(os.path.join("models", "block.urdf"), block_position, useFixedBase=True)
    p.changeDynamics(
        bodyUniqueId=block_id,
        linkIndex=-1,                  # -1 for the base link of the block
        lateralFriction=0.5,           # Sliding friction coefficient
        spinningFriction=0.2,          # Friction against in-place rotation
        rollingFriction=0.1,           # Friction against rolling
        restitution=0.1,               # Bounciness of the block (elasticity)
        frictionAnchor=False,           # Keeps friction stable
        contactStiffness=500,         # Spring stiffness (N/m)
        contactDamping=0.1             # Damping to reduce oscillations
    )

    
    tq_rec = torque_recorder.TorqueRecorder(f"{os.getcwd()}/data/test.txt", rob_cntrl)

    for step in range(1500):  # 240 steps for 1 second of simulation
        p.stepSimulation()
        time.sleep(1/240)  # Match the real-time simulation speed
        tq_rec.measure_torque()
        if step < 500:
            rob_cntrl.set_end_pos([2, 0, 0.5]) 
        elif step < 1000:
            rob_cntrl.set_end_pos([2, 0, 0.2 + 0.02])
        else:
            rob_cntrl.set_end_pos([2, 0.75, 0.2 + 0.02])

    tq_rec.save_torque_info()    
    p.disconnect()

if __name__ == "__main__":
    main()