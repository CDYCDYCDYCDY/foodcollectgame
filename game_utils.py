import pygame
from game_config import *

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hover = False
        self.font = pygame.font.SysFont("SimHei", 30)

    def draw(self, screen):
        # 根据悬停状态选择颜色
        color = BUTTON_HOVER if self.hover else BUTTON_NORMAL
        pygame.draw.rect(screen, color, self.rect)

        # 绘制文字
        text_surface = self.font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


def draw_text(screen, text, x, y, font_size=30, color=TEXT_COLOR):
    font = pygame.font.SysFont("SimHei", font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_sky(screen):
    # ====== 预留天空图像导入 ======
    # 未来可替换为图像加载代码
    # sky_image = pygame.image.load("assets/images/sky.png").convert()
    # screen.blit(sky_image, (0, 0))
    # ============================
    
    # 当前使用纯色填充作为过渡
    screen.fill(SKY_COLOR)

def draw_ground(screen):
    # ====== 预留地面图像导入 ======
    # 未来可替换为图像加载代码
    # ground_image = pygame.image.load("assets/images/ground.png").convert()
    # screen.blit(ground_image, (0, SCREEN_HEIGHT - GROUND_HEIGHT))
    # ============================
    
    # 当前使用纯色矩形作为过渡
    pygame.draw.rect(
        screen,
        GROUND_COLOR,
        (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
    )


# 新增：绘制世界元素（粮仓等游戏场景物体）
def draw_world_elements(screen, grain_bin_rect):
    # 绘制粮仓
    # 粮仓主体（棕色矩形）
    pygame.draw.rect(screen, (139, 69, 19), grain_bin_rect)
    # 粮仓屋顶（棕色三角形）
    x, y, width, height = grain_bin_rect
    pygame.draw.polygon(screen, (165, 42, 42), [
        (x, y),
        (x + width, y),
        (x + width // 2, y - height // 4)
    ])