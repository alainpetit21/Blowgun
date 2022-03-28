import hashlib
import os
import os.path
import sqlite3

from src.CCC.SingletonDecorator import SingletonDecorator
from src.Model.BG_QueryResults import BG_QueryResults
from src.Model.BG_Report import BG_Report


@SingletonDecorator
class BG_Report_Repository:
    def __init__(self):
        if not (os.path.isfile('./data/blowgun.db')):
            connForerunner = sqlite3.connect('./data/blowgun.db')
            cursor = connForerunner.cursor()

            cursor.execute("CREATE TABLE Report (classification TEXT, url TEXT, title TEXT, date TEXT, hash TEXT);")
            connForerunner.commit()
            connForerunner.close()

    def exist(self, objReport: BG_Report) -> bool:
        hashStr = objReport.getProductID()

        connection = sqlite3.connect('./data/blowgun.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Report WHERE hash = '" + hashStr + "'")
        lstRows = cursor.fetchall()

        return len(lstRows) > 0

    def save(self, objReport: BG_Report):
        objReport.strTitle = objReport.strTitle.replace('"', '\"')
        objReport.strTitle = objReport.strTitle.replace("'", "\'")
        objReport.strReportText = objReport.strReportText.replace('"', '\"')
        objReport.strReportText = objReport.strReportText.replace("'", "\'")
        strCommand = 'REPLACE INTO Report (classification, url, title, date, hash) ' \
                     'VALUES (' \
                     '"' + objReport.getClassification() + '", ' \
                     '"' + objReport.getURL() + '", ' \
                     '"' + objReport.getTitle() + '", ' \
                     '"' + objReport.getDate() + '", ' \
                     '"' + objReport.getProductID() + '");'

        connection = sqlite3.connect('./data/blowgun.db')
        cursor = connection.cursor()
        cursor.execute(strCommand)
        connection.commit()
        connection.close()

    def searchInTitle(self, searchTerm: str) -> BG_QueryResults:
        connection = sqlite3.connect('./data/blowgun.db')
        cursor = connection.cursor()
        sqlCommand = 'SELECT * FROM Report WHERE title LIKE "%' + searchTerm + '%"'
        cursor.execute(sqlCommand)
        lstRows = cursor.fetchall()

        objQueryResults = BG_QueryResults()
        for row in lstRows:
            objReport = BG_Report()
            objReport.setClassification(row[0])
            objReport.setURL(row[1])
            objReport.setTitle(row[2])
            objReport.setDate(row[3])
            objReport.setProductID(row[4])
            objQueryResults.addReportToResultSet(objReport)

        objQueryResults.buildXML()
        return objQueryResults
