import logging
import csv
import io

class CsvFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.output = io.StringIO()
        self.writer = csv.writer(self.output, quoting=csv.QUOTE_ALL)

    def format(self, record):
        self.writer.writerow(record.msg.split(","))
        data = self.output.getvalue()
        self.output.truncate(0)
        self.output.seek(0)
        return data.strip()

logging.basicConfig(level=logging.DEBUG, filename="hallolog.csv")

logger = logging.getLogger(__name__)
logging.root.handlers[0].setFormatter(CsvFormatter())