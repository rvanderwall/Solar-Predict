__author__ = 'robertv'

import numpy as np

class SubmissionFile:
    file_name = ""

    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, station_list, data):
        date_list = data[:,0]
        station_data = data[:,1:]
        file_content = ""
        header = "Date"
        for station in station_list:
            header += "," + station
        file_content += header

        rowIndex = 0
        for date in date_list:
            rowData = '\n' + str(int(date))
            stationID = 0
            for station in station_list:
                rowData += "," + str(station_data[rowIndex, stationID])
                stationID += 1
            file_content += rowData
            rowIndex += 1

        with open(self.file_name, 'w') as submission_file:
            submission_file.write(file_content)

