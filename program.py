class SimulationTime:
    type = "Real Simulation"
    now = 0

    def add(self, duration):
        SimulationTime.now += duration
        return SimulationTime.now

    def reset_virtual(self, duration):
        SimulationTime.now -= duration


class BranchTime(SimulationTime):
    type = "Branch"

    def add(self, duration):
        BranchTime.now += duration
        return BranchTime.now

    def reset_virtual(self, duration):
        BranchTime.now = SimulationTime.now


class Loader:

    def __init__(self, loader_status):
        self.status = loader_status

    # def Working(self):
    #     """
    #     docstring
    #     """
    #     print("Loader {} started working at {}".format(self.id,))
    #     print("Truck {} Finished working at {}".format(self.id))


class Truck:

    def __init__(self, truck_id, loading_dur, hauling_dur, dumping_dur, returning_dur):
        self.id = truck_id
        self.loading_duration = loading_dur
        self.hauling_duration = hauling_dur
        self.dumping_duration = dumping_dur
        self.returning_duration = returning_dur
        self.status = "cycle starting"

    def process(self, TimeClass, loader):
        if self.status == "cycle starting":
            return self.loading(TimeClass, loader)

    def loading(self, TimeClass, loader):
        """
        docstring
        """
        if loader.status == "idle":

            print(TimeClass.type, "Truck {} started Loading at {}".format(self.id, TimeClass.now))
            startTime = TimeClass.now
            TimeClass.add(self.loading_duration)
            print(TimeClass.type, "Truck {} Finished Loading at {}".format(self.id, TimeClass.now))
            finishTime = TimeClass.now

            if TimeClass == SimulationTime:
                loader.status = "active"
                self.status = "idle"
            TimeClass.reset_virtual(self.loading_duration)
            return startTime, finishTime, self.id, "Loading"
        else:
            print(TimeClass.type, "Truck {} could not start loading at {}".format(self.id, TimeClass.now))

    # def Hauling(self):
    #     """
    #     docstring
    #     """

    #     print("Truck {} started Hauling at {}".format(self.id, time))
    #     time += self.haulingDuration
    #     print("Truck {} Finished Hauling at {}".format(self.id, time))

    # def Dumping(self):
    #     """
    #     docstring
    #     """

    #     print("Truck {} started Dumping at {}".format(self.id, time))
    #     time += self.dumpingDuration
    #     print("Truck {} Finished Dumping at {}".format(self.id, time))

    # def Returning(self):
    #     """
    #     docstring
    #     """

    #     print("Truck {} started Returning at {}".format(self.id, time))
    #     time += self.returningDuration
    #     print("Truck {} Finished Returning at {}".format(self.id, time))


a0 = Truck(
    truck_id=0,
    loading_dur=10,
    hauling_dur=20,
    dumping_dur=7,
    returning_dur=15)

a1 = Truck(
    truck_id=1,
    loading_dur=15,
    hauling_dur=30,
    dumping_dur=9,
    returning_dur=10)

a2 = Truck(
    truck_id=2,
    loading_dur=9,
    hauling_dur=15,
    dumping_dur=11,
    returning_dur=5)

myTruckList = [a0, a1, a2]
quantity = len(myTruckList)

myLoader = Loader("idle")

for i in range(1):
    activityData = []
    realData = []
    for j in range(quantity):
        singleBranchData = myTruckList[j].process(BranchTime, myLoader)
        activityData.append(singleBranchData)

    # Priority list based on ES and EF
    activityData = sorted(activityData, key=lambda k: [k[0], k[1]])
    print(activityData)
    for j in range(quantity):
        singleRealData = myTruckList[activityData[j][2]].process(SimulationTime, myLoader)
        realData.append(singleRealData)
    print(realData)
