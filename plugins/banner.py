import os
from colorama import Fore
import colorama

colorama.init()


def print_banner():
    banner = Fore.LIGHTRED_EX + f"""
                                                                           
                                ╭━━━╮╭╮╱╱╱╱╱╱╭╮╭╮╭╮╱╱ ╭━━━╮
                                ┃╭━╮┣╯╰╮╱╱╱╱╱┃┣╯╰┫┃╱╱ ┃╭━╮┃
                                ┃╰━━╋╮╭╋━━┳━━┫┣╮╭┫╰━╮ ┃╰━━┳━━┳━┳━━┳━━┳━━╮
                                ╰━━╮┃┃┃┃┃━┫╭╮┃┃┃┃┃╭╮┃ ╰━━╮┃╭━┫╭┫╭╮┃╭╮┃┃━┫
                                ┃╰━╯┃┃╰┫┃━┫╭╮┃╰┫╰┫┃┃┃ ┃╰━╯┃╰━┫┃┃╭╮┃╰╯┃┃━┫
                                ╰━━━╯╰━┻━━┻╯╰┻━┻━┻╯╰╯ ╰━━━┻━━┻╯╰╯╰┫╭━┻━━╯
                                ╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱ ╱╱╱╱╱╱╱╱╱╱╱╱┃┃
                                ╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱ ╱╱╱╱╱╱╱╱╱╱╱╱╰╯
                                {Fore.RESET}
                                    By JustXploit
                                    In Github: @CanXplot
                                                                           
"""

    print(banner)