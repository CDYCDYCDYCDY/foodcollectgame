import pygame
import random
from game_config import (
    ITEM_FALL_SPEED_RANGE, 
    ITEM_SPAWN_INTERVAL_RANGE, 
    ITEM_SPAWN_X_RANGE,  
    ITEM_SPAWN_PROBABILITIES  # 添加到文件开头的导入中
)

# 道具类型常量 - 便于未来扩展
ITEM_TYPES = {
    'FOOD': 1,        # 1号道具：粮食
    'BOMB': 2,        # 2号道具：炸弹
    'CLOCK': 3,       # 3号道具：时钟
    'SUPER_FOOD': 4   # 4号道具：超级粮食
}

class Item:
    def __init__(self, item_type, x, y):
        # 基础属性
        self.item_type = item_type
        self.x = x
        self.y = y
        self.size = 30  # 道具碰撞体积
        self.speed = random.randint(*ITEM_FALL_SPEED_RANGE)  # 道具下落速度
        self.active = True  # 道具活动状态
        self.spawn_time = pygame.time.get_ticks()  # 生成时间

    def update(self):
        """更新道具状态"""
        # 移动逻辑
        self.y += self.speed
        

    def check_collision(self, player):
        """检测与玩家的碰撞(矩形碰撞检测)"""
        # 检查玩家状态
        if player.state == 'stun' or player.game_state.is_storing:
            return False
        # 创建玩家碰撞矩形
        player_rect = pygame.Rect(
            player.x,
            player.y,
            player.width,
            player.height
        )
        
        # 可选：缩小道具碰撞范围（如80%）以提高判定精度
        item_rect = pygame.Rect(
            self.x - (self.size*0.4),
            self.y - (self.size*0.4),
            self.size*0.8,
            self.size*0.8
        )
        
        return player_rect.colliderect(item_rect)

    def on_collect(self, player):
        """处理道具收集逻辑(基类实现基础功能，子类重写实现具体效果)"""
        self.active = False  # 收集后设置为非活动状态
        

    def draw(self, screen):
        """绘制道具(基类实现默认外观，子类重写实现特定外观)"""
        # 默认绘制一个白色圆形
        pygame.draw.circle(
            screen,
            (255, 255, 255),  # 白色
            (self.x, self.y),
            self.size//2
        )
        # 绘制道具类型标识
        font = pygame.font.Font(None, 16)
        type_text = font.render(str(self.item_type), True, (0, 0, 0))
        text_rect = type_text.get_rect(center=(self.x, self.y))
        screen.blit(type_text, text_rect)

class FoodItem(Item):
    def __init__(self, x, y):
        super().__init__(ITEM_TYPES['FOOD'], x, y)
        self.image = None  # 预留外观导入空间

    def on_collect(self, player):
        super().on_collect(player)
        if player.game_state.current_weight < player.game_state.max_weight:
            player.game_state.current_weight += 1

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x - self.size//2, self.y - self.size//2))
        else:
            pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), self.size//2)
        # 绘制道具类型标识
        font = pygame.font.Font(None, 16)
        type_text = font.render(str(self.item_type), True, (0, 0, 0))
        text_rect = type_text.get_rect(center=(self.x, self.y))
        screen.blit(type_text, text_rect)

class BombItem(Item):
    def __init__(self, x, y):
        super().__init__(ITEM_TYPES['BOMB'], x, y)
        self.image = None  # 预留外观导入空间

    def on_collect(self, player):
        super().on_collect(player)
        # 炸弹特有逻辑待实现

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x - self.size//2, self.y - self.size//2))
        else:
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.size//2)
        # 绘制道具类型标识
        font = pygame.font.Font(None, 16)
        type_text = font.render(str(self.item_type), True, (0, 0, 0))
        text_rect = type_text.get_rect(center=(self.x, self.y))
        screen.blit(type_text, text_rect)

class ClockItem(Item):
    def __init__(self, x, y):
        super().__init__(ITEM_TYPES['CLOCK'], x, y)
        self.image = None  # 预留外观导入空间

    def on_collect(self, player):
        super().on_collect(player)
        # 时钟特有逻辑待实现

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x - self.size//2, self.y - self.size//2))
        else:
            pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), self.size//2)
        # 绘制道具类型标识
        font = pygame.font.Font(None, 16)
        type_text = font.render(str(self.item_type), True, (0, 0, 0))
        text_rect = type_text.get_rect(center=(self.x, self.y))
        screen.blit(type_text, text_rect)

