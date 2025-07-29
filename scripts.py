import sys
import os
import re
from enum import StrEnum

import uvicorn
from dotenv import load_dotenv
import importlib


class CommandEnum(StrEnum):
    ENV_FILE = ".env"
    CONFIG_FILE = "[.yml|.yaml]"
    MAIN_FILE = ".py"


def _parse_command_line() -> dict[str, str]:
    command_line = " ".join(sys.argv)
    available_commands = "|".join(
        [fr"({element.name}=(?P<{element.name.lower()}>[^\s]+{element.value}))" for element in CommandEnum]
    )
    commands = re.finditer(available_commands, command_line)
    result = {}
    for command in commands:
        result.update({key: value for key, value in command.groupdict().items() if value is not None})
    return result


def run_project() -> None:
    commands = _parse_command_line()
    main_file = commands.get(CommandEnum.MAIN_FILE.name.lower())
    config_file = commands.get(CommandEnum.CONFIG_FILE.name.lower())

    if config_file:
        os.environ[f"{CommandEnum.CONFIG_FILE.name}"] = config_file

    module = main_file if main_file else "src.main"
    module = module.replace(str(CommandEnum.MAIN_FILE.value), "").replace("/", ".")

    load_dotenv(dotenv_path=commands.get(CommandEnum.ENV_FILE.name.lower(), ".env"))
    src = importlib.import_module(module)

    from src.core.settings.settings import settings
    uvicorn.run(app=src.app, port=settings.MAIN.PORT)
