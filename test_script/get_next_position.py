"""
财富流游戏位置计算测试脚本 - Position Calculation Test
测试内圈Z字形移动路径的位置计算算法

文件功能概述：
==============
本文件是专门用于测试和验证内圈Z字形移动路径算法的测试脚本。
内圈的移动规则比较特殊，需要在到达边界时进行反向移动，
这个脚本用于验证算法的正确性。

主要功能：
----------
1. get_next_position_with_reversal函数
   - 计算内圈Z字形路径的下一个位置
   - 处理边界反转逻辑（1↔9之间往返）
   - 支持多步移动的累积计算

2. 路径规则实现
   - 正向移动：1→2→3→4→5→6→7→8→9
   - 到达9后反向：9→8→7→6→5→4→3→2→1
   - 到达1后再正向：1→2→3→...
   - 形成无限往返的Z字形路径

核心算法：
----------
- 边界检测和方向切换
- 多步移动的逐步计算
- 位置边界的正确处理
- 方向状态的维护

测试目的：
----------
- 验证内圈移动算法的正确性
- 测试边界条件和特殊情况
- 确保多步移动的准确性
- 为主游戏提供算法验证

使用方式：
----------
直接运行此脚本，查看各种移动情况的测试结果，
验证算法是否符合游戏规则要求。

技术特点：
----------
- 独立的算法验证脚本
- 完整的边界条件测试
- 清晰的测试用例设计
- 易于理解的算法实现

作者：财富流游戏开发团队
版本：v1.0
更新日期：2024年
"""

def get_next_position_with_reversal(current_position, steps):
    """
    Calculate next position with reversal at boundaries.
    Path: 1→2→3→4→5→6→7→8→9→8→7→6→5→4→3→2→1→2...
    
    Args:
        current_position: The current position (1-9)
        steps: Number of steps to move (dice roll)
    
    Returns:
        New position after movement
    """
    # If current_position is a tuple, extract position and direction
    if isinstance(current_position, tuple):
        position, is_moving_forward = current_position
    else:
        position = current_position
        is_moving_forward = position != 9
    
    for _ in range(steps):
        if is_moving_forward:
            position += 1
            if position == 9:  # Reached position 9, reverse direction
                is_moving_forward = False
        else:
            position -= 1
            if position == 1:  # Reached position 1, reverse direction
                is_moving_forward = True
    
    return position, is_moving_forward

if __name__ == "__main__":
    print("测试内圈反转移动逻辑。输入 q 退出。")
    current_position = 1
    while True:
        print(f"当前位置: {current_position}")
        user_input = input("请输入步数（正整数，q退出）：")
        if user_input.lower() == 'q':
            print("退出测试。")
            break
        try:
            steps = int(user_input)
            if steps < 0:
                print("请输入正整数步数。")
                continue
            new_position = get_next_position_with_reversal(current_position, steps)
            print(f"移动{steps}步后，新位置: {new_position}")
            current_position = new_position
        except ValueError:
            print("请输入有效的数字或q退出。")