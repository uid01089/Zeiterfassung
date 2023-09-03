from TimeEntryAggregator import TimeEntryAggregator, TimeLogState
from TimeLogFile import TimeLogFile


def test_markShortBreakes() -> None:
    '''
    Test if the csv-file is read correctly
    '''
    timeEntryAggregator = TimeEntryAggregator()
    timeLogFile = TimeLogFile('data_test_heartbeat1.txt')
    timeentryList = timeLogFile.readTimeLogFile()
    compressedList = timeEntryAggregator.markShortBreakes(timeentryList)

    assert len(compressedList) == 16

    assert compressedList[0].timeLogState == TimeLogState.RUNNING
    assert compressedList[1].timeLogState == TimeLogState.SKIPPED_LOCK
    assert compressedList[2].timeLogState == TimeLogState.RUNNING
    assert compressedList[3].timeLogState == TimeLogState.SKIPPED_LOCK
    assert compressedList[4].timeLogState == TimeLogState.RUNNING
    assert compressedList[5].timeLogState == TimeLogState.SKIPPED_LOCK
    assert compressedList[6].timeLogState == TimeLogState.RUNNING
    assert compressedList[7].timeLogState == TimeLogState.SKIPPED_LOCK
    assert compressedList[8].timeLogState == TimeLogState.RUNNING
    assert compressedList[9].timeLogState == TimeLogState.LOCKED
    assert compressedList[10].timeLogState == TimeLogState.RUNNING
    assert compressedList[11].timeLogState == TimeLogState.LOCKED
    assert compressedList[12].timeLogState == TimeLogState.RUNNING
    assert compressedList[13].timeLogState == TimeLogState.LOCKED
    assert compressedList[14].timeLogState == TimeLogState.SKIPPED_LOCK
    assert compressedList[15].timeLogState == TimeLogState.RUNNING
