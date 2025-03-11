import pybullet as p
import pybullet_data
import os

def setup_environment():

    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.8)

    plane_id = p.loadURDF("plane.urdf")

    robot_position = [0,0,0]
    robot_id = p.loadURDF(os.path.join("models", "IRB_6400.urdf"), robot_position, useFixedBase=True)
    apply_end_effecter_stiffness(robot_id)


    block_position = [2, 0, 0] 
    block_id = p.loadURDF(os.path.join("models", "block.urdf"), block_position, useFixedBase=True)
    apply_block_stiffness(block_id)

    return robot_id, block_id

def apply_block_stiffness(object_id):
    p.changeDynamics(
        bodyUniqueId=object_id,
        linkIndex=-1,                  # -1 for the base link of the block
        lateralFriction=0.8,           # Sliding friction coefficient
        spinningFriction=0.2,          # Friction against in-place rotation
        rollingFriction=0.1,           # Friction against rolling
        restitution=0.1,               # Bounciness of the block (elasticity)
        frictionAnchor=True,           # Keeps friction stable
        contactStiffness=1000,         # Spring stiffness (N/m)
        contactDamping=0.1             # Damping to reduce oscillations
    )

def apply_end_effecter_stiffness(object_id):
    p.changeDynamics(
    bodyUniqueId=object_id,
    linkIndex=6,                 # This is the "end-effecter" link
    lateralFriction=0.9,         # Friction when sliding
    spinningFriction=0.2,        # Friction for rotation around the contact normal
    rollingFriction=0.1,         # Friction for rolling behavior
    contactStiffness=500,        # Spring-like stiffness of the robot's link
    contactDamping=0.1,          # Damping to reduce bounce
    frictionAnchor=True          # Keeps the friction force stable
    )