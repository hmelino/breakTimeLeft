import requests
import re as re
import datetime
import naah
from naah import *
timeNow=datetime.datetime.today()
print("Welcome 😎")

firstUrl='https://fourthhospitality.com/*removed*'
payload = {'Username': str(naah.d1), 'Password': str(naah.d2)}

print("connecting to Fourth...")
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

customDate="08%2F08%2F2019"
url2="https://www.fourthhospitality.com/Portal/Admin/Modules/HR/Rotas/Time_Attendance/ViewAttendance.asp?ClientID=*removed*&LocationID=*removed*&lngMemberID=*removed*&ShiftDate="+str(todayDateUrl)+"&lngShiftHeaderID=*removed*&lngDivisionID=*removed*&lngME_ID=0&lngDay=5&g_intAttendanceLateThreshold=2&g_intAttendanceEarlyThreshold=2&clockStatus=1&Location=*removed*&Employee=*removed*&lngMainJob=1"
connect4=s.get(url2)
finalConnect=connect4.text

breakStartMatch=re.findall("(\d{2}:\d{2}:\d{2})<.td><td ALIGN='center'>Break Start",finalConnect)
signIn=re.findall("(\d{4})'><.td><td ALIGN='center'>Clock In",finalConnect)

if len(signIn)<1:
    print("You are off today 😒😛😂 ")
elif len(breakStartMatch)<1:
  print("You didnt sign for your break 🙈")
else:
    parsedTime=datetime.datetime.strptime(breakStartMatch[0],"%H:%M:%S")
    o=(timeNow-parsedTime)
    startTime = (datetime.datetime.min + o).time()
    leftTime=(startTime.minute)
    print("You have left "+str(leftTime)+" minutes till your break finish")
