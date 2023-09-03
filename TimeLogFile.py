from datetime import datetime
from pathlib import Path
import csv
import logging

from TimeEntryAggregator import TimeEntry, TimeLogState


logger = logging.getLogger('TimeLogFile')


class TimeLogFile:
    def __init__(self, logFile: Path) -> None:
        self.logFile = logFile

    def addComputerSleepingMarker(self, dataList: list[list[str]]) -> list[list[str]]:

        dataListWithSleep = []

        for x in range(len(dataList) - 1):
            currentTimeObject = datetime.strptime(dataList[x][0], '%m/%d/%Y-%H:%M')
            nextTimeObject = datetime.strptime(dataList[x + 1][0], '%m/%d/%Y-%H:%M')

            delta = nextTimeObject - currentTimeObject

            # Append corrent line
            dataListWithSleep.append(dataList[x])

            # if needed append also sleep
            if delta.total_seconds() > (6 * 60):
                # Sleep detected
                dataListWithSleep.append([dataList[x][0], "sleep"])
                # dataListWithSleep.append([dataList[x + 1][0], "sleep"])

        # finally add last line
        dataListWithSleep.append(dataList[-1])

        return dataListWithSleep

    def evaluateTimeLogTable(self, dataList: list[list[str]]) -> list[TimeEntry]:

        state = TimeLogState.RUNNING
        stateBeforeSleep = TimeLogState.UNDEF

        timeFrame = []
        timeEntryList = []

        dataListWithSleep = self.addComputerSleepingMarker(dataList)

        for row in dataListWithSleep:

            currentTimeObject = datetime.strptime(row[0], '%m/%d/%Y-%H:%M')
            currentIdentifier = row[1]

            if state == TimeLogState.RUNNING:
                if currentIdentifier == 'lock':
                    # print(f'Lock: {timeFrame[0]} - {currentTimeObject}')

                    timeFrame.append(currentTimeObject)
                    timeEntryList.append(TimeEntry(timeFrame, state))

                    # Start new timeFrame
                    timeFrame = []
                    timeFrame.append(currentTimeObject)

                    state = TimeLogState.LOCKED

                elif currentIdentifier == 'unlock':
                    logging.warning(f'Double-Unlock detected by {currentTimeObject}')

                    # Add anyway the timeframe and stay in mode running
                    timeFrame.append(currentTimeObject)

                elif currentIdentifier == 'tick':

                    # Ticking. Add current line
                    timeFrame.append(currentTimeObject)

                elif currentIdentifier == 'sleep':

                    timeFrame.append(currentTimeObject)
                    timeEntryList.append(TimeEntry(timeFrame, state))

                    # Start new timeFrame
                    timeFrame = []
                    timeFrame.append(currentTimeObject)

                    stateBeforeSleep = state
                    state = TimeLogState.SLEEP

            elif state == TimeLogState.LOCKED:
                if currentIdentifier == 'lock':
                    logging.warning(f'Double-Lock detected by {currentTimeObject}')

                    # Add anyway the timeframe and stay in mode locked
                    timeFrame.append(currentTimeObject)

                elif currentIdentifier == 'unlock':

                    timeFrame.append(currentTimeObject)
                    timeEntryList.append(TimeEntry(timeFrame, state))

                    # Start new timeFrame
                    timeFrame = []
                    timeFrame.append(currentTimeObject)

                    state = TimeLogState.RUNNING

                elif currentIdentifier == 'tick':

                    # Ticking. Add current line
                    timeFrame.append(currentTimeObject)

                elif currentIdentifier == 'sleep':

                    timeFrame.append(currentTimeObject)
                    timeEntryList.append(TimeEntry(timeFrame, state))

                    # Start new timeFrame
                    timeFrame = []
                    timeFrame.append(currentTimeObject)
                    stateBeforeSleep = state
                    state = TimeLogState.SLEEP

            elif state == TimeLogState.SLEEP:
                timeFrame.append(currentTimeObject)
                timeEntryList.append(TimeEntry(timeFrame, state))

                # Start new timeFrame
                timeFrame = []
                timeFrame.append(currentTimeObject)

                state = TimeLogState.RUNNING

        return timeEntryList

    def readTimeLogFile(self) -> list[TimeEntry]:

        with open(self.logFile, mode='r', encoding='utf-16') as csvfile:
            timeReader = csv.reader(csvfile, delimiter=';')

            # Convert CSV data into a list of dictionaries
            data_list = [row for row in timeReader]

        return self.evaluateTimeLogTable(data_list)

    def detectComputerSleeping(self, currentTimeObject: datetime, timeFrame: list[datetime]) -> bool:
        """
        Detect if computer felt into sleep state.

        Parameters:
        currentTimeObject (datetime): The current time object to check against the last time frame.
        timeFrame (list[datetime]): The list of datetime objects representing the time frame.

        Returns:
        bool: True if a time gap is detected, False otherwise.
        """

        # Initialize the time gap detection flag as False
        disTimeGap = False

        # Check if the time frame is not empty
        if len(timeFrame) > 0:
            # Calculate the time difference between the current time object and the last time frame
            delta = currentTimeObject - timeFrame[-1]

            # A time gap is detected if the time difference is more than 6 minutes
            disTimeGap = delta.total_seconds() > (6 * 60)

        # Return whether a time gap is detected or not
        return disTimeGap
