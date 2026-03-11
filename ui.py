import pygame

def draw_menu(game_logic):
    screen = game_logic.screen
    screen.fill((200, 200, 255))  # Light blue background
    font = pygame.font.SysFont(None, 64)
    title = font.render("Stickman Shootout", True, game_logic.BLACK)
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))
    
    font = pygame.font.SysFont(None, 36)
    instructions = font.render("Click to Start Game", True, game_logic.BLACK)
    screen.blit(instructions, (screen.get_width() // 2 - instructions.get_width() // 2, 250))
    
    # Draw game rules
    font = pygame.font.SysFont(None, 24)
    rules = [
        "Game Rules:",
        "1. Place enemies and bombs on the grid",
        "2. Shoot enemies while avoiding bombs",
        "3. If you shoot a bomb, you lose",
        "4. The AI will learn from your patterns",
        "5. Win by shooting all enemies"
    ]
    
    for i, rule in enumerate(rules):
        rule_text = font.render(rule, True, game_logic.BLACK)
        screen.blit(rule_text, (screen.get_width() // 2 - rule_text.get_width() // 2, 350 + i * 30))

def draw_setup_screen(game_logic):
    screen = game_logic.screen
    screen.fill(game_logic.WHITE)
    
    # Draw grid
    for col in range(game_logic.GRID_COLS):
        for row in range(game_logic.GRID_ROWS):
            rect = pygame.Rect(
                col * game_logic.GRID_CELL_WIDTH, 
                game_logic.GRID_TOP_MARGIN + row * game_logic.GRID_CELL_HEIGHT, 
                game_logic.GRID_CELL_WIDTH, 
                game_logic.GRID_CELL_HEIGHT
            )
            pygame.draw.rect(screen, game_logic.GRAY, rect, 1)
    
    # Draw placed objects
    for obj in game_logic.setup_objects:
        x, y, obj_type = obj
        if obj_type == 0:  # Enemy
            screen.blit(game_logic.enemy_img, (x - game_logic.enemy_img.get_width() // 2, y - game_logic.enemy_img.get_height() // 2))
        else:  # Bomb
            screen.blit(game_logic.bomb_img, (x - game_logic.bomb_img.get_width() // 2, y - game_logic.bomb_img.get_height() // 2))
    
    # Draw remaining count
    font = pygame.font.SysFont(None, 32)
    enemy_text = font.render(f"Enemies: {game_logic.remaining_enemies}", True, game_logic.BLACK)
    bomb_text = font.render(f"Bombs: {game_logic.remaining_bombs}", True, game_logic.BLACK)
    screen.blit(enemy_text, (20, 20))
    screen.blit(bomb_text, (20, 60))
    
    # Draw selected type
    selection_text = font.render(f"Selected: {'Enemy' if game_logic.setup_selected_type == 0 else 'Bomb'}", True, game_logic.BLACK)
    screen.blit(selection_text, (screen.get_width() - selection_text.get_width() - 20, 20))
    
    # Draw instructions
    if game_logic.remaining_enemies == 0 and game_logic.remaining_bombs == 0:
        ready_text = font.render("Click to start game", True, game_logic.GREEN)
        screen.blit(ready_text, (screen.get_width() // 2 - ready_text.get_width() // 2, game_logic.HEIGHT - 50))
    else:
        instruction = font.render("Place all enemies and bombs on the grid", True, game_logic.BLACK)
        screen.blit(instruction, (screen.get_width() // 2 - instruction.get_width() // 2, game_logic.HEIGHT - 50))
        
    # Draw selection buttons
    enemy_button = pygame.Rect(game_logic.WIDTH - 200, 60, 80, 30)
    bomb_button = pygame.Rect(game_logic.WIDTH - 100, 60, 80, 30)
    
    pygame.draw.rect(screen, game_logic.RED if game_logic.setup_selected_type == 0 else game_logic.GRAY, enemy_button)
    pygame.draw.rect(screen, game_logic.BLACK if game_logic.setup_selected_type == 1 else game_logic.GRAY, bomb_button)
    
    button_font = pygame.font.SysFont(None, 24)
    enemy_label = button_font.render("Enemy", True, game_logic.WHITE)
    bomb_label = button_font.render("Bomb", True, game_logic.WHITE)
    
    screen.blit(enemy_label, (enemy_button.x + enemy_button.width // 2 - enemy_label.get_width() // 2, 
                            enemy_button.y + enemy_button.height // 2 - enemy_label.get_height() // 2))
    screen.blit(bomb_label, (bomb_button.x + bomb_button.width // 2 - bomb_label.get_width() // 2, 
                           bomb_button.y + bomb_button.height // 2 - bomb_label.get_height() // 2))

def draw_game_screen(game_logic):
    screen = game_logic.screen
    screen.fill(game_logic.WHITE)
    
    # Draw grid
    for col in range(game_logic.GRID_COLS):
        for row in range(game_logic.GRID_ROWS):
            rect = pygame.Rect(
                col * game_logic.GRID_CELL_WIDTH, 
                game_logic.GRID_TOP_MARGIN + row * game_logic.GRID_CELL_HEIGHT, 
                game_logic.GRID_CELL_WIDTH, 
                game_logic.GRID_CELL_HEIGHT
            )
            pygame.draw.rect(screen, game_logic.GRAY, rect, 1)
    
    # Draw enemies
    for enemy in game_logic.enemies:
        x, y, visible = enemy
        if visible:  # Only draw if visible
            screen.blit(game_logic.enemy_img, (x - game_logic.enemy_img.get_width() // 2, y - game_logic.enemy_img.get_height() // 2))
    
    # Draw bombs
    for bomb in game_logic.bombs:
        x, y, visible = bomb
        if visible:  # Only draw if visible
            screen.blit(game_logic.bomb_img, (x - game_logic.bomb_img.get_width() // 2, y - game_logic.bomb_img.get_height() // 2))
    
    # Draw player
    screen.blit(game_logic.stickman_img, (game_logic.player_pos[0] - game_logic.stickman_img.get_width() // 2, game_logic.player_pos[1] - game_logic.stickman_img.get_height() // 2))
    
    # Draw shots
    for shot in game_logic.shots:
        x, y, _, _ = shot
        pygame.draw.circle(screen, game_logic.BLUE, (int(x), int(y)), 5)
    
    # Draw AI shots
    for shot in game_logic.ai_shots:
        x, y, _, _ = shot
        pygame.draw.circle(screen, game_logic.RED, (int(x), int(y)), 5)
    
    # Draw explosions
    for exp in game_logic.explosions:
        x, y, _ = exp
        screen.blit(game_logic.explosion_img, (x - game_logic.explosion_img.get_width() // 2, y - game_logic.explosion_img.get_height() // 2))
    
    # Draw scores
    font = pygame.font.SysFont(None, 32)
    player_text = font.render(f"Player: {game_logic.player_score}", True, game_logic.BLUE)
    ai_text = font.render(f"AI: {game_logic.ai_score}", True, game_logic.RED)
    screen.blit(player_text, (20, 20))
    screen.blit(ai_text, (game_logic.WIDTH - ai_text.get_width() - 20, 20))
    
    # Draw current state
    state_text = font.render(f"{'Player Turn' if game_logic.game_state == game_logic.STATE_PLAYER_SHOOTING else 'AI Turn'}", True, game_logic.BLACK)
    screen.blit(state_text, (screen.get_width() // 2 - state_text.get_width() // 2, 20))

def draw_game_over(game_logic):
    screen = game_logic.screen
    screen.fill(game_logic.WHITE)
    font = pygame.font.SysFont(None, 64)
    title = font.render("Game Over", True, game_logic.BLACK)
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 100))
    
    font = pygame.font.SysFont(None, 48)
    result = font.render(game_logic.game_over_message, True, game_logic.BLACK)
    screen.blit(result, (screen.get_width() // 2 - result.get_width() // 2, 200))
    
    font = pygame.font.SysFont(None, 36)
    scores = font.render(f"Player: {game_logic.player_score}  AI: {game_logic.ai_score}", True, game_logic.BLACK)
    screen.blit(scores, (screen.get_width() // 2 - scores.get_width() // 2, 300))
    
    font = pygame.font.SysFont(None, 32)
    restart = font.render("Click to Play Again", True, game_logic.BLACK)
    screen.blit(restart, (screen.get_width() // 2 - restart.get_width() // 2, 400))
