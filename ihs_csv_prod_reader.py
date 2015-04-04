import os
from datetime import datetime

class WellStatus(object):
    ACTIVE = 'A'
    INACTIVE = 'I'

# function to determine total num of wells in list
def numofwells(lines):
    i = 0
    for line in lines:
        if codes["Start Record Label"] in line:
            i += 1
    return i

# Current directory
curdir = os.getcwd()

# Change directory
os.chdir("C:/Users/Dario/Documents/IHS")

print("----------------------------------------------------------------------------------------------------")
start_dt = datetime.now()
print("starting ...")

# open production ihs export file for read-only
fname = "Atascosa - 298 Production CSV.98c"
fo = open(fname, "r")
print("  opening file (input): ", fo.name)

# read production ihs export file
print("    reading file ...")
lines = fo.readlines()
print("    number of read lines: ", len(lines))

# close production ihs export file
print("  closing file (input) ...")
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

# to store num_wells, non_multi wells, and active wells
num_wells = 0
non_multi = 0
num_wells_active = 0

# creates production ihs export file for writing
fout = open("Atascosa - 298 Production output.csv", "w")
print("  opening file (production): ", fout.name)

# creates header ihs export file for writing
fout2 = open("Atascosa - 298 Header output.csv", "w")
print("  opening file (header):", fout2.name)

for line in lines:
    # if new well found -- uid is initialized
    # increment num_wells
    # initialize uid, wellstat, res_name
    if codes["Start Record Label"] in line:
        num_wells += 1
        uid = ""
        wellstat = ""
        res_name = ""
        # count non-MULTI well
        if not line.split(",")[1].__contains__("MULTI"):
            non_multi += 1
    # set reservoir name
    if codes["Name Record 2"] in line:
        res_name = line.split(",")[5]
    # set uid -- active well indicator
    if codes["Well Record"] in line:
        uid = line.split(",")[1]
        wellstat = line.split(",")[9].strip('"')
        if wellstat == WellStatus.ACTIVE:
            num_wells_active += 1
    # set well header name, and coordinates
    if codes["Lat/Long Record"] in line and wellstat == WellStatus.ACTIVE:
        fout2.write(','.join(map(str, uid.split() + line.split(',')[1:3])) + "," + res_name.strip() + "\n")
    # add uid to monthly production record
    if codes["Monthly Production"] in line and len(uid) > 0 and wellstat == WellStatus.ACTIVE:
        # temp -- line.split(",")[0] ==
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




