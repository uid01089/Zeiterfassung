from __future__ import annotations
from datetime import datetime, timedelta
from enum import Enum
import logging

MIN_TIME_TIMEGAP_MINUTES_LOCK = 20
MIN_TIME_TIMEGAP_MINUTES_RUNNING = 2
MIN_SLEEPING_MINUTES = 6

logger = logging.getLogger('TimeEntryAggregator')


class TimeLogState(Enum):
    UNDEF = 0
    RUNNING = 1
    LOCKED = 2
    SKIPPED_LOCK = 3
    SKIPPED_RUNNING = 4
    SLEEP = 5


class TimeEntry:
    def __init__(self, timeStamps: list[datetime], timeLogState: TimeLogState) -> None:
        self.timeStamps = timeStamps
        self.timeLogState = timeLogState

    def add(self, timeEntry: TimeEntry):
        self.timeStamps = self.timeStamps + timeEntry.getTimeStamps()

    def getStart(self) -> datetime:
        return self.timeStamps[0]

    def getEnd(self) -> datetime:
        return self.timeStamps[-1]

    def getTimeStamps(self) -> list[datetime]:
        return self.timeStamps

    def getTimeLogState(self) -> str:
        return self.timeLogState

    def setTimeLogState(self, timeLogState: TimeLogState) -> None:
        self.timeLogState = timeLogState

    def getDurationInSec(self) -> int:
        duration = self.getEnd() - self.getStart()
        return duration.total_seconds()

    def getDuration(self) -> timedelta:
        return self.getEnd() - self.getStart()


class TimeEntryAggregator:
    def __init__(self) -> None:
        pass

    def markShortBreakes(self, timeEntries: list[TimeEntry]) -> list[TimeEntry]:
        for timeEntry in timeEntries:
            duration = timeEntry.getDurationInSec()
            if timeEntry.getTimeLogState() == TimeLogState.LOCKED and duration < (MIN_TIME_TIMEGAP_MINUTES_LOCK * 60):
                timeEntry.setTimeLogState(TimeLogState.SKIPPED_LOCK)
            elif timeEntry.getTimeLogState() == TimeLogState.RUNNING and duration < (MIN_TIME_TIMEGAP_MINUTES_RUNNING * 60):
                timeEntry.setTimeLogState(TimeLogState.SKIPPED_RUNNING)

        return timeEntries

    def printTimeEntries(self, timeEntries: list[TimeEntry]) -> None:
        dayOld = -1
        for timeEntry in timeEntries:
            start = timeEntry.getStart()
            end = timeEntry.getEnd()
            durationInSec = timeEntry.getDurationInSec()
            type = timeEntry.getTimeLogState()

            if start.day != dayOld:
                dayOld = start.day
                print("------------------------------------------------------")

            print(f'{start} - {end} - {type} - {durationInSec}')
