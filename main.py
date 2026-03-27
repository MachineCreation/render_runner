# -------------------------------------------------------------------------------
# Main
# Joseph Egan
# 2026-03-17
# Sources: None
# -------------------------------------------------------------------------------
# Description: main function

# Local imports
from app.UI.EnvSetup import make_env
from app.UI.render_runner_ui.MainUI import UI
from logs import log_config

# python imports


def MainUI():

    # run terminal UI for environment setup
    # make_env()

    # run terminal UI for main logic
    ui = UI()
    ui.start()

    # delete ui after loop close
    del ui


if __name__ == '__main__':
    MainUI()
