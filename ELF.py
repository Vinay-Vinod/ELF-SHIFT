import csv
 
# opening the CSV file
with open('shifts.csv', mode ='r') as file:    
        # reading the CSV file
        csvFile = csv.DictReader(file)
        # displaying the contents of the CSV file
        #for lines in csvFile:
            #print(lines)
        name_shifts = {}
        for line in csvFile:
            name_shifts[line['NAME']] = []
            for item in line:
                if line[item] == "TRUE":
                    name_shifts[line['NAME']].append(item)
with open('exclusion.csv', mode ='r') as file:    
        # reading the CSV file
        csvFile = csv.reader(file)
        # displaying the contents of the CSV file
        #for lines in csvFile:
            #print(lines)
        shiftedLastTime = []
        for line in csvFile:
            shiftedLastTime += line
with open('availableTimes.csv', mode ='r') as file:    
        # reading the CSV file
        csvFile = csv.DictReader(file)
        # displaying the contents of the CSV file
        #for lines in csvFile:
            #print(lines)
        name_availableTimes = {}
        for line in csvFile:
            name_availableTimes[line['NAME']] = []
            for item in line:
                if line[item] == "TRUE":
                    name_availableTimes[line['NAME']].append(float(item))
#print(name_availableTimes)
#print(shiftedLastTime)
#print(name_shifts)

startTime = 4.50

times_shifts = {startTime: ['Cage Oversight 1', 'Cage Transport 1', 'Cage Transport 2', 'Cage Transport 3'],
                startTime + 0.50: ['Stage Setup', 'Registration Setup', 'Tech Setup', 'Utility 1'],
                startTime + 1: ['Tech Setup', 'Registration Check In 1', 'Registration Check In 2', 'Registration Check In 3', 'Utility 1'],
                startTime + 1.50: ['Late Registration Check In 1', 'Late Registration Check In 2', 'Tech Oversight', 'Photographer', 'Social Media', 'Utility 1', 'Utility 2'],
                startTime + 2: ['Late Registration Check In 3', 'Late Registration Check In 4', 'Tech Oversight', 'Photographer', 'Social Media', 'Utility 1', 'Utility 2'],
                startTime + 2.50: ['Cage Oversight 1', 'Cage Transport 1', 'Cage Transport 2', 'Cage Transport 3']
                }

shifts_times = {'Cage Oversight 1' : [startTime],
                'Cage Transport 1' : [startTime],
                'Cage Transport 2' : [startTime],
                'Cage Transport 3' : [startTime],
                'Stage Setup' : [startTime + 0.50],
                'Registration Setup' : [startTime + 0.50],
                'Tech Setup' : [startTime + 0.50, startTime + 1],
                'Registration Check In 1': [startTime + 1],
                'Registration Check In 2': [startTime + 1],
                'Registration Check In 3': [startTime + 1],
                'Late Registration Check In 1': [startTime + 1.5],
                'Late Registration Check In 2': [startTime + 1.5],
                'Late Registration Check In 3': [startTime + 2],
                'Late Registration Check In 4': [startTime + 2],
                'Tech Oversight': [startTime + 1.5, startTime + 2],
                'Photographer': [startTime + 1.5, startTime + 2],
                'Social Media': [startTime + 1.5, startTime + 2],
                'Utility 1' : [startTime + 0.50, startTime + 1, startTime + 1.5, startTime + 2],
                'Utility 2': [startTime + 1.5, startTime + 2],
                'Cage Oversight 2': [startTime + 2.5],
                'Cage Transport 4': [startTime + 2.5],
                'Cage Transport 5': [startTime + 2.5],
                'Cage Transport 6': [startTime + 2.5],
}
#print(sortedShiftsNums)
#this is the creation of the dictionary that will contain each shift and each person that can do each shift
shifts_listOfPeople = {}              
#this is the scanner that will pull the list of people for each shift   
for person in name_availableTimes:
     for shift in name_shifts[person]:
          if not all(x in name_availableTimes[person] for x in shifts_times[shift]):
               name_shifts[person].remove(shift)
#print(name_shifts)
for person in name_shifts:
    listOfPeople = []
    for shift in name_shifts[person]:
        if shift not in shifts_listOfPeople:
            shifts_listOfPeople[shift] = []
        shifts_listOfPeople[shift].append(person)
shifts_nums = {}
for shift in shifts_listOfPeople:
    shifts_nums[shift] = len(shifts_listOfPeople[shift])
print(shifts_nums)
sortedShiftsNums = dict(sorted(shifts_nums.items(), key=lambda x:x[1]))
print('\n')
print(sortedShiftsNums)
    #listOfPeople = ["j", "s", "p"]
    #this inputs the people into each shift and what they can do
    #for shift in sortedShiftsNums:
        #for person in listOfPeople:
            #shifts_listOfPeople[shift] = listOfPeople
exclusionList = []

returnList = {}
#print(shifts_listOfPeople)

for shift in sortedShiftsNums:
    saved = ""
    for person in shifts_listOfPeople[shift]:
        if person not in shiftedLastTime and person not in exclusionList:
            saved = person
            exclusionList.append(person)
            break
    returnList[shift] = saved

exclusionList2 = []
for shift in returnList:
    saved = ""
    if returnList[shift] == '':
        for person in shifts_listOfPeople[shift]:
            if person not in exclusionList2 and person not in exclusionList:
                saved = person
                exclusionList2.append(person)
                break
        returnList[shift] = saved
                    
#print(shifts_listOfPeople)
#print("\n")

print(returnList)

