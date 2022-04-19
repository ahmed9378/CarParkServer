from datetime import datetime

# .env library
from dotenv import dotenv_values
config = dotenv_values(".env")


class RequestInfo():
    def __init__(self, requestIp=None, requestTime=None):
        self.requestIp = requestIp
        self.requestTime = []


class RequestRecorder(RequestInfo):
    def __init__(self):
        self.requestList = []
    
    # public methods
    def addRecord(self, rIp):
        return self.__addRecord(rIp)

    def checkLastTenRequest(self, rIp):
        return self.__checkLastTenRequest(rIp)

    def rqListPrint(self):
        return self.__rqListPrint()

    def ipInTheList(self, rip, lst):
        return self.__ipInTheList(rip, lst)

    # private methods
    def __addRecord(self, rIp):
        reqt = datetime.now().timestamp()
        # first request
        if (self.requestList == []):
            s = RequestInfo()
            s.requestIp = rIp
            s.requestTime.append(reqt)
            self.requestList.append(s)

        # other requests
        else:
            # first time visit record
            ipav, ind = self.ipInTheList(rIp, self.requestList)
            if (not ipav):
                s = RequestInfo()
                s.requestIp = rIp
                s.requestTime.append(reqt)
                self.requestList.append(s)

            # next time visit record time
            if (ipav):
                self.requestList[ind].requestTime.append(reqt)

    def __ipInTheList(self, rip, lst):
        i = 0
        for s in lst:
            if s.requestIp == rip:
                return True, i
            i += 1
        return False, -1

    def __checkLastTenRequest(self, rIp):
        ipav, ind = self.ipInTheList(rIp, self.requestList)
        rtc = self.requestList[ind].requestTime.__len__()
        reqCountLimit = int(config.get("IP_REQUEST_COUNT"))
        reqTimeLimit = int(config.get("IP_REQUEST_TIME_LIMIT"))
        if rtc > reqCountLimit:
            # 10 attempt exceeded
            delta = self.requestList[ind].requestTime[rtc-1] - \
                self.requestList[ind].requestTime[rtc-reqCountLimit-1]
            # delet old request times
            if rtc > reqCountLimit+10:
                del self.requestList[ind].requestTime[0:rtc-20]

            # todo: delete the old ips from request list
            # for rq in self.requestList:
            #     if (not self.ipInTheList(rip, self.requestList)):
            #         pass
            #     pass

            # return
            return False if delta > reqTimeLimit else True

    def __rqListPrint(self):
        for x in self.requestList:
            print(x.requestIp, x.requestTime)
