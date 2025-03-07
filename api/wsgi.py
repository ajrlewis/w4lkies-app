import sys

sys.path.append("src/")

from loguru import logger

from app import create_app
from config import Config

app = create_app(Config)


def main(host: str = "0.0.0.0", port: int = 5000, debug: bool = True):
    logger.info(f"{host = } {port = } {debug = }")
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    _, host, port = sys.argv
    main(host, port)
