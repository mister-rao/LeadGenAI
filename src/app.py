from loguru import logger
import typer

from util import lead_iterator


def main():
    for lead in lead_iterator():
        print(lead)


if __name__ == "__main__":
    typer.run(main)
