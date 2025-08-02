import pygame
from game_config import *
from game_utils import Button, draw_text
from game_state import GameState
from dialog_manager import get_dialog_text

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        # 添加字体初始化
        self.font = pygame.font.Font("assets/fonts/simhei.ttf", 16)
        self.buttons = {
            'pause': Button(SCREEN_WIDTH - BUTTON_WIDTH - BUTTON_MARGIN, BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT, "暂停"),
            'restart': Button(SCREEN_WIDTH - BUTTON_WIDTH - BUTTON_MARGIN, BUTTON_MARGIN*2 + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, "重新开始"),
            'quit': Button(SCREEN_WIDTH//2 - BUTTON_WIDTH - 20, SCREEN_HEIGHT//2 + 50, BUTTON_WIDTH, BUTTON_HEIGHT, "退出游戏"),
            'replay': Button(SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT//2 + 50, BUTTON_WIDTH, BUTTON_HEIGHT, "重新开始")
        }

    def draw_all(self, game_state):
        #根据游戏状态决定按钮字样
        self.buttons['pause'].text = "继续" if game_state.is_paused else "暂停"

         # 绘制粮仓交互提示（包含样式优化）
        if game_state.show_store_prompt:
            # 绘制半透明背景板
            text = "按S或↓储存"
            # 绘制提示文本
            draw_text(
                self.screen,
                text,
                game_state.grain_bin_rect.centerx-40,
                game_state.grain_bin_rect.y-40,
                16
            )

         # 添加跟随人物的对话框
        if hasattr(game_state, 'show_dialog') and game_state.show_dialog:
            # 获取对话文本
            dialog_text = get_dialog_text(game_state.current_dialog_id)
            if dialog_text:
                # 计算文本尺寸
                text_width, text_height = self.font.size(dialog_text)
                
                # 根据文本长度计算对话框尺寸(增加内边距)
                dialog_width = text_width + 20  # 左右各10px内边距
                dialog_height = text_height + 10  # 上下各5px内边距
                
                # 计算对话框位置(人物头顶上方居中)
                dialog_x = game_state.player.x + game_state.player.width//2 - dialog_width//2
                dialog_y = game_state.player.y - dialog_height - 10
                
                # 绘制对话框背景和边框
                pygame.draw.rect(self.screen, (255, 255, 220), (dialog_x, dialog_y, dialog_width, dialog_height))
                pygame.draw.rect(self.screen, (0, 0, 0), (dialog_x, dialog_y, dialog_width, dialog_height), 2)
                
                # 绘制对话文本
                draw_text(
                    self.screen,
                    dialog_text,
                    dialog_x + 10,  # 左内边距
                    dialog_y + 5,   # 上内边距
                    16,
                    (0, 0, 0)  # 文本颜色
                )
        
       

        # 绘制暂停界面
        if game_state.is_paused:
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 128))
            self.screen.blit(s, (0, 0))
            draw_text(self.screen, "游戏已暂停", SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2, 40)

        # 绘制结算界面
        if game_state.game_over:
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            self.screen.blit(s, (0, 0))
            draw_text(self.screen, "游戏结束", SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 - 50, 40)
            draw_text(self.screen, f"最终得分: {game_state.score}", SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2, 30)
            self.buttons['quit'].draw(self.screen)
            self.buttons['replay'].draw(self.screen)

        # 添加中央积分显示
        draw_text(
            self.screen,
            f"积分: {game_state.score}",
            SCREEN_WIDTH // 2,
            20,
            36  # 仅保留font_size参数
        )

        # 添加跟随人物的储存提示或者负重显示
        if game_state.is_storing:
            draw_text(
                self.screen,
                "储存中",
                game_state.player.x-20,
                game_state.player.y + game_state.player.height+10,
                16
            )
        else:
            draw_text(
                self.screen,
                f"当前负重：{game_state.current_weight}/{game_state.max_weight}",
                game_state.player.x-20,
                game_state.player.y + game_state.player.height+10,
                16
            )
        

        # 按钮绘制到最后，确保在所有界面之上
        self.buttons['pause'].draw(self.screen)
        self.buttons['restart'].draw(self.screen)
        # 添加倒计时显示
        draw_text(self.screen, f"剩余时间: {game_state.get_remaining_time()}秒", 20, 20)



    def handle_click(self, mouse_pos, game_state):
        if self.buttons['pause'].is_clicked(mouse_pos):
            game_state.toggle_pause()
        elif self.buttons['restart'].is_clicked(mouse_pos):
            game_state.restart()
        elif game_state.game_over:
            if self.buttons['quit'].is_clicked(mouse_pos):
                return False  # 退出游戏
            elif self.buttons['replay'].is_clicked(mouse_pos):
                game_state.restart()
        return True