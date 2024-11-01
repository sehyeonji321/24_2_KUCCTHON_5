import pygame
import random
import math

# 초기 설정
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("무한 우주 먼지 수집 바운스볼")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# 폰트 설정
font = pygame.font.Font(None, 36)

# 게임 변수
clock = pygame.time.Clock()
score = 0
scroll_speed = 2  # 맵 스크롤 초기 속도
max_scroll_speed = 10  # 스크롤 최대 속도
speed_increase_interval = 5000  # 속도 증가 간격 (밀리초)

# 바운스볼 설정
ball_radius = 20
ball_speed = 8  # 기존 5에서 8로 속도 증가
ball_pos = [WIDTH // 2, HEIGHT // 2]

# 장애물 이미지 로드 및 설정
rock_image = pygame.image.load("rock_obstacle.png")  # 투명 배경의 PNG 이미지 로드
rock_image = pygame.transform.scale(rock_image, (40, 40))  # 이미지 크기 조정
rock_angle = 0  # 회전 각도

# 장애물 리스트 (이미지와 위치 정보를 함께 저장)
obstacles = [{"rect": pygame.Rect(random.randint(0, WIDTH), random.randint(-HEIGHT, 0), 40, 40), "angle": 0} for _ in range(5)]

# 먼지 생성 함수
def create_dust():
    x = random.randint(0, WIDTH)
    y = random.randint(-HEIGHT, 0)
    return pygame.Rect(x, y, 8, 8)

# 먼지 리스트
dusts = [create_dust() for _ in range(10)]

# 바운스 함수
def move_ball(keys):
    if keys[pygame.K_w]: ball_pos[1] -= ball_speed
    if keys[pygame.K_s]: ball_pos[1] += ball_speed
    if keys[pygame.K_a]: ball_pos[0] -= ball_speed
    if keys[pygame.K_d]: ball_pos[0] += ball_speed

# 충돌 체크 함수
def check_collisions():
    global score
    for dust in dusts[:]:
        if math.hypot(ball_pos[0] - dust.x, ball_pos[1] - dust.y) < ball_radius:
            score += 10
            dusts.remove(dust)
            dusts.append(create_dust())

    for obstacle in obstacles:
        obstacle_rect = obstacle["rect"]
        if math.hypot(ball_pos[0] - obstacle_rect.x, ball_pos[1] - obstacle_rect.y) < ball_radius + 20:
            return True
    return False

# 메인 게임 루프
running = True
game_over = False
while running:
    screen.fill(BLACK)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if retry_button.collidepoint(mouse_pos):
                score = 0
                scroll_speed = 2
                obstacles = [{"rect": pygame.Rect(random.randint(0, WIDTH), random.randint(-HEIGHT, 0), 40, 40), "angle": 0} for _ in range(5)]
                dusts = [create_dust() for _ in range(10)]
                ball_pos = [WIDTH // 2, HEIGHT // 2]
                game_over = False

    if not game_over:
        # 시간 경과에 따라 스크롤 속도 증가
        if current_time % speed_increase_interval < 50:
            scroll_speed = min(scroll_speed + 1, max_scroll_speed)

        # 이동 및 충돌 체크
        keys = pygame.key.get_pressed()
        move_ball(keys)
        if check_collisions():
            game_over = True

        # 먼지 이동
        for dust in dusts:
            dust.y += scroll_speed
            if dust.y > HEIGHT:
                dusts.remove(dust)
                dusts.append(create_dust())

        # 장애물 이동 및 회전
        for obstacle in obstacles:
            obstacle["rect"].y += scroll_speed
            obstacle["angle"] += 5  # 각 장애물이 회전하도록 각도 증가
            if obstacle["rect"].y > HEIGHT:
                obstacle["rect"].y = random.randint(-HEIGHT, 0)
                obstacle["rect"].x = random.randint(0, WIDTH)

            # 회전된 이미지 그리기
            rotated_image = pygame.transform.rotate(rock_image, obstacle["angle"])
            new_rect = rotated_image.get_rect(center=obstacle["rect"].center)
            screen.blit(rotated_image, new_rect.topleft)

        # 먼지와 바운스볼 그리기
        for dust in dusts:
            pygame.draw.rect(screen, WHITE, dust)
        pygame.draw.circle(screen, YELLOW, (int(ball_pos[0]), int(ball_pos[1])), int(ball_radius))

        # 텍스트 표시
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    else:
        screen.fill(BLACK)
        end_text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
        screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - 30))
        retry_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 40)
        pygame.draw.rect(screen, BLUE, retry_button)
        retry_text = font.render("Retry", True, WHITE)
        screen.blit(retry_text, (retry_button.x + 10, retry_button.y + 5))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
