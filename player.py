import pygame
from game_config import *

class Player:
    def __init__(self, x, y):
        # 玩家基本属性
        self.width = 40
        self.height = 60
        self.x = x
        self.y = y
        self.speed = 5
        self.direction = 'right'  # 初始方向向右
        self.weight = 0  # 新增：数字负重状态，默认为0
        self.state = 'stop'  # 新增：角色状态（move/stop/stun/unload）
        
        # 创建玩家矩形
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # 新增：人物形象配置字典 - 存储不同方向的形象数据
        self.sprites = {
            'right': {
                'color': (0, 128, 255),
                'eye_position': (self.rect.centerx + 5, self.rect.centery - 10)
            },
            'left': {
                'color': (0, 128, 255),
                'eye_position': (self.rect.centerx - 5, self.rect.centery - 10)
            }
        }

    def draw(self, screen):
        # 根据当前方向获取对应的形象配置
        current_sprite = self.sprites[self.direction]
        
        # 绘制玩家身体
        pygame.draw.rect(screen, current_sprite['color'], self.rect)
        
        # 绘制眼睛（根据方向定位）
        pygame.draw.circle(screen, (255, 255, 255), 
                          (self.rect.centerx + (5 if self.direction == 'right' else -5), 
                           self.rect.centery - 10), 3)

    def change_direction(self, direction):
        # 改变玩家方向
        if direction in ['left', 'right']:
            self.direction = direction
            # 更新眼睛位置
            self.sprites[direction]['eye_position'] = (
                self.rect.centerx + (5 if direction == 'right' else -5),
                self.rect.centery - 10
            )

    def move(self, dx):
        # 移动玩家并更新方向
        self.x += dx
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.rect.x = self.x
        
        # 根据移动方向自动更新朝向
        if dx > 0:
            self.change_direction('right')
        elif dx < 0:
            self.change_direction('left')

    # 新增：获取当前状态的方法，供main.py使用
    def get_current_state(self):
        return {
            'direction': self.direction,
            'position': (self.x, self.y),
            'size': (self.width, self.height)
        }

    # 新增：加载外部形象的方法（为未来素材库功能预留）
    def load_sprite(self, direction, sprite_data):
        if direction in ['left', 'right']:
            self.sprites[direction] = sprite_data
            # 如果当前方向是被加载的方向，立即更新
            if direction == self.direction:
                self.change_direction(direction)

     # 新增：设置负重状态的方法
    def set_weight(self, weight):
        self.weight = weight
        # 负重变化时重新加载形象
        self.load_image()

    # 新增：设置角色状态的方法
    def set_state(self, state):
        if state in ['move', 'stop', 'stun', 'unload']:
            self.state = state
            # 状态变化时重新加载形象
            self.load_image()

    # 修改：加载外部形象的方法
    def load_image(self):
        try:
            # 构建包含数字负重的文件名
            filename = f"{self.direction}_{self.state}_{self.weight}.png"
            # 加载图片
            return pygame.image.load(f"assets/characters/{filename}").convert_alpha()
        except FileNotFoundError:
            # 找不到对应图片时使用默认绘制
            return None