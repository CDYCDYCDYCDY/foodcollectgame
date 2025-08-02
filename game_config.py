# 游戏窗口设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 颜色定义
SKY_COLOR = (135, 206, 235)  # 天蓝色
GROUND_COLOR = (34, 139, 34)  # 地面绿色
GROUND_HEIGHT = 100  # 地面高度
TEXT_COLOR = (255, 255, 255)  # 白色文字
BUTTON_NORMAL = (70, 130, 180)  # 按钮正常颜色
BUTTON_HOVER = (100, 149, 237)   # 按钮悬停颜色

# 倒计时设置
GAME_DURATION = 60  # 游戏总时长（秒）
# 负重系统配置
MAX_WEIGHT = 3      # 最大负重限制

# 新增储存系统配置
STORE_DURATIONS = [0, 0.5, 1.0, 1.5]  # 各负重对应的储存时间(秒)，索引对应负重值
STORE_SCORES = [0, 10, 20, 30]           # 各负重对应的积分，索引对应负重值

# 粮仓配置
GRAIN_BIN_X = 50                # 粮仓X坐标
GRAIN_BIN_Y = SCREEN_HEIGHT - GROUND_HEIGHT - 50  # 粮仓Y坐标
GRAIN_BIN_WIDTH = 60            # 粮仓宽度
GRAIN_BIN_HEIGHT = 50           # 粮仓高度
# 按钮设置
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 20

# 道具系统配置
ITEM_FALL_SPEED_RANGE = (3, 4)  # 道具下落速度范围 (最小值, 最大值)
ITEM_SPAWN_INTERVAL_RANGE = (500, 1000)  # 道具生成间隔范围 (毫秒)
ITEM_SPAWN_X_RANGE = (50, 750)  # 道具生成X轴范围 (左边界, 右边界)

# 新增道具生成概率配置（总和100%）
ITEM_SPAWN_PROBABILITIES = {
    1: 70,   # 1号道具(粮食)概率70%
    2: 15,   # 2号道具(炸弹)概率15%
    3: 5,    # 3号道具(时钟)概率5%
    4: 10    # 4号道具(超级粮食)概率10%
}
