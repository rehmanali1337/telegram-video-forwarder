
import time
import os
from logging.handlers import RotatingFileHandler
import logging
import colorama
from consolemenu import PromptUtils, Screen
from app import metadata
from typing import Optional, Tuple


colorama.init(autoreset=True)


max_filesize_in_mbs = 20
log_filename = "logs.log"
file_encoding = "UTF-8"

logging_format = logging.Formatter("%(levelname)s:[%(filename)s:%(lineno)s]:%(asctime)s: %(message)s")
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging_format)
file_handler = RotatingFileHandler(
    log_filename,
    mode="a",
    maxBytes=max_filesize_in_mbs * 1024 * 1024,
    backupCount=2,
    encoding=file_encoding,
    delay=False,
)
file_handler.setFormatter(logging_format)

logger.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)
console_handler.setLevel(logging.DEBUG)

# logger.addHandler(console_handler)
logger.addHandler(file_handler)


class Console:
    prompt = PromptUtils(Screen())

    DEFAULT_CLOSE_PROMPT = "Press Enter <-"

    @classmethod
    def get_text_input(cls, prompt_text: str, default: Optional[str] = None) -> str:
        return cls.prompt.input(prompt_text, default=default)[0]

    @classmethod
    def get_number_input(cls, prompt_text: str, default: int = 1) -> int:
        while True:
            try:
                return int(cls.get_text_input(prompt_text, default=str(default)))

            except ValueError:
                cls.warn("Please enter a number !!")
                continue

    @classmethod
    def numbered_choices(cls, choices_list: list[str], title: str = "Make a choice") -> str:
        return choices_list[cls.prompt.prompt_for_numbered_choice(choices_list, title=title)]

    @classmethod
    def j_args(cls, *args: str | Tuple[str, ...]) -> str:
        j = [str(arg) for arg in args]
        return " ".join(j)

    @staticmethod
    def _wait_for_shutdown(prompt: str = DEFAULT_CLOSE_PROMPT) -> None:
        input(colorama.Fore.CYAN + colorama.Style.BRIGHT + f"\n[#] {prompt}")

    @staticmethod
    def error(
        *args: str | Tuple[str, ...],
        exc_info: bool = False,
        shutdown: bool = False,
        close_prompt: str = DEFAULT_CLOSE_PROMPT,
    ) -> None:
        message = Console.j_args(*args)
        logger.debug(message, exc_info=exc_info)
        print(colorama.Fore.RED + colorama.Style.BRIGHT + f"[-] {message}")
        if shutdown:
            return Console._wait_for_shutdown(close_prompt)

    @staticmethod
    def processing(
        *args: str, exc_info: bool = False, shutdown: bool = False, close_prompt: str = DEFAULT_CLOSE_PROMPT
    ) -> None:
        message = Console.j_args(*args)
        logger.debug(message, exc_info=exc_info)
        print(colorama.Fore.BLUE + colorama.Style.BRIGHT + f"[...] {message}")
        if shutdown:
            return Console._wait_for_shutdown(close_prompt)

    @staticmethod
    def warn(
        *args: str, exc_info: bool = False, shutdown: bool = False, close_prompt: str = DEFAULT_CLOSE_PROMPT
    ) -> None:
        message = Console.j_args(*args)
        logger.debug(message, exc_info=exc_info)
        print(colorama.Fore.YELLOW + colorama.Style.BRIGHT + f"[*] {message}")
        if shutdown:
            return Console._wait_for_shutdown(close_prompt)

    @staticmethod
    def info(
        *args: str, exc_info: bool = False, shutdown: bool = False, close_prompt: str = DEFAULT_CLOSE_PROMPT
    ) -> None:
        message = Console.j_args(*args)
        logger.debug(message, exc_info=exc_info)
        print(colorama.Fore.GREEN + colorama.Style.BRIGHT + f"[+] {message}")
        if shutdown:
            return Console._wait_for_shutdown(close_prompt)


Console.info("<" + "-" * 50 + ">")
print("\n")
Console.info(f"App Name => {metadata.NAME}")
Console.info(f"Version Number: {metadata.VERSION}")
Console.info(f"Developer Contact => {metadata.CONTACT_INFO}")
print("\n")
Console.info("<" + "-" * 50 + ">")
if not os.environ.get("REHMAN", False):
    time.sleep(3)
