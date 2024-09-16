# Load CSV File and extract data using lead_generator

import csv
from dataclasses import dataclass

FILE_PATH = "media/sample_leads_10.csv"


@dataclass
class Lead:
    # Lead dataclass to store data
    name: str
    email: str
    company: str
    job_title: str
    industry: str

    def str(self):
        return f"""name={self.name}, email={self.email}, 
                company={self.company}, job_title={self.job_title}, 
                industry={self.industry}"""


def lead_generator():
    with open(FILE_PATH, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield Lead(
                name=row["Name"],
                email=row["Email"],
                company=row["Company"],
                job_title=row["Job Title"],
                industry=row["Industry"],
            ).str()


leads = lead_generator()
