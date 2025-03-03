import matplotlib.pyplot as plt
import datetime

#Basic object which records the torque measured in the joints of a given urdf model and saves it to a given filename
class TorqueRecorder():


    def __init__(self, filename, rob):

        self.filename = filename
        self.rob = rob

        #The times of the measurements
        self.times = []

        #The torques are saved as sublists for each motor
        # #i.e. [[motor_1 torques], [motor_2 torques]... [motor_n torques]] 
        self.torques = [[] for i in range(self.rob.num_jnts)]

        return


    #Take a measurement of the torques
    def measure_torque(self):

        curr_torques = self.rob.get_joint_torques()

    
        for jnt in range(self.rob.num_jnts):
            self.torques[jnt].append(curr_torques[jnt])
            self.times.append(datetime.datetime.now().time())

        return


    #Save all the torque info to the file
    def save_torque_info(self):

        #Open the file
        with open(self.filename, "w+") as f:

            f.write(f"{datetime.datetime.now()} - Joint Torques \n")


            #Write every torque to the file
            for i in range(len(self.torques[0])):

                #Write out the time
                f.write(str(self.times[i]))

                #Write every joint info
                for j in range(len(self.torques)):
                    f.write(f"{self.torques[j][i]},")

                #Go to the next line
                f.write("\n")



        return
