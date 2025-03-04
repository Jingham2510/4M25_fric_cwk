"""
A simple file that contains the associated data/plotting functions
"""
import matplotlib.pyplot as plt
import datetime
import os 


def plot_torques(filename):


    #Time data
    timestep = []

    #Torque Data
    m1_trq = []
    m2_trq = []
    m3_trq = []
    m4_trq = []
    m5_trq = []
    m6_trq = []


    #Open the file
    with open(filename) as f:

        #First line pass flag
        FIRST_LINE_PASS = True
    
        #Save the first timestep as 0

        

        for line in f:

            if(FIRST_LINE_PASS):
                FIRST_LINE_PASS = False
                continue

            #Extract the line info
            curr_line = line.split(",")
        
            #Format the timestep
            curr_line_time = datetime.datetime.strptime(curr_line[0], "%H:%M:%S.%f")

            #Save the first time as the original time
            if len(timestep) == 0:
                timestep.append(0)
                first_time = curr_line_time

            else:
                #Calculate time passed since original time
                timestep.append((curr_line_time - first_time).total_seconds())


                       

            #Extract the torque info
            m1_trq.append(float(curr_line[1]))
            m2_trq.append(float(curr_line[2]))
            m3_trq.append(float(curr_line[3]))
            m4_trq.append(float(curr_line[4]))
            m5_trq.append(float(curr_line[5]))
            m6_trq.append(float(curr_line[6]))


    #Create a plot contianing 6 seperate subplots
    fig, axs = plt.subplots(3, 2)

    axs[0,0].plot(timestep, m1_trq)
    axs[0,0].set_title("Motor 1 Torque")

    axs[0,1].plot(timestep, m2_trq)
    axs[0,1].set_title("Motor 2 Torque")

    axs[1,0].plot(timestep, m3_trq)
    axs[1,0].set_title("Motor 3 Torque")

    axs[1,1].plot(timestep, m4_trq)
    axs[1,1].set_title("Motor 4 Torque")

    axs[2,0].plot(timestep, m5_trq)
    axs[2,0].set_title("Motor 5 Torque")

    axs[2,1].plot(timestep, m6_trq)
    axs[2,1].set_title("Motor 6 Torque")

    #Set axs labels
    for ax in axs.flat:
        ax.set(xlabel="Time(s)", ylabel="Torque(Nm)")


    #Set layout type
    fig.tight_layout()


    plt.show()




    return




if __name__ == "__main__":
    print("PLOTTING")
    plot_torques(os.getcwd() + "/data/test.txt")