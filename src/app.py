from loguru import logger
import typer


def main():
    logger.debug(f"Hello")


if __name__ == "__main__":
    typer.run(main)
