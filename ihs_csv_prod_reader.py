import os
# import time
from datetime import datetime
from enum import Enum

class WellStatus(object):
    ACTIVE   = 'A'
    INACTIVE = 'I'

# function to determine total num of wells in list
def numofwells(lines):
    i = 0
    for line in lines:
        if codes["Start Record Label"] in line:
            i += 1
    return i

# Current directory
dircurd = os.getcwd()

# Change directory
os.chdir("C:/Users/Dario/Documents/IHS")

print("----------------------------------------------------------------------------------------------------")
start_dt = datetime.now()
print("starting ...")

# Opening file
fname = "Atascosa - 298 Production CSV.98c"
#fname = "LOUISIANA - 298 Production.98c"
#fname = "HAYNESVILLE - 298 Production.98c"

fo = open(fname, "r")
print("  opening file (reading): ", fo.name)

# reading entire file
print("  reading file ...")
lines = fo.readlines()
print("  number of lines: ", len(lines))

# Closing file
print("  closing file ...")
fo.close()

# dictionary with 298 Production Export codes
codes = {
    "Start Record Label": "START_US_PROD",
    "Unique ID Record": "++ ",
    "Entity Record": "+A ",
    "Congressional and Carter Location": "+AC",
    "Texas Location": "+AT",
    "Offshore Location": "+AO",
    "Regulatory Record": "+AR",
    "Multiple County Record": "+A#",
    "Name Record 1": "+B ",
    "Name Record 2": "+C ",
    "Well Record": "+D ",
    "Lat/Long Record": "+D!",
    "Test Information Record 1": "+E ",
    "Test Information Record 2": "+E!",
    "Cumulative Production": "+F ",
    "Monthly Production": "+G ",
    "Cumulative Injection": "+I ",
    "Monthly Injection": "+J ",
    "Total Disposition for Current Month": "+K ",
    "Monthly Disposition by Transporter": "+L ",
    "End Record Label": "END_US_PROD"
}

# print only selected coded lines
num_wells = 0
non_multi = 0
num_wells_active = 0

fout = open("Atascosa - 298 Production output.csv", "w")
#fout = open("LOUISIANA - 298 Production output.csv", "w")
#fout = open("HAYNESVILLE - 298 Production output.csv", "w")

print("  opening file (production): ", fout.name)

#fout2 = open("HAYNESVILLE - 298 Header output.csv", "w")
fout2 = open("Atascosa - 298 Header output.csv", "w")
print("  opening file (header):", fout2.name)


for line in lines:
    # If new well count it -- uid is initialized
    if codes["Start Record Label"] in line:
        num_wells += 1
        uid = ""
        WellStat = ""
        res_name = ""

        # count non-MULTI well -- convert uid to list
        if not line.split(",")[1].__contains__("MULTI"):
            non_multi += 1
            uid = line.split(",")[1]
    # set (write) reservoir name on header
    if codes["Name Record 2"] in line:
        res_name = line.split(",")[5]
    # set Well Status
    if codes["Well Record"] in line:
        WellStat = line.split(",")[9].strip('"')
        if WellStat == WellStatus.ACTIVE:
            num_wells_active += 1
    # set (write) well header name, and coordinates
    if codes["Lat/Long Record"] in line:
        #  and WellStat == WellStatus.ACTIVE
        fout2.write(','.join(map(str, uid.split() + line.split(',')[1:3])) + "," + res_name.strip() + "\n")
    # add uid to monthly production record
    if line.split(",")[0] == codes["Monthly Production"] and len(uid) > 0:
        # and WellStat == WellStatus.ACTIVE
        fout.write(','.join(map(str, uid.split() + line.split(',')[1:8])))

# closing file for writing
fout.close()
fout2.close()
print("  closing file (header) ...")
print("  closing file (production) ...")

print('------------')
print("  # wells: ", num_wells, ";    non-multi wells: ", non_multi, ";    active wells: ", num_wells_active)

end_dt = datetime.now()
print("----------------------------------------------------------------------------------------------------")
print("start: ", start_dt, " -- end: ", end_dt, " -- Elapsed: ",
      (end_dt - start_dt))