class SuperFoodItem(Item):
    def __init__(self, x, y):
        super().__init__(ITEM_TYPES['SUPER_FOOD'], x, y)
        self.image = None  # 预留外观导入空间

    def on_collect(self, player):
        super().on_collect(player)
        # 超级粮食特有逻辑待实现

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x - self.size//2, self.y - self.size//2))
        else:
            pygame.draw.circle(screen, (128, 0, 128), (self.x, self.y), self.size//2)
        # 绘制道具类型标识
        font = pygame.font.Font(None, 16)
        type_text = font.render(str(self.item_type), True, (0, 0, 0))
        text_rect = type_text.get_rect(center=(self.x, self.y))
        screen.blit(type_text, text_rect)




class ItemManager:
    """道具管理器 - 处理道具生成、更新和生命周期管理"""
    def __init__(self, screen_height=600):
        self.items = []
        self.spawn_timer = 0
        self.screen_height = screen_height
        self.last_spawn_time = pygame.time.get_ticks()
        # 初始化生成间隔
        self._reset_spawn_interval()  # 替换直接赋值
        # 添加属性记录上一个生成的道具类型
        self.last_item_type = None
        # 定义特殊道具类型列表，如果有新的特殊道具或者道具改名，加入这个地方需要更改
        self.special_item_types = [ITEM_TYPES['BOMB'], ITEM_TYPES['CLOCK'], ITEM_TYPES['SUPER_FOOD']]
        # 直接使用文件开头导入的概率配置
        self.item_probabilities = ITEM_SPAWN_PROBABILITIES

    def _reset_spawn_interval(self):
        """重置道具生成间隔（提取重复逻辑为独立方法）"""
        self.spawn_interval = random.randint(*ITEM_SPAWN_INTERVAL_RANGE)

    def update(self, player):
        """更新所有道具状态并处理生成逻辑"""
        current_time = pygame.time.get_ticks()
        self._handle_spawning(current_time)
        self._update_items(player)
        self._cleanup_inactive_items()

    def _handle_spawning(self, current_time):
        """处理道具生成逻辑"""
        if current_time - self.last_spawn_time > self.spawn_interval:
            # 确定道具类型
            if self.last_item_type in self.special_item_types:
                # 如果上一个是特殊道具，则本次强制生成粮食
                item_type = ITEM_TYPES['FOOD']
            else:
                # 否则按照概率选择道具类型
                types = list(self.item_probabilities.keys())
                weights = list(self.item_probabilities.values())
                item_type = random.choices(types, weights=weights, k=1)[0]

            x_pos = random.randint(*ITEM_SPAWN_X_RANGE)

            # 根据类型创建不同的道具实例
            if item_type == ITEM_TYPES['FOOD']:
                new_item = FoodItem(x_pos, 0)
            elif item_type == ITEM_TYPES['BOMB']:
                new_item = BombItem(x_pos, 0)
            elif item_type == ITEM_TYPES['CLOCK']:
                new_item = ClockItem(x_pos, 0)
            elif item_type == ITEM_TYPES['SUPER_FOOD']:
                new_item = SuperFoodItem(x_pos, 0)
            else:
                pass #未来如果引入新的道具类型，这里需要添加对应的逻辑
            
            self.items.append(new_item)
            # 记录本次生成的道具类型
            self.last_item_type = item_type
            # 重置生成计时器和下次生成间隔
            self.last_spawn_time = current_time
            self._reset_spawn_interval()  # 替换直接赋值

    def _update_items(self, player):
        """更新所有道具位置并检测碰撞"""
        for item in self.items:
            if item.active:
                item.update()
                # 检测与玩家碰撞
                if item.check_collision(player):
                    item.on_collect(player)
                # 检测是否落地
                if item.y >= self.screen_height - item.size//2:
                    item.active = False

    def _cleanup_inactive_items(self):
        """移除所有非活动道具"""
        self.items = [item for item in self.items if item.active]

    def draw(self, screen):
        """绘制所有活动道具"""
        for item in self.items:
            if item.active:
                item.draw(screen)
