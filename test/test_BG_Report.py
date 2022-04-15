import unittest

from src.Model.BG_Report import BG_Report
from src.Repository.BG_Report_Repository import BG_Report_Repository


class TestBGReport(unittest.TestCase):

    def test_BG_ReportCreationAndSavingWorks(self):
        objReport = BG_Report()
        objReport.title = "test"
        objReport.date_report = "2022/04/12"

        objRepoReport = BG_Report_Repository()
        self.assertFalse(objRepoReport.exists(objReport))

        objRepoReport.save(objReport)
        self.assertTrue(objRepoReport.exists(objReport))

        objRepoReport.delete(objReport)
        self.assertFalse(objRepoReport.exists(objReport))


if __name__ == '__main__':
    unittest.main()