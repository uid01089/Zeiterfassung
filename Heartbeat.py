import logging

from TimeEntryAggregator import TimeEntryAggregator
from TimeLogFile import TimeLogFile
from WorkingDayAggregator import WorkingDayAggregator


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    timeEntryAggregator = TimeEntryAggregator()
    workingDayAggrgator = WorkingDayAggregator()
    timeLogFile = TimeLogFile('heartbeat.txt')
    # timeLogFile = TimeLogFile('data_test_heartbeat3.txt')

    # Read in file
    timeentryList = timeLogFile.readTimeLogFile()

    # preprocess time events
    compressedList = timeEntryAggregator.markShortBreakes(timeentryList)
    timeEntryAggregator.printTimeEntries(compressedList)

    workingDays = workingDayAggrgator.createWorkingDays(compressedList)

    for workingDay in workingDays:
        workingDay.print()


if __name__ == '__main__':
    main()
