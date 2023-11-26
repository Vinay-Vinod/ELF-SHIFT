import csv
import random


def process_shifts(shifts_path, exclusion_path, available_times_path):
    """
    Main function to process shifts. Reads shift preferences, exclusion list,
    and available times from provided CSV files, and assigns shifts accordingly.

    Args:
    shifts_path (str): Path to the CSV file containing shift preferences.
    exclusion_path (str): Path to the CSV file containing names of people who should be excluded.
    available_times_path (str): Path to the CSV file containing available times of people.

    Returns:
    dict: A dictionary with shifts as keys and assigned person names as values.
    """
    name_shifts = read_shifts(shifts_path)
    shiftedLastTime = read_exclusion(exclusion_path)
    name_availableTimes = read_available_times(available_times_path)

    shifts_times = define_shifts_times()
    sortedShiftsNums = sort_shifts_by_availability(
        name_shifts, name_availableTimes, shifts_times
    )
    exclusionList = set(shiftedLastTime)

    returnList = assign_shifts(
        name_shifts, name_availableTimes, shifts_times, sortedShiftsNums, exclusionList
    )

    return returnList


def read_shifts(shifts_path):
    """
    Reads the shifts CSV file and creates a dictionary mapping each person to their preferred shifts.

    Args:
    shifts_path (str): Path to the CSV file containing shift preferences.

    Returns:
    dict: A dictionary where keys are person names and values are lists of preferred shifts.
    """
    with open(shifts_path, mode="r") as file:
        return {
            line["NAME"]: [item for item in line if line[item] == "TRUE"]
            for line in csv.DictReader(file)
        }


def read_exclusion(exclusion_path):
    """
    Reads a CSV file containing a list of people who are excluded from being assigned to shifts.

    Args:
    exclusion_path (str): Path to the CSV file containing the exclusion list.

    Returns:
    set: A set of names of people who should not be assigned to any shifts.
    """

    with open(exclusion_path, mode="r") as file:
        return set(item for sublist in csv.reader(file) for item in sublist)


def read_available_times(available_times_path):
    """
    Reads the available times CSV file and creates a dictionary mapping each person to their available times.

    Args:
    available_times_path (str): Path to the CSV file containing available times of people.

    Returns:
    dict: A dictionary where keys are person names and values are lists of times when they are available.
    """

    with open(available_times_path, mode="r") as file:
        return {
            line["NAME"]: [float(item) for item in line if line[item] == "TRUE"]
            for line in csv.DictReader(file)
        }


def define_shifts_times():
    """
    Defines the start times for each shift.

    Returns:
    dict: A dictionary with shift names as keys and lists of start times as values.
    """

    startTime = 4.50

    shifts_times = {
        "Cage Oversight 1": [startTime],
        "Cage Transport 1": [startTime],
        "Cage Transport 2": [startTime],
        "Cage Transport 3": [startTime],
        "Stage Setup": [startTime + 0.50],
        "Registration Setup": [startTime + 0.50],
        "Tech Setup": [startTime + 0.50, startTime + 1],
        "Registration Check In 1": [startTime + 1],
        "Registration Check In 2": [startTime + 1],
        "Registration Check In 3": [startTime + 1],
        "Late Registration Check In 1": [startTime + 1.5],
        "Late Registration Check In 2": [startTime + 1.5],
        "Late Registration Check In 3": [startTime + 2],
        "Late Registration Check In 4": [startTime + 2],
        "Tech Oversight": [startTime + 1.5, startTime + 2],
        "Photographer": [startTime + 1.5, startTime + 2],
        "Social Media": [startTime + 1.5, startTime + 2],
        "Utility 1": [startTime + 0.50, startTime + 1, startTime + 1.5, startTime + 2],
        "Utility 2": [startTime + 1.5, startTime + 2],
        "Cage Oversight 2": [startTime + 2.5],
        "Cage Transport 4": [startTime + 2.5],
        "Cage Transport 5": [startTime + 2.5],
        "Cage Transport 6": [startTime + 2.5],
    }

    return shifts_times


def sort_shifts_by_availability(name_shifts, name_availableTimes, shifts_times):
    """
    Sorts shifts based on the number of available people for each shift.

    Args:
    name_shifts (dict): A dictionary mapping each person to their preferred shifts.
    name_availableTimes (dict): A dictionary mapping each person to their available times.
    shifts_times (dict): A dictionary mapping each shift to its corresponding times.

    Returns:
    dict: A dictionary of shifts sorted by the number of available people, with shifts as keys.
    """
    shifts_nums = {}
    for shift in shifts_times:
        shifts_nums[shift] = sum(
            person in name_shifts
            and any(time in name_availableTimes[person] for time in shifts_times[shift])
            for person in name_shifts
        )
    return dict(sorted(shifts_nums.items(), key=lambda x: x[1]))


def assign_shifts(
    name_shifts, name_availableTimes, shifts_times, sortedShiftsNums, exclusionList
):
    """
    Assigns shifts to people based on their availability, preferences, and exclusion list.

    Args:
    name_shifts (dict): A dictionary mapping each person to their preferred shifts.
    name_availableTimes (dict): A dictionary mapping each person to their available times.
    shifts_times (dict): A dictionary mapping each shift to its corresponding times.
    sortedShiftsNums (dict): A dictionary of sorted shifts based on availability.
    exclusionList (set): A set of names of people who should not be assigned to any shifts.

    Returns:
    dict: A dictionary with shifts as keys and assigned person names as values.
    """
    returnList = {shift: "" for shift in shifts_times}
    for shift in sortedShiftsNums:
        candidates = {
            person
            for person in name_shifts
            if person not in exclusionList
            and any(time in name_availableTimes[person] for time in shifts_times[shift])
        }
        if candidates:
            selected = random.choice(list(candidates))
            returnList[shift] = selected
            exclusionList.add(selected)
    return returnList


if __name__ == "__main__":
    """
    Tests function with example file paths
    """

    shifts = "elfAPP/test_files/test1.csv"
    exclusion = "elfAPP/test_files/test1Exclusion.csv"
    available_times = "elfAPP/test_files/test1AvailableTimes.csv"
    result = process_shifts(shifts, exclusion, available_times)
    for shift, person in result.items():
        print(f"Shift: {shift}, Assigned Person: {person}")
