import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Longest Increasing Subsequence Animation")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GREY = (169, 169, 169)
DARK_GREY = (105, 105, 105)

font = pygame.font.SysFont("comicsans", 30)
button_font = pygame.font.SysFont("comicsans", 25)

# Sample input array
nums = [9, 2, 5, 3, 7, 11, 8, 10, 19, 6]

# Variables for animation
index_i = 1
index_j = 0
animation_speed = 1000
last_update_time = pygame.time.get_ticks()
is_paused = False

dp = [1] * len(nums)
prev = [-1] * len(nums)  # Previous indices
dp_table = []


def reset_animation():
    global index_i, index_j, dp, prev, dp_table
    index_i = 1
    index_j = 0
    dp[:] = [1] * len(nums)  # Reset dp to all 1s
    prev[:] = [-1] * len(nums)  # Reset prev to -1
    dp_table.clear()


def draw_array():
    array_x, array_y = 50, 50
    box_size = 50
    for i, num in enumerate(nums):
        # Highlight elements in LIS in orange
        color = ORANGE if i in get_lis_indices() else BLUE if i == index_i else WHITE
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(array_x + i * (box_size + 10), array_y, box_size, box_size),
        )
        text = font.render(str(num), True, BLACK)
        screen.blit(text, (array_x + i * (box_size + 10) + 10, array_y + 10))


def draw_table():
    headers = ["Index", "Num", "LIS Length", "Prev", "Results"]
    start_x, start_y = 50, 150
    cell_height = 40

    column_widths = [font.size(header)[0] + 20 for header in headers]

    for i, header in enumerate(headers):
        pygame.draw.rect(
            screen, GREY, pygame.Rect(start_x, start_y, column_widths[i], cell_height)
        )
        text = font.render(header, True, BLACK)
        screen.blit(text, (start_x + 5, start_y + 5))
        start_x += column_widths[i]

    for row_idx in range(len(nums)):
        start_x = 50
        for col_idx in range(len(headers)):
            if col_idx == 1:  # Num column
                color = ORANGE if row_idx in get_lis_indices() else WHITE
            else:
                color = WHITE

            item = (
                row_idx,
                nums[row_idx],
                dp[row_idx],
                prev[row_idx],
                get_results(row_idx),
            )[col_idx]
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(
                    start_x,
                    start_y + (row_idx + 1) * cell_height,
                    column_widths[col_idx],
                    cell_height,
                ),
            )
            text = font.render(str(item), True, BLACK)
            screen.blit(text, (start_x + 5, start_y + (row_idx + 1) * cell_height + 5))
            start_x += column_widths[col_idx]


def get_lis_indices():
    lis_indices = []
    max_length = max(dp)
    current_index = dp.index(max_length)
    while current_index != -1:
        lis_indices.append(current_index)
        current_index = prev[current_index]
    return lis_indices[::-1]  # Reverse to get the correct order


def get_results(row_idx):
    if prev[row_idx] == -1:
        return "[]"
    return f"[{nums[prev[row_idx]]}]"


def draw_pause_button():
    pause_color = GREEN if not is_paused else RED
    pygame.draw.rect(
        screen, pause_color, pygame.Rect(WIDTH - 150, HEIGHT - 100, 120, 50)
    )
    text = button_font.render("Pause" if not is_paused else "Resume", True, BLACK)
    screen.blit(text, (WIDTH - 135, HEIGHT - 90))


def draw_restart_button():
    pygame.draw.rect(screen, DARK_GREY, pygame.Rect(WIDTH - 300, HEIGHT - 100, 120, 50))
    text = button_font.render("Restart", True, WHITE)
    screen.blit(text, (WIDTH - 285, HEIGHT - 90))


def update_dp_table():
    global dp, prev, index_i, index_j
    if index_i >= len(nums):
        return
    if index_j < index_i:
        if nums[index_j] < nums[index_i]:
            if dp[index_i] < dp[index_j] + 1:
                dp[index_i] = dp[index_j] + 1
                prev[index_i] = index_j  # Update the previous index
        index_j += 1
    else:
        dp_table.append([index_i, nums[index_i], dp[index_i], prev[index_i]])
        index_i += 1
        index_j = 0


def main():
    global last_update_time, is_paused
    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (
                    WIDTH - 150 <= mouse_x <= WIDTH - 30
                    and HEIGHT - 100 <= mouse_y <= HEIGHT - 50
                ):
                    is_paused = not is_paused
                if (
                    WIDTH - 300 <= mouse_x <= WIDTH - 180
                    and HEIGHT - 100 <= mouse_y <= HEIGHT - 50
                ):
                    reset_animation()
        draw_array()
        draw_table()
        draw_pause_button()
        draw_restart_button()
        if not is_paused:
            current_time = pygame.time.get_ticks()
            if current_time - last_update_time > animation_speed:
                update_dp_table()
                last_update_time = current_time
        pygame.display.flip()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
