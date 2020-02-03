import requests
import re 
import datetime

class Passwords:
    def __init__(self,portal,username,password,ClientID,LocationID,lngMemberID,lngShiftHeaderID,lngDivisionID,Location,Employee):
        self.portal=portal
        self.username=username
        self.password=password
        self.ClientID=ClientID
        self.LocationID=LocationID
        self.lngMemberID=lngMemberID
        self.lngShiftHeaderID=lngShiftHeaderID
        self.lngDivisionID=lngDivisionID
        self.Location=Location
        self.Employee=Employee

class Times:
    start=None
    bStart=None
    bFinish=None
    finish=None

    def __init__(self,text):
        self.findTimes(text)
        self.countBreak()
    
    def convertTime(self,text):
        if text:
            return datetime.datetime.strptime(text,'%H:%M:%S')
        return None

    def searchTime(self,pattern,text):
        try:
             re.findall(r'(\d{2}:\d{2}:\d{2}).{20,30}'+pattern,text)[0]
        except IndexError:
            return None

    def findTimes(self,text):
        Times.start=self.convertTime(self.searchTime('Clock In',text))
        Times.bStart=self.convertTime(self.searchTime('Break Start',text))
        Times.bFinish=self.convertTime(self.searchTime('Break End',text))
        Times.finish=self.convertTime(self.searchTime('Clock Out',text))

    def howMuchBreak(self):
        return (today - self.bStart).seconds

    def countBreak(self):
        if self.bStart:
            if self.bFinish:
                print(f'You already had {int((self.bFinish - self.bStart).seconds/60)} minutes long break.')
            else:
                print(f'You are already {self.howMuchBreak()/60} minutes on your break.')
        else:
            print('You didnt sign in today.')

#Fill up required info in Passwords object
passObject=Passwords()
payLoad={
    'Username' : passObject.username,
    'Password' : passObject.password
}

print("Welcome 😎")
today=datetime.datetime.today()
with requests.Session() as s:
    c1=s.get(f'https://fourthhospitality.com/{passObject.portal}')
    if c1.status_code==200:
        print(". 1/3")
    c2=s.post('http://www.fourthhospitality.com/Portal/Registration/login.asp',data=payLoad)
    if c2.status_code==200:
        print(".. 2/3")
    stringDay='{}{}{}{}{}'.format(today.strftime('%d'),'%2F',today.strftime('%m'),'%2F',today.strftime('%Y'))
    c3=s.get(f"https://www.fourthhospitality.com/Portal/Admin/Modules/HR/Rotas/Time_Attendance/ViewAttendance.asp?ClientID={passObject.ClientID}&LocationID={passObject.LocationID}&lngMemberID={passObject.lngMemberID}&ShiftDate={stringDay}&lngShiftHeaderID={passObject.lngShiftHeaderID}&lngDivisionID={passObject.lngDivisionID}&lngME_ID=0&lngDay=5&g_intAttendanceLateThreshold=2&g_intAttendanceEarlyThreshold=2&clockStatus=1&Location={passObject.Location}&Employee={passObject.Employee}&lngMainJob=1")
    if c3.status_code==200:
        print("... 3/3")

shiftTime=Times(c3.text)

pass
