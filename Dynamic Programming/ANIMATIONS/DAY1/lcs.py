import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LCS Animation")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GREY = (169, 169, 169)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 149, 237)

font = pygame.font.SysFont("comicsans", 30)

text1 = "ABAABA"
text2 = "BABBAB"

index_i, index_j = 1, 1
animation_speed = 1500
last_update_time = pygame.time.get_ticks()
paused = False

m, n = len(text1), len(text2)
dp = [[0] * (n + 1) for _ in range(m + 1)]
all_lcs = set()
is_animation_complete = False


def reset_animation():
    global index_i, index_j, dp, is_animation_complete, all_lcs, paused
    index_i, index_j = 1, 1
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    all_lcs.clear()
    is_animation_complete = False
    paused = False


def draw_strings():
    start_x, start_y = 200, 50
    box_size = 50
    for i, char in enumerate(text1):
        color = ORANGE if i + 1 == index_i else ORANGE
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(
                start_x - box_size, start_y + (i + 2) * box_size, box_size, box_size
            ),
        )
        text = font.render(char, True, BLACK)
        screen.blit(text, (start_x - box_size + 10, start_y + (i + 2) * box_size + 10))

    for j, char in enumerate(text2):
        color = YELLOW if j + 1 == index_j else RED
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(start_x + (j + 2) * box_size, start_y, box_size, box_size),
        )
        text = font.render(char, True, BLACK)
        screen.blit(text, (start_x + (j + 2) * box_size + 10, start_y + 10))


def draw_table():
    start_x, start_y = 200, 100
    box_size = 50
    for i in range(m + 1):
        for j in range(n + 1):
            if i == index_i and j == index_j:
                color = GREEN if text1[i - 1] == text2[j - 1] else PURPLE
            else:
                color = GREY
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(
                    start_x + (j + 1) * box_size,
                    start_y + i * box_size,
                    box_size,
                    box_size,
                ),
            )
            value = dp[i][j]
            text = font.render(str(value), True, BLACK)
            screen.blit(
                text, (start_x + (j + 1) * box_size + 10, start_y + i * box_size + 10)
            )


def update_table():
    global index_i, index_j, is_animation_complete
    if index_i > m:
        if not is_animation_complete:
            print_all_lcs(m, n, "")
            is_animation_complete = True
        return

    if index_j > n:
        index_i += 1
        index_j = 1
        return

    if text1[index_i - 1] == text2[index_j - 1]:
        dp[index_i][index_j] = dp[index_i - 1][index_j - 1] + 1
    else:
        dp[index_i][index_j] = max(dp[index_i - 1][index_j], dp[index_i][index_j - 1])

    index_j += 1


def backtrack_lcs(i, j, current_lcs):
    if i == 0 or j == 0:
        all_lcs.add(current_lcs[::-1])
        return
    if text1[i - 1] == text2[j - 1]:
        backtrack_lcs(i - 1, j - 1, current_lcs + text1[i - 1])
    else:
        if dp[i - 1][j] >= dp[i][j - 1]:
            backtrack_lcs(i - 1, j, current_lcs)
        if dp[i][j - 1] >= dp[i - 1][j]:
            backtrack_lcs(i, j - 1, current_lcs)


def print_all_lcs(i, j, current_lcs):
    backtrack_lcs(i, j, current_lcs)
    print("All LCS:")
    for lcs in all_lcs:
        print(lcs)


def display_lcs():
    lcs_text = "LCS: " + ", ".join(all_lcs)
    text = font.render(lcs_text, True, WHITE)
    screen.blit(text, (100, 600))


def draw_button(text, rect, hover):
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=20)
    pygame.draw.rect(screen, WHITE, rect, 3, border_radius=20)
    button_text = font.render(text, True, WHITE)
    text_rect = button_text.get_rect(center=rect.center)
    screen.blit(button_text, text_rect)


def draw_buttons():
    restart_button_rect = pygame.Rect(720, 50, 160, 60)
    pause_button_rect = pygame.Rect(720, 130, 160, 60)
    speed_up_button_rect = pygame.Rect(720, 210, 160, 60)
    speed_down_button_rect = pygame.Rect(720, 290, 160, 60)
    return (
        restart_button_rect,
        pause_button_rect,
        speed_up_button_rect,
        speed_down_button_rect,
    )


def main():
    global last_update_time, paused, animation_speed
    running = True
    while running:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (
                    restart_button_rect,
                    pause_button_rect,
                    speed_up_button_rect,
                    speed_down_button_rect,
                ) = draw_buttons()
                if restart_button_rect.collidepoint(event.pos):
                    reset_animation()
                elif pause_button_rect.collidepoint(event.pos):
                    paused = not paused
                elif speed_up_button_rect.collidepoint(event.pos):
                    animation_speed = max(500, animation_speed - 500)
                elif speed_down_button_rect.collidepoint(event.pos):
                    animation_speed += 500

        draw_strings()
        draw_table()

        (
            restart_button_rect,
            pause_button_rect,
            speed_up_button_rect,
            speed_down_button_rect,
        ) = draw_buttons()
        draw_button(
            "Restart", restart_button_rect, restart_button_rect.collidepoint(mouse_pos)
        )
        draw_button(
            "Pause" if not paused else "Resume",
            pause_button_rect,
            pause_button_rect.collidepoint(mouse_pos),
        )
        draw_button(
            "Speed Up",
            speed_up_button_rect,
            speed_up_button_rect.collidepoint(mouse_pos),
        )
        draw_button(
            "Slow Down",
            speed_down_button_rect,
            speed_down_button_rect.collidepoint(mouse_pos),
        )

        if not paused:
            current_time = pygame.time.get_ticks()
            if current_time - last_update_time > animation_speed:
                update_table()
                last_update_time = current_time

        if is_animation_complete:
            display_lcs()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
