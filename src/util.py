import csv

from models.lead import Lead

from constants import FILE_PATH


def lead_iterator():
    with open(FILE_PATH, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield Lead(
                name=row["Name"],
                email=row["Email"],
                company=row["Company"],
                job_title=row["Job Title"],
                industry=row["Industry"],
            )
