from dataclasses import dataclass


@dataclass
class Lead:
    name: str
    email: str
    company: str
    job_title: str
    industry: str
