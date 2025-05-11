import pygame
import sys
import os

# Get the directory of the currently executing file
current_directory = os.getcwd()
current_directory = current_directory.replace("\\", "/")

# Init
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ricardo e Bruno - Jogo")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load assets
player1_img = pygame.image.load(f"{current_directory}/src/player1.png").convert_alpha()
player2_img = pygame.image.load(f"{current_directory}/src/player2.png").convert_alpha()
#player1_img = pygame.transform.scale(player1_img, (80, 100)) 
#player2_img = pygame.transform.scale(player2_img, (80, 100))
hit_sound = pygame.mixer.Sound(f"{current_directory}/src/hit.wav")
background_img = pygame.image.load(f"{current_directory}/src/minecraft.png").convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Players
player1 = pygame.Rect(100, HEIGHT//2 - 50, 80, 100)
player2 = pygame.Rect(WIDTH - 180, HEIGHT//2 - 50, 80, 100)

# Game State
balls = []
score1 = 0
score2 = 0
timer = 60
game_over = False

# Timers
pygame.time.set_timer(pygame.USEREVENT, 1000)

# Cooldowns
last_shot1 = 0
last_shot2 = 0
COOLDOWN = 1100  # 1.1 seconds in milliseconds

# Buttons
restart_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 60)

def draw_text(text, size, color, x, y, center=True):
    font_obj = pygame.font.SysFont(None, size)
    text_surf = font_obj.render(text, True, color)
    rect = text_surf.get_rect(center=(x, y) if center else (x, y))
    screen.blit(text_surf, rect)

def reset_game():
    global balls, score1, score2, timer, game_over, last_shot1, last_shot2
    balls = []
    score1 = 0
    score2 = 0
    timer = 60
    game_over = False
    last_shot1 = 0
    last_shot2 = 0

running = True
while running:
    clock.tick(60)
    screen.blit(background_img, (0, 0))
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT and not game_over:
            timer -= 1
            if timer <= 0:
                game_over = True

        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if restart_button.collidepoint(event.pos):
                reset_game()

    keys = pygame.key.get_pressed()
    if not game_over:
        # Player 1 movement (WASD)
        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= 5
        if keys[pygame.K_s] and player1.bottom < HEIGHT:
            player1.y += 5

        # Player 2 movement (Arrow Keys)
        if keys[pygame.K_UP] and player2.top > 0:
            player2.y -= 5
        if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
            player2.y += 5

        # Shoot cooldown
        if keys[pygame.K_SPACE] and current_time - last_shot1 > COOLDOWN:
            balls.append(["left", pygame.Rect(player1.right, player1.centery - 5, 10, 10)])
            last_shot1 = current_time

        if keys[pygame.K_RETURN] and current_time - last_shot2 > COOLDOWN:
            balls.append(["right", pygame.Rect(player2.left - 10, player2.centery - 5, 10, 10)])
            last_shot2 = current_time

        # Ball movement and collision
        for ball in balls[:]:
            if ball[0] == "left":
                ball[1].x += 10
                if ball[1].colliderect(player2):
                    balls.remove(ball)
                    score1 += 1
                    hit_sound.play()
            else:
                ball[1].x -= 10
                if ball[1].colliderect(player1):
                    balls.remove(ball)
                    score2 += 1
                    hit_sound.play()

            if ball[1].x < 0 or ball[1].x > WIDTH:
                balls.remove(ball)

    # Draw players
    screen.blit(player1_img, player1)
    screen.blit(player2_img, player2)

    # Draw balls
    for ball in balls:
        pygame.draw.circle(screen, BLACK, ball[1].center, 5)

    # Draw HUD
    draw_text(f"{score1} - {score2}", 48, BLACK, WIDTH // 2, 40)
    draw_text(f"Tempo: {timer}", 36, BLACK, WIDTH // 2, 80)

    if game_over:
        result = "Empatou!"
        if score1 > score2:
            result = "Ricardinho ganhou!"
        elif score2 > score1:
            result = "Bruninho ganhou!"
        draw_text("Jogo acabou!", 64, BLACK, WIDTH // 2, HEIGHT // 2 - 60)
        draw_text(result, 48, BLACK, WIDTH // 2, HEIGHT // 2 - 10)
        pygame.draw.rect(screen, (200, 200, 200), restart_button)
        draw_text("Jogo acabou", 36, BLACK, restart_button.centerx, restart_button.centery)

    pygame.display.flip()

pygame.quit()
sys.exit()