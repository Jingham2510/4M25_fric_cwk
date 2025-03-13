import os
import pybullet_data
import pybullet as p
import time
import rob_controller_impedance as controller
#import rob_controller_inversekinematics as controller
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
        lateralFriction=0.9,         # Friction when sliding
        spinningFriction=0.2,        # Friction for rotation around the contact normal
        rollingFriction=0.1,         # Friction for rolling behavior
        contactStiffness=5000,        # Spring-like stiffness of the robot's link
        contactDamping=0.1,          # Damping to reduce bounce
        frictionAnchor=True          # Keeps the friction force stable
    )
    rob_cntrl = controller.RobController(physicsClient, robot_id)

    block_position = [2, 0, 0] 
    block_id = p.loadURDF(os.path.join("models", "block.urdf"), block_position, useFixedBase=True)
    p.changeDynamics(
        bodyUniqueId=block_id,
        linkIndex=-1,                  # -1 for the base link of the block
        lateralFriction=0.8,           # Sliding friction coefficient
        spinningFriction=0.2,          # Friction against in-place rotation
        rollingFriction=0.1,           # Friction against rolling
        restitution=0.1,               # Bounciness of the block (elasticity)
        frictionAnchor=True,           # Keeps friction stable
        contactStiffness=1000,         # Spring stiffness (N/m)
        contactDamping=0.1             # Damping to reduce oscillations
    )

    
    tq_rec = torque_recorder.TorqueRecorder(f"{os.getcwd()}/data/test.txt", rob_cntrl)

    for step in range(5000):  # 240 steps for 1 second of simulation
        p.stepSimulation()
        time.sleep(1/240)  # Match the real-time simulation speed
        tq_rec.measure_torque()
        if step < 1000:
            rob_cntrl.set_end_pos([1, 0, 1]) 
        elif step < 2000:
            rob_cntrl.set_end_pos([1, 0, 0.1])
        else:
            rob_cntrl.set_end_pos([1, 0.5, 0.1])

    tq_rec.save_torque_info()    
    p.disconnect()

if __name__ == "__main__":
    main()