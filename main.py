# import pygame
from board import Board

if __name__ == '__main__':
  # pygame.init()
  # pygame.display.set_mode((160, 144))
  # pygame.display.set_caption('gb-em')
  
  gameboy = Board('roms/07.gb')

  # while gameboy.cpu.regs.pc != 0x100:
  #   gameboy.step()
  
  while True:
    gameboy.step()