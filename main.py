import core.engine as engine
from tests.games.pong.pong import Pong


def main() -> None:

    appState = Pong()

    engine.init(appState)
    engine.run()


if __name__ == "__main__":
    main()
    pass
