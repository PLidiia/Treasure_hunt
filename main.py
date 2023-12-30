import pygame

from Constants import *
from Entrance import Enter


if __name__ == "__main__":
    entry = Enter()
    entry.append_block_menu('Имя')
    entry.append_block_menu('Пароль')
    entry.append_block_menu('Настройки')
    entry.run()