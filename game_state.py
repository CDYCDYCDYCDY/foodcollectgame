import pygame
from game_config import GAME_DURATION, SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_HEIGHT, MAX_WEIGHT, GRAIN_BIN_X, GRAIN_BIN_Y, GRAIN_BIN_WIDTH, GRAIN_BIN_HEIGHT, STORE_DURATIONS, STORE_SCORES
from player import Player

class GameState:
    def __init__(self):
        self.is_paused = False
        self.game_over = False
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time_when_paused = 0
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - GROUND_HEIGHT - 60)
        # 负重系统状态
        self.current_weight = 0
        self.max_weight = MAX_WEIGHT
        # 添加粮仓属性
        self.grain_bin_rect = pygame.Rect(
            GRAIN_BIN_X,
            GRAIN_BIN_Y,
            GRAIN_BIN_WIDTH,
            GRAIN_BIN_HEIGHT
        )
        self.show_store_prompt = False  # 储存提示显示标志
         # 新增储存状态变量
        self.is_storing = False
        self.store_start_time = 0
        self.store_duration = 0
        self.store_paused_time = 0   # 储存过程中的暂停时间
        self.last_store_pause_start = 0  # 最后一次储存暂停开始时间

        # 对话系统相关状态
        self.show_dialog = False
        self.current_dialog_id = ""
        self.dialog_start_time = 0
        self.dialog_duration = 1000  # 对话框显示时间(毫秒)


    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.elapsed_time_when_paused = (pygame.time.get_ticks() - self.start_time) // 1000
        else:
            self.start_time = pygame.time.get_ticks() - (self.elapsed_time_when_paused * 1000)

    def restart(self):
        self.__init__()  # 重置所有状态

    def update(self):
        # 仅在游戏正常运行状态下允许移动
        if not self.is_paused and not self.game_over and not self.is_storing:
            # 移动逻辑 - 受状态控制
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.move(-self.player.speed)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.move(self.player.speed)

            # 添加粮仓碰撞检测
            self.show_store_prompt = self.player.rect.colliderect(self.grain_bin_rect)
            # 添加储存粮食按键检测
            keys = pygame.key.get_pressed()
            if self.show_store_prompt and (keys[pygame.K_s] or keys[pygame.K_DOWN]):
                if self.current_weight == 0:
                    # 显示无法储存的对话
                    self.show_dialog_for_duration("empty_storage", 1000)
                else:
                    # 储存粮食
                    self.store_grain()
        
        if self.is_storing:
            if self.is_paused or self.game_over:
                if not hasattr(self, 'last_store_pause_start') or self.last_store_pause_start == 0:
                    self.last_store_pause_start = pygame.time.get_ticks()
            else:
                if self.last_store_pause_start > 0:
                    # 计算暂停时长并累加到储存暂停时间
                    self.store_paused_time += pygame.time.get_ticks() - self.last_store_pause_start
                    self.last_store_pause_start = 0
        if self.is_storing and not self.is_paused and not self.game_over:
            current_time = pygame.time.get_ticks()
            # 减去储存过程中的暂停时间
            elapsed = (current_time - self.store_start_time - self.store_paused_time) / 1000
            if elapsed >= self.store_duration:
                # 储存完成
                self.is_storing = False
                self.score += STORE_SCORES[self.current_weight]
                self.current_weight = 0
                self.store_paused_time = 0  # 重置储存暂停时间
                self.last_store_pause_start = 0

        # 处理对话框自动关闭
        if self.show_dialog and pygame.time.get_ticks() - self.dialog_start_time > self.dialog_duration:
            self.show_dialog = False

        # 检查游戏结束
        if self.get_remaining_time() <= 0 and not self.is_paused:
            self.game_over = True
        

    def get_remaining_time(self):
        if not self.is_paused:
            elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
            return max(GAME_DURATION - elapsed, 0)
        return max(GAME_DURATION - self.elapsed_time_when_paused, 0)
    
    # 新增：储存粮食的方法
    def store_grain(self):
        if self.is_storing:  # 防止重复触发
            return

        # 从配置文件获取储存参数
        self.store_duration = STORE_DURATIONS[self.current_weight]
        score_increase = STORE_SCORES[self.current_weight]

        # 开始储存
        self.is_storing = True
        self.store_start_time = pygame.time.get_ticks()

    def show_dialog_for_duration(self, dialog_id, duration=1000):
        """显示指定ID的对话框一段时间"""
        self.current_dialog_id = dialog_id
        self.show_dialog = True
        self.dialog_start_time = pygame.time.get_ticks()
        self.dialog_duration = duration