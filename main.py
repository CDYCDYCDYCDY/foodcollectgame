import pygame
import sys
from game_config import *
from game_utils import draw_sky, draw_ground, draw_world_elements
from ui_manager import UIManager
from game_state import GameState
from items import ItemManager  # 导入道具管理器

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("接粮食小游戏")
        self.clock = pygame.time.Clock()
        self.running = True

        # 初始化模块
        self.state = GameState()
        self.state.player.game_state = self.state
        self.ui = UIManager(self.screen)
        self.item_manager = ItemManager(screen_height=SCREEN_HEIGHT)  # 创建道具管理器实例

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.ui.handle_click(pygame.mouse.get_pos(), self.state):
                    self.running = False
        

    def run(self):
        while self.running:
            # 事件处理
            self.handle_events()
            
            # 获取鼠标位置并更新按钮悬停状态
            mouse_pos = pygame.mouse.get_pos()
            self.ui.buttons['pause'].check_hover(mouse_pos)
            self.ui.buttons['restart'].check_hover(mouse_pos)
            
            # 游戏状态更新
            self.state.update()
            # 仅在游戏未暂停且未结束时更新道具
            if not self.state.is_paused and not self.state.game_over:
                self.item_manager.update(self.state.player)  # 更新道具状态和碰撞检测
            
            # 绘制逻辑（严格按照从下到上的层级顺序）
            draw_sky(self.screen)               # 1. 天空
            draw_world_elements(self.screen, self.state.grain_bin_rect)  # 2. 世界元素
            self.item_manager.draw(self.screen)  # 3. 道具
            draw_ground(self.screen)             # 4. 地面（覆盖道具）
            self.state.player.draw(self.screen)  # 5. 玩家
            self.ui.draw_all(self.state)         # 6. UI元素
            
            # 刷新屏幕
            pygame.display.flip()
            
            # 控制帧率
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()