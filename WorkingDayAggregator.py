from datetime import datetime, timedelta
from TimeEntryAggregator import TimeEntry, TimeLogState


class WorkingDay:
    def __init__(self) -> None:
        self.state = TimeLogState.UNDEF
        self.timeEntries = []

    def addTimeEntry(self, timeEntry: TimeEntry) -> None:

        if self.state == TimeLogState.UNDEF:

            # we have to wait till running event
            if timeEntry.getTimeLogState() == TimeLogState.RUNNING:
                self.timeEntries.append(timeEntry)
                self.state = TimeLogState.RUNNING

        elif self.state == TimeLogState.RUNNING:
            if (timeEntry.getTimeLogState() == TimeLogState.RUNNING
                    or timeEntry.getTimeLogState() == TimeLogState.SKIPPED_LOCK):

                # If EndTime of last timeEntry equal to StartTime of current Time, then murge it
                if self.timeEntries[-1].getEnd() == timeEntry.getStart():
                    self.timeEntries[-1].add(timeEntry)
                else:
                    self.timeEntries.append(timeEntry)

            elif timeEntry.getTimeLogState() == TimeLogState.LOCKED:
                self.state = TimeLogState.LOCKED

        if self.state == TimeLogState.LOCKED:

            # we have to wait till running event
            if timeEntry.getTimeLogState() == TimeLogState.RUNNING:
                self.timeEntries.append(timeEntry)
                self.state = TimeLogState.RUNNING

    def getStart(self) -> datetime:
        return self.timeEntries[0].getStart()

    def getEnd(self) -> datetime:
        return self.timeEntries[-1].getEnd()

    def getDuration(self) -> timedelta:

        duration = timedelta()

        for timeEntry in self.timeEntries:
            duration = duration + timeEntry.getDuration()

        return duration

    def print(self) -> None:
        if len(self.timeEntries) > 0:
            print("-----------------------------------------------------------")
            print(f'{self.getStart()} - {self.getEnd()} - Bürozeit: {self.getEnd() - self.getStart()} - Arbeitszeit: {self.getDuration()}')
            for timeEntry in self.timeEntries:
                print(f'{timeEntry.getStart().time()} - {timeEntry.getEnd().time()} - {timeEntry.getTimeLogState()} - {timeEntry.getDuration()}')


class WorkingDayAggregator:
    def __init__(self) -> None:
        pass

    def createWorkingDays(self, timeEntries: list[TimeEntry]) -> list[WorkingDay]:
        dayOld = -1
        workingDays = []
        workingday = None
        for timeEntry in timeEntries:

            # Create new WorkingDay and add it to collection
            dayOfYear = timeEntry.getStart().timetuple().tm_yday
            if dayOfYear != dayOld:
                dayOld = dayOfYear
                workingday = WorkingDay()
                workingDays.append(workingday)

            # Add timeEntry to working day
            workingday.addTimeEntry(timeEntry)

        return workingDays
