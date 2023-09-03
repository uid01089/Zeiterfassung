from TimeEntryAggregator import TimeLogState
from TimeLogFile import TimeLogFile


def test_readTimeLogFile1() -> None:
    '''
    Test if the csv-file is read correctly
    '''

    timeLogFile = TimeLogFile('data_test_heartbeat1.txt')
    timeentryList = timeLogFile.readTimeLogFile()

    assert len(timeentryList) == 16

    assert timeentryList[0].timeLogState == TimeLogState.RUNNING
    assert timeentryList[1].timeLogState == TimeLogState.LOCKED
    assert timeentryList[2].timeLogState == TimeLogState.RUNNING
    assert timeentryList[3].timeLogState == TimeLogState.LOCKED
    assert timeentryList[4].timeLogState == TimeLogState.RUNNING
    assert timeentryList[5].timeLogState == TimeLogState.LOCKED
    assert timeentryList[6].timeLogState == TimeLogState.RUNNING
    assert timeentryList[7].timeLogState == TimeLogState.LOCKED
    assert timeentryList[8].timeLogState == TimeLogState.RUNNING
    assert timeentryList[9].timeLogState == TimeLogState.LOCKED
    assert timeentryList[10].timeLogState == TimeLogState.RUNNING
    assert timeentryList[11].timeLogState == TimeLogState.LOCKED
    assert timeentryList[12].timeLogState == TimeLogState.RUNNING
    assert timeentryList[13].timeLogState == TimeLogState.LOCKED
    assert timeentryList[14].timeLogState == TimeLogState.LOCKED
    assert timeentryList[15].timeLogState == TimeLogState.RUNNING


def test_readTimeLogFile2() -> None:
    '''
    Test if the csv-file is read correctly, especially with Computer sleep detection
    '''

    timeLogFile = TimeLogFile('data_test_heartbeat2.txt')
    timeentryList = timeLogFile.readTimeLogFile()

    assert len(timeentryList) == 9
    assert timeentryList[0].timeLogState == TimeLogState.RUNNING
    assert timeentryList[1].timeLogState == TimeLogState.LOCKED
    assert timeentryList[2].timeLogState == TimeLogState.RUNNING
    assert timeentryList[3].timeLogState == TimeLogState.LOCKED
    assert timeentryList[4].timeLogState == TimeLogState.RUNNING
    assert timeentryList[5].timeLogState == TimeLogState.LOCKED
    assert timeentryList[6].timeLogState == TimeLogState.RUNNING
    assert timeentryList[7].timeLogState == TimeLogState.RUNNING
    assert timeentryList[8].timeLogState == TimeLogState.RUNNING
