import engine
from tests.engine_dev.app_state_dev import AppStateDev


def main() -> None:

    appState: AppStateDev = AppStateDev()

    engine.init(appState)
    engine.run()


if __name__ == "__main__":
    main()
    pass
