class SimulationTime:
    type = "Real Simulation"
    now = 0
    
    def Add(duration):
        SimulationTime.now += duration
        return SimulationTime.now
    def ResetVirtual(duration):
        SimulationTime.now -= duration
    
class BranchTime(SimulationTime):
    type = "Branch"
    def Add(duration):
        BranchTime.now += duration
        return BranchTime.now
    
    def ResetVirtual(_):
        BranchTime.now = SimulationTime.now

class Loader:
    
    def __init__(self, loaderStatus):
        self.status=loaderStatus

    # def Working(self):
    #     """
    #     docstring
    #     """
    #     print("Loader {} started working at {}".format(self.id,))
    #     print("Truck {} Finished working at {}".format(self.id))

class Truck:
    
    def __init__(self, ID, loadingDur, haulingDur, dumpingDur, returningDur):
        self.id = ID
        self.loadingDuration = loadingDur
        self.haulingDuration = haulingDur
        self.dumpingDuration = dumpingDur
        self.returningDuration = returningDur
        self.status = "cycle starting"
    
    def Process(self,TimeClass,loader):
        if self.status == "cycle starting":
            return self.Loading(TimeClass,loader)
            


    def Loading(self,TimeClass,loader):
        """
        docstring
        """
        if loader.status == "idle":
            
            print(TimeClass.type,"Truck {} started Loading at {}".format(self.id,TimeClass.now))
            startTime = TimeClass.now
            TimeClass.Add(self.loadingDuration)
            print(TimeClass.type,"Truck {} Finished Loading at {}".format(self.id,TimeClass.now))
            finishTime = TimeClass.now
            
            if TimeClass == SimulationTime:
                loader.status = "active"
                self.status = "idle"
            TimeClass.ResetVirtual(self.loadingDuration)
            return (startTime, finishTime, self.id, "Loading") 
        else:
            print(TimeClass.type,"Truck {} couldnt start loading at {}".format(self.id,TimeClass.now))

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
    #     print("Truck {} Finished Returninging at {}".format(self.id, time))


# loadingDuration=10
# haulingDuration=10
# dumpingDuration=3
# returninDduration=5

# myTruckList=[]
# for i in range(quantity):
#     myTruckList.append(Truck(ID=i,
#                 loadingDur=loadingDuration,
#                 haulingDur=haulingDuration,
#                 dumpingDur=dumpingDuration,
#                 returningDur=returninDduration))


a0 = Truck(
        ID=0,
        loadingDur=10,
        haulingDur=20,
        dumpingDur=7,
        returningDur=15)


a1 = Truck(
        ID=1,
        loadingDur=15,
        haulingDur=30,
        dumpingDur=9,
        returningDur=10)


a2 = Truck(
        ID=2,
        loadingDur=9,
        haulingDur=15,
        dumpingDur=11,
        returningDur=5)


myTruckList = [a0,a1,a2]
quantity = len(myTruckList)

myLoader=Loader("idle")


for i in range(1):
    activityData=[]
    realData = []
    for j in range(quantity):
        singleBranchData = myTruckList[j].Process(BranchTime,myLoader)
        activityData.append(singleBranchData)
    
    # Priority list based on ES and EF
    activityData = sorted(activityData , key=lambda k: [k[0], k[1]])
    print(activityData)
    for j in range(quantity):
        singleRealData = myTruckList[activityData[j][2]].Process(SimulationTime,myLoader)
        realData.append(singleRealData)
    print(realData)
        
    
    
    
















