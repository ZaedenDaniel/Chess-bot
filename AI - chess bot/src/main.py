import pygame
import sys
from const import *
from game import *

class Main:

  def __init__(self):
    pygame.init
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess")
    self.game = Game()


  def mainloop(self):
    screen = self.screen
    game = self.game
    dragger = self.game.dragger
    board = self.game.board

    while True:
      game.show_bg(screen)
      game.show_moves(screen)
      game.show_pieces(screen)

      if dragger.dragging:
        dragger.update_blit(screen)
       
      for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
          dragger.update_mouse(event.pos)

          clicked_row = dragger.mouseY // SQSIZE
          clicked_col = dragger.mouseX // SQSIZE
          #incase piece exists at the clicked square
          if board.squares[clicked_row][clicked_col].has_piece():
            piece = board.squares[clicked_row][clicked_col].piece
            board.calc_moves(piece, clicked_row, clicked_col)
            dragger.save_initial(event.pos)
            dragger.drag_piece(piece)
            game.show_bg(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
        
        #moving selected piece with the mouse
        elif event.type == pygame.MOUSEMOTION:
          if dragger.dragging:
            dragger.update_mouse(event.pos)
            game.show_bg(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            dragger.update_blit(screen)
        #releasing the piece at a given square
        elif event.type == pygame.MOUSEBUTTONUP:
          dragger.undrag_piece()
        
        #quit game
        elif event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
      pygame.display.update()

main = Main()
main.mainloop()