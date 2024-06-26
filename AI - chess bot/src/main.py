import pygame
import sys
from const import *
from game import Game
from square import Square
from move import Move
from board import Board
class Main:

  def __init__(self):
    pygame.init
    pygame.mixer.init()
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
      game.show_last_move(screen)
      game.show_moves(screen)
      game.show_pieces(screen)
      game.show_hover(screen)

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
            
            if piece.color == game.next_player:
              board.calc_moves(piece, clicked_row, clicked_col, bool = True)
              dragger.save_initial(event.pos)
              dragger.drag_piece(piece)
              game.show_bg(screen)
              game.show_moves(screen) 
              game.show_pieces(screen)
             
        #moving selected piece with the mouse
        elif event.type == pygame.MOUSEMOTION:
          motion_row = event.pos[1] // SQSIZE
          motion_col = event.pos[0] // SQSIZE

          game.set_hover(motion_row, motion_col)

          if dragger.dragging:
            dragger.update_mouse(event.pos)
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)
            dragger.update_blit(screen)

        #releasing the piece at a given square
        elif event.type == pygame.MOUSEBUTTONUP:
          if dragger.dragging:
            dragger.update_mouse(event.pos)

            released_row = dragger.mouseY // SQSIZE
            released_col = dragger.mouseX // SQSIZE

            initial = Square(dragger.initial_row, dragger.initial_col)
            final = Square(released_row, released_col)
            move = Move(initial, final)

            if board.valid_move(dragger.piece, move):
              capture = board.squares[released_row][released_col].has_piece()
              
              board.move(dragger.piece, move)

              game.sound_effect(capture)

              game.show_bg(screen)
              game.show_last_move(screen)
              game.show_pieces(screen)

              game.next_turn()
          
          dragger.undrag_piece()


        elif event.type == pygame.KEYDOWN:

          if event.key == pygame.K_c:
            game.change_theme()
        
          if event.key == pygame.K_r:
            game.reset_game()
            game = self.game
            dragger = self.game.dragger
            board = self.game.board

        #quit game
        elif event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()


      pygame.display.update()

main = Main()
main.mainloop()