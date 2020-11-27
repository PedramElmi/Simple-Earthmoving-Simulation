
class Time:
    def __init__(self, time_type) -> None:
        self.type = time_type
        self.now = 0

    def add(self, duration):
        self.now += duration
        return self.now

    def reset(self, duration):
        self.now -= duration

class Loader:

    def __init__(self, working_status: bool, start_working_time):
        self.working = working_status
        self.available_time = start_working_time

    # def Working(self):
    #     """
    #     docstring
    #     """
    #     print("Loader {} started working at {}".format(self.id,))
    #     print("Truck {} Finished working at {}".format(self.id))
    
class Truck:

    
    def __init__(self, truck_id, loading_dur, hauling_dur, dumping_dur, returning_dur, time: object):
        self.id = truck_id
        self.loading_duration = loading_dur
        self.hauling_duration = hauling_dur
        self.dumping_duration = dumping_dur
        self.returning_duration = returning_dur
        self.event_time = time.now
        self.status = "initiating new cycle"
        self.round = 0
        self.working = False
        self.starting_activity = 0
        self.finishing_activity = 0
        
        
    
    def process(self, time: object, loader: object):

        if self.status == "initiating new cycle":
            if not loader.working:
                if time == "simulation":
                    self.round += 1
                return self.load(time, loader)
            else:
                print(time.type, "Truck {} could not start loading at {}".format(
                    self.id, time.now))
                pass

        elif self.status == "loading":
            return self.haul(time)

        elif self.status == "hauling":
            return self.dump(time)

        elif self.status == "dumping":
            return self.truck_return(time)

        else:
            return None, None, None


    def load(self, time: object, loader: object):
        """
        docstring
        """
        print(time.type, "Truck {} started Loading at {}".format(
            self.id, time.now))
        start_time = time.now
        time.add(self.loading_duration)
        print(time.type, "Truck {} Finished Loading at {}".format(
            self.id, time.now))
        finish_time = time.now

        if time.type == "simulation":
            loader.working = True
            loader.available_time = finish_time
            self.status = "loading"
            self.starting_activity = start_time
            self.finishing_activity = finish_time

        time.reset(self.loading_duration)
        return start_time, finish_time, self.id, self.status

    def haul(self, time: object):
        """
        docstring
        """
        print(time.type, "Truck {} started Hauling at {}".format(self.id, time.now))
        start_time = time.now
        time.add(self.loading_duration)
        print(time.type, "Truck {} Finished Hauling at {}".format(self.id, time.now))
        finish_time = time.now

        if time.type == "simulation":
            self.status = "hauling"
            self.starting_activity = start_time
            self.finishing_activity = finish_time

        time.reset(self.loading_duration)
        return start_time, finish_time, self.id, self.status

    def dump(self, time: object):
        """
        docstring
        """
        print(time.type, "Truck {} started Dumping at {}".format(self.id, time.now))
        start_time = time.now
        time.add(self.loading_duration)
        print(time.type, "Truck {} Finished Dumping at {}".format(self.id, time.now))
        finish_time = time.now

        if time.type == "simulation":
            self.status = "dumping"
            self.starting_activity = start_time
            self.finishing_activity = finish_time

        time.reset(self.loading_duration)
        return start_time, finish_time, self.id, self.status

    def truck_return(self, time: object):
        """
        docstring
        """
        print(time.type, "Truck {} started Returning at {}".format(self.id, time.now))
        start_time = time.now
        time.add(self.loading_duration)
        print(time.type, "Truck {} Finished Returning at {}".format(self.id, time.now))
        finish_time = time.now

        if time.type == "simulation":
            self.status = "initiating new cycle"
            self.starting_activity = start_time
            self.finishing_activity = finish_time

        time.reset(self.loading_duration)
        return start_time, finish_time, self.id, self.status



branch = Time("branch")
simulation = Time("simulation")


a0 = Truck(
    truck_id=0,
    loading_dur=10,
    hauling_dur=20,
    dumping_dur=7,
    returning_dur=15, time=simulation)

a1 = Truck(
    truck_id=1,
    loading_dur=15,
    hauling_dur=30,
    dumping_dur=9,
    returning_dur=10, time=simulation)

a2 = Truck(
    truck_id=2,
    loading_dur=9,
    hauling_dur=15,
    dumping_dur=11,
    returning_dur=5, time=simulation)

truck_list = [a0, a1, a2]
quantity = len(truck_list)

truck_list[1].status = "loading"


loader01 = Loader(False, simulation.now)


discrete_times = []
discrete_event_count = 0
for i in range(10):
    brunch_data = []
    real_data = []
    
    
    
    for j in range(quantity):
        print("Truck {} round {}".format(truck_list[j].id,truck_list[j].round))



    branch.now = simulation.now
    for j in range(quantity):
        if not truck_list[j].working:
            single_branch_data = truck_list[j].process(branch, loader01)
            brunch_data.append(single_branch_data)
    print(brunch_data)
    brunch_data = [k for k in brunch_data if k]



    # Priority list based on ES and EF
    brunch_data = sorted(brunch_data, key=lambda k: [k[0], k[1]])
    print(brunch_data)



    for j in brunch_data:
        single_real_data = truck_list[j[2]].process(simulation, loader01)
        real_data.append(single_real_data)
    print(real_data)
    real_data = [k for k in real_data if k]
    print(real_data)



    discrete_time = list(list(zip(*real_data))[1])
    print(discrete_time)
    discrete_times += discrete_time
    print(discrete_times)
    discrete_times = sorted(discrete_times)
    simulation.now = discrete_times[discrete_event_count]
    print("*" * 30)
    print("simulation time is now:", simulation.now)



    for j in range(quantity):
        if truck_list[j].starting_activity < simulation.now < truck_list[j].finishing_activity:
            truck_list[j].working = True
        else:
            truck_list[j].working = False
        print("Truck {} working status: {}".format(
            truck_list[j].id, truck_list[j].working))

    if loader01.available_time <= simulation.now:
        loader01.working = False

    discrete_event_count += 1
