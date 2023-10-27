import core.engine as engine
from tests.physics.collision.collision_test import CollisionTest


def main() -> None:

    appState = CollisionTest()

    engine.init(appState)
    engine.run()


if __name__ == "__main__":
    main()
    pass
