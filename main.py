import pygame
from ui import draw_menu, draw_setup_screen, draw_game_screen, draw_game_over
from game_logic import GameLogic

def main():
    pygame.init()
    game_logic = GameLogic()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            game_logic.handle_events(event)
        
        game_logic.update()
        
        # Draw screen based on game state
        if game_logic.game_state == game_logic.STATE_MENU:
            draw_menu(game_logic)
        elif game_logic.game_state == game_logic.STATE_PLAYER_SETUP:
            draw_setup_screen(game_logic)
        elif game_logic.game_state in [game_logic.STATE_PLAYER_SHOOTING, game_logic.STATE_AI_SHOOTING]:
            draw_game_screen(game_logic)
        elif game_logic.game_state == game_logic.STATE_GAME_OVER:
            draw_game_over(game_logic)
        
        pygame.display.flip()
        game_logic.clock.tick(game_logic.FPS)
    
    game_logic.save_q_table()
    pygame.quit()

if __name__ == "__main__":
    main()
