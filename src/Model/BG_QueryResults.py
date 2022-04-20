from lxml import etree
from src.Model.BG_Report import BG_Report


class BG_QueryResults:
    def __init__(self):
        self.results : list[BG_Report] = []
        self.elResults = etree.Element("results")

    def addReportToResultSet(self, report: BG_Report):
        self.results.append(report)

    def buildXML(self) -> str:
        for report in self.results:
            elReport = etree.Element("result")

            lstName = ["Classification", "SN", "Title", "Date", "ProductID", "URL"]
            lstPredicate = [BG_Report.getClassification, BG_Report.getSerialNumber, BG_Report.getTitle, BG_Report.getDate, BG_Report.getProductID, BG_Report.getURL]
            for i in range(0, 6):
                elReportColumnName = etree.Element("name")
                elReportColumnName.text = lstName[i]

                elReportColumnValue = etree.Element("value")
                elReportColumnValue.text = (lstPredicate[i])(report)

                elReportColumn = etree.Element("column")
                elReportColumn.append(elReportColumnName)
                elReportColumn.append(elReportColumnValue)

                elReport.append(elReportColumn)

            self.elResults.append(elReport)

        return etree.tostring(self.elResults)

    def buildSimpleHTML(self) -> str:
        res = ""
        for report in self.results:
            res += "<tr>\n"
            res += '\t<td width="40%">' + report.getTitle() + '</td>'
            res += '\t<td width="10%">' + report.getDate() + '</td>'
            res += '\t<td width="40%">' + report.getURL() + '</td>'
            res += '\t<td width="10%"><a href="' + report.getURL() + '">Click here! </a></td>'
            res += '\t<td width="10%"><a href=https://blowgun.bianisoft.com/downloadPDF?url=' + report.getURL() + '">Click here! </a></td>'
            res += "</tr>\n"

        return res

    def __str__(self) -> str:
        return str(etree.tostring(self.elResults))[2:-1]
