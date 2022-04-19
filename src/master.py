import park
import requestRecorder


class Master:
    def __init__(self):
        self.p = park.Park()
        self.r = requestRecorder.RequestRecorder()

    # park master
    def parkACar(self, car_number):
        return self.p.parkaCar(car_number)

    def unParkACar(self, car_number=None, slot_number=None):
        return self.p.unparkaCar(car_number, slot_number)

    def isGarageFull(self):
        return not self.p.freeSlotAvailable()

    def getParkInfo(self, car_number=None, slot_id=None):
        return self.p.getSlotInfo(car_number, slot_id)

    def isParkAvailable(self, slot_number=None):
        return self.p.isSlotAvailable(slot_number)

    def isCarParked(self, car_number=None):
        return self.p.isCarAvailable(car_number)

    def getParkList(self):
        return self.p.getAllParkInSlot()

    def getParkStrList(self):
        return self.p.getAllPArkInStr()

    def countFreeSlots(self):
        return self.p.countAvailableSlots()

    # request master

    def addRequestRecord(self, rip):
        self.r.addRecord(rip)

    def printRequestList(self):
        self.r.rqListPrint()

    def checkRequestLimits(self, rip):
        return self.r.checkLastTenRequest(rIp=rip)
