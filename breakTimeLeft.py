import requests
import re as re
import datetime
timeNow=datetime.datetime.today()
print("hey")

firstUrl='https://fourthhospitality.com/*removed*'
payload = {'Username': '', 'Password': ''}

print("connecting to Fourth")
s=requests.Session()
connect=s.get(firstUrl)
if "<Response [200]>" in str(connect):
    print(". 1/3")
url="http://www.fourthhospitality.com/Portal/Registration/login.asp"
connect2=s.post(url, data=payload)
if "<Response [200]>" in str(connect2):
    print(".. 2/3")


connect3=s.get("https://www.fourthhospitality.com/Portal/menus/frameset.asp")
if "<Response [200]>" in str(connect3):
    print("... 3/3")

# create today date url
day=str(datetime.datetime.today().day)
month=str(datetime.datetime.today().month)
year=str(datetime.datetime.today().year)
if len(day)<2:
    day="0"+day
if len(month)<2:
    month="0"+month
todayDateUrl=day+"%2F"+month+"%2F"+year


url2="https://www.fourthhospitality.com/Portal/Admin/Modules/HR/Rotas/Time_Attendance/ViewAttendance.asp?ClientID=*removed*&LocationID=*removed*&lngMemberID=*removed*&ShiftDate="+str(todayDateUrl)+"&lngShiftHeaderID=*removed*&lngDivisionID=*removed*&lngME_ID=0&lngDay=5&g_intAttendanceLateThreshold=2&g_intAttendanceEarlyThreshold=2&clockStatus=1&Location=*removed*&Employee=*removed*&lngMainJob=1"
connect4=s.get(url2)

breakStartMatch=re.findall("(\d{2}:\d{2}:\d{2})<.td><td ALIGN='center'>Break Start",connect4.text)
if len(breakStartMatch)<1:
    print("You didnt sign in today ")
else:
    parsedTime=datetime.datetime.strptime(breakStartMatch[0],"%H:%M:%S")
    o=(timeNow-parsedTime)
    startTime = (datetime.datetime.min + o).time()
    leftTime=(startTime.minute)
    print("You have left "+str(leftTime)+" minutes till your break finish")
