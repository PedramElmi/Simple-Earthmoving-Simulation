# time module is only for knowing when this program ran. this will be at output-simulation-data.txt file
import time
# loader and truck class in written local module (you will find machine.py in current file path with main.py)
from machine import Loader, Truck
# a couple of functions for cleaner code! (you will find programtools.py in current file path with main.py)
from programtools import Time, write_csv, read_csv_truck_data

print("This program will read data from: input-truck-data.csv\n"
      "The program currently works with only one Loader (Queue is considered)\n"
      "Add as many as trucks you want in the input-truck-data.csv file\n"
      "Info for input-truck-data.csv:\n"
      "ID: Truck ID (combination of letters and numbers)\n"
      "last status: the last thing that the truck have done\n")

# Create the main simulation time and branch simulation time
branch = Time("branch")
simulation = Time("simulation")

# read "input-truck-data.csv" truck's data
truck_data = read_csv_truck_data("input-truck-data.csv")

# creating truck's instances and putting them inside of a list
truck_list = []
for info in truck_data:
    truck = Truck(
        truck_id=info[0],
        loading_dur=info[1],
        hauling_dur=info[2],
        dumping_dur=info[3],
        returning_dur=info[4],
        truck_status=info[5],
        time=simulation)
    truck_list.append(truck)

# total count of trucks
quantity_of_trucks = len(truck_list)

# creating one loader
the_loader = Loader(False, simulation.now)

# write in "output-event-simulation-data.txt" kind of a logger file but it's not!
with open("output-simulation-data.txt", 'w') as txt_file:
    # write starting details: simulation is running with these configs etc.
    txt_file.write("*" * 80 + "\n")
    txt_file.write(time.strftime(r'%Y-%m-%d %H:%M %Z',
                                 time.localtime(time.time())) + "\n")
    txt_file.write("Event logs of the program from main.py" + "\n")
    txt_file.write("-" * 80 + "\n")
    txt_file.write("One loader machine is being created." + "\n")
    txt_file.write("Created truck's list:" + "\n")
    for truck in truck_list:
        write_this = f"{truck.index} Truck ID={truck.id}: Status={truck.status}, " \
                     f"Loading duration= {truck.loading_duration}, Hauling duration= {truck.hauling_duration}, " \
                     f"Dumping duration= {truck.dumping_duration}, Returning duration= {truck.returning_duration}\n"
        txt_file.write(write_this)

    # every discrete time in the sim will be stored here
    discrete_times = []

    # a counter for milestones (increasing by 1 every loop)
    discrete_time_counter = 0
    chronological_list = []
    # Main Loop of the simulation for checking and doing EVERY available activity:
    for i in range(50):

        # writing with Discrete Event Simulation logics:
        txt_file.write("- - " * 20 + "\n")
        txt_file.write("Simulation time is now: {}\n".format(simulation.now))

        # write loader's stats
        txt_file.write("The loader is or will be available at time {}\n"
                       "The loader's working status is now {}. "
                       "(True: Working, False: Idle).\n".format(the_loader.available_time, the_loader.working))

        brunch_data = []
        real_data = []
        # write truck's status
        for j in range(quantity_of_trucks):
            write_this = "Truck {} is at round {}. Its working status:{}".format(
                truck_list[j].id, truck_list[j].round, truck_list[j].working)
            txt_file.write(write_this + "\n")

        # reset branch to the main simulation before starting the branch
        branch.now = simulation.now
        write_this = "\nStarting a branch Simulation for prioritizing and checking doable activities:\n"
        txt_file.write(write_this)

        # do a branch simulation of the main simulation for prioritizing and checking doable activities
        # call process method for all of the trucks
        for j in range(quantity_of_trucks):
            if not truck_list[j].working:
                single_branch_data = truck_list[j].process(branch, the_loader, txt_file)
                brunch_data.append(single_branch_data)

        # print(brunch_data)

        # removing None values
        brunch_data = [k for k in brunch_data if k]

        # Prioritize list based on Early Start and Early Finish
        brunch_data = sorted(brunch_data, key=lambda k: [k[0], k[1]])

        write_this = "Branch Simulation has been completed. branch data of trucks (Sorted and Prioritized):\n" \
                     "[start, finish, ID, current status]\n"
        txt_file.write(write_this)
        for item in brunch_data:
            txt_file.write("%s\n" % list(item))
        # print(brunch_data)

        write_this = "\nStarting the main Simulation:\n"
        txt_file.write(write_this)
        for j in brunch_data:
            single_real_data = truck_list[j[2]].process(simulation, the_loader, txt_file)
            real_data.append(single_real_data)
        # print(real_data)
        real_data = [k for k in real_data if k]

        write_this = "The main simulation is done. started truck's activities are:\n" \
                     "[start, finish, ID, current status]\n"
        txt_file.write(write_this)
        for item in real_data:
            txt_file.write("%s\n" % list(item))

        chronological_list.append(real_data)

        # print(real_data)

        # Check if no activity happens then no need to add new future time to discrete_times list
        if len(real_data) > 0:
            discrete_time = list(list(zip(*real_data))[1])
            # print(discrete_time)
            discrete_times += discrete_time
            # print(discrete_times)

            discrete_times = sorted(discrete_times)

            # removing duplicated times in the list
            discrete_times = list(dict.fromkeys(discrete_times))

        simulation.now = discrete_times[discrete_time_counter]

        # print("- - " * 15)
        # print("simulation time is now:", simulation.now)

        for j in range(quantity_of_trucks):
            if truck_list[j].starting_activity < simulation.now < truck_list[j].finishing_activity:
                truck_list[j].working = True
            else:
                truck_list[j].working = False

            # print("Truck {} working status: {}".format(
            #     truck_list[j].id, truck_list[j].working))

        if the_loader.available_time <= simulation.now:
            the_loader.working = False

        discrete_time_counter += 1

print("*" * 60)
print("Program Simulation is done.\n"
      "OPEN FILE : output-chronological-list-truck.csv\n"
      "OPEN FILE : output-simulation-data.txt")

modified_01_chronological_list = []
for layer1 in chronological_list:
    for layer2 in layer1:
        modified_01_chronological_list.append(layer2)

modified_02_chronological_list = []
for i in modified_01_chronological_list:
    modified_02_chronological_list.append((i[0], i[1], truck_list[i[2]].id, i[3]))

write_csv("output-chronological-list-truck.csv", modified_02_chronological_list)
