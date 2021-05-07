from board import Board

if __name__ == '__main__':
  gameboy = Board('roms/tetris.gb')

  while True:
    gameboy.step()