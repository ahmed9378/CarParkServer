from datetime import datetime

# .env library
from dotenv import dotenv_values
config = dotenv_values(".env")


class Slot:
    def __init__(self, slot_id, car_plate_no, park_dtime, is_free):
        self.slot_id = int(slot_id)
        self.car_plate_no = car_plate_no
        self.park_dtime = park_dtime
        self.is_free = bool(is_free)


class Park:
    # init
    def __init__(self):
        self.park_slot = []
        if (self.__validate(int(config.get("PARKING_LOT_SIZE")), 1)):
            self.parksize = int(config.get("PARKING_LOT_SIZE"))
        else:
            raise ValueError(
                "Error check .env file parking lot size must be integer")
        self.__genrateSlots()

    def freeSlotAvailable(self):
        for z in self.park_slot:
            if(z.is_free):
                return True
        return False

    def parkaCar(self, car_number):
        return self.__parkCar(car_number=car_number)

    def unparkaCar(self, car_number=None, slot_number=None):
        return self.__unparkCar(car_number, slot_number)

    def getSlotInfo(self, car_number=None, slot_number=None):
        return self.__getSlotInfo(car_number, slot_number)

    def getAllParkInSlot(self):
        return self.park_slot

    def getAllPArkInStr(self):
        if self.park_slot is not None and self.park_slot.__len__() > 0:
            rlist = []
            for x in self.park_slot:
                rlist.append(str(x.slot_id)+"," + str(
                    x.car_plate_no)+"," + str(x.park_dtime))
            return rlist

    def isSlotAvailable(self, slot_numer):
        if self.__validate(slot_numer, 2):
            for z in self.park_slot:
                if(z.slot_id == slot_numer):
                    return False
            return True

    def isCarAvailable(self, car_number):
        if self.__validate(car_number, 3):
            for z in self.park_slot:
                if(z.car_plate_no == car_number):
                    return True
            return False

    def countAvailableSlots(self):
        cont = 0
        for z in self.park_slot:
            if(z.is_free):
                cont += 1
        return cont

    # private methods
    # return slot information {slot_id, car_number, park_time}

    def __getSlotInfo(self, car_number, slot_id):
        if self.__validate(car_number, 3):
            if self.isCarAvailable(car_number):
                for z in self.park_slot:
                    if(z.car_plate_no == car_number):
                        return "slot No.:" + str(z.slot_id)+" Car No.:" + str(z.car_plate_no)+" Parking Time:"+str(z.park_dtime)
                return "No car info"
        elif self.__validate(slot_id, 2):
            if(not self.isSlotAvailable(slot_id)):
                for z in self.park_slot:
                    if(z.slot_id == slot_id):
                        return "slot No.:" + str(z.slot_id)+" Car No.:" + str(z.car_plate_no)+" Parking Time:"+str(z.park_dtime)
                return "No car info"
        else:
            return "Error data validation"

    # unpark a car using either the car number or the slot number
    def __unparkCar(self, car_number, slot_id):
        if self.__validate(car_number, 3):
            if self.isCarAvailable(car_number):
                for z in self.park_slot:
                    if(z.car_plate_no == car_number):
                        s = Slot(slot_id=z.slot_id, car_plate_no=None,
                                 park_dtime=None, is_free=True)
                        self.park_slot.__setitem__(z.slot_id, s)
                        return "Car unparked from slot: "+str(z.slot_id)
            else:
                return "No car found with this number"
        elif self.__validate(slot_id, 2):
            if(not self.isSlotAvailable(slot_id)):
                for z in self.park_slot:
                    if(z.slot_id == slot_id):
                        if z.car_plate_no == None:
                            return "Slot "+str(z.slot_id)+" is already free"
                        else:
                            s = Slot(slot_id=z.slot_id,
                                     car_plate_no=None,
                                     park_dtime=None,
                                     is_free=True)
                            self.park_slot.__setitem__(z.slot_id, s)
                            return "Car unparked from slot: "+str(z.slot_id)
        else:
            return "Error data validation"

    # parking a car with str number
    def __parkCar(self, car_number):
        if(self.__validate(car_number, 3)):
            if(self.freeSlotAvailable()):
                sid = self.__pickaSlot()
                s = Slot(slot_id=sid,
                         car_plate_no=car_number,
                         park_dtime=datetime.now().strftime("%c"),
                         is_free=False)
                self.park_slot.__setitem__(sid, s)
                return "Car parked successfully in slot: " + str(sid)
            else:
                return "No free slot available"
        else:
            return "Please enter correct data format"

    # create garage with free slots
    def __genrateSlots(self):
        try:
            for x in range(self.parksize):
                s = Slot(slot_id=x,
                         car_plate_no=None,
                         park_dtime=None,
                         is_free=True)
                self.park_slot.append(s)
        except:
            raise NotImplementedError("Error genrating park slots")

    # pick the slot number of the first parking slot
    def __pickaSlot(self):
        if (self.park_slot):
            for z in self.park_slot:
                if(z.is_free):
                    return int(z.slot_id)
            else:
                return None
        else:
            raise ValueError("Error variable not found")

    # check integer is withen range limits
    def __withenRange(self, num, minlimt, maxlimt):
        return True if num > minlimt and num < maxlimt else False

    # validate with 2 options
    def __validate(self, xval, opt=2):
        if (xval is not None):
            # unsined integer
            if (opt == 1 and isinstance(xval, int)):
                if(xval >= 0):
                    return True
                else:
                    return False
            # unsined integer within garage size start from 0
            elif (opt == 2 and isinstance(xval, int)):
                if(self.__withenRange(xval, -1, self.parksize)):
                    return True
                else:
                    return False
            # string validation
            elif (opt == 3 and isinstance(xval, str)):
                if (xval.isalnum()):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
