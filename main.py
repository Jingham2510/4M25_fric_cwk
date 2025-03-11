from simulation.setup_simulation import setup_environment
import pybullet as p
import time

def main():
    # Initialize the simulation environment
    robot_id, block_id = setup_environment()

    # Run the simulation loop (no control or movement yet)
    for step in range(480):  # 240 steps for 1 second of simulation
        p.stepSimulation()
        time.sleep(1/240)  # Match the real-time simulation speed

    # Disconnect from the simulation when done
    p.disconnect()

if __name__ == "__main__":
    main()
