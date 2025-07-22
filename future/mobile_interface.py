"""
未来手机客户端接口
为将来的手机客户端功能预留接口
"""

import json
from enum import Enum

class ActionType(Enum):
    """操作类型"""
    ROLL_DICE = "roll_dice"
    BUY_CARD = "buy_card"
    PASS_CARD = "pass_card"
    END_TURN = "end_turn"
    SELL_ASSET = "sell_asset"
    GET_GAME_STATE = "get_game_state"

class MobileClientInterface:
    """为未来手机客户端预留的接口"""
    
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.connected_clients = {}  # {player_id: client_info}
        
    def register_client(self, player_id, client_info):
        """注册客户端"""
        self.connected_clients[player_id] = client_info
        return True
    
    def unregister_client(self, player_id):
        """注销客户端"""
        if player_id in self.connected_clients:
            del self.connected_clients[player_id]
            return True
        return False
    
    def handle_mobile_action(self, player_id, action_type, action_data=None):
        """处理手机客户端的操作"""
        
        # 验证客户端是否已注册
        if player_id not in self.connected_clients:
            return self._create_response(False, "客户端未注册")
        
        # 验证是否轮到该玩家
        current_player = self.game_engine.get_current_player()
        if not current_player or current_player.name != player_id:
            return self._create_response(False, "不是你的回合")
        
        try:
            # 根据操作类型执行相应的动作
            if action_type == ActionType.ROLL_DICE.value:
                return self._handle_roll_dice(player_id, action_data)
            elif action_type == ActionType.BUY_CARD.value:
                return self._handle_buy_card(player_id, action_data)
            elif action_type == ActionType.PASS_CARD.value:
                return self._handle_pass_card(player_id, action_data)
            elif action_type == ActionType.END_TURN.value:
                return self._handle_end_turn(player_id, action_data)
            elif action_type == ActionType.SELL_ASSET.value:
                return self._handle_sell_asset(player_id, action_data)
            elif action_type == ActionType.GET_GAME_STATE.value:
                return self._handle_get_game_state(player_id)
            else:
                return self._create_response(False, f"未知操作类型: {action_type}")
                
        except Exception as e:
            return self._create_response(False, f"操作执行失败: {str(e)}")
    
    def _handle_roll_dice(self, player_id, action_data):
        """处理投骰子操作"""
        success, message = self.game_engine.roll_dice()
        
        if success:
            # 广播给所有客户端
            self._broadcast_game_state()
            
        return self._create_response(success, message, {
            'dice_value': self.game_engine.current_dice_roll if success else None
        })
    
    def _handle_buy_card(self, player_id, action_data):
        """处理购买卡片操作"""
        additional_data = action_data.get('additional_data') if action_data else None
        success, message = self.game_engine.handle_card_decision("buy", additional_data)
        
        if success:
            self._broadcast_game_state()
            
        return self._create_response(success, message)
    
    def _handle_pass_card(self, player_id, action_data):
        """处理放弃卡片操作"""
        success, message = self.game_engine.handle_card_decision("pass")
        
        if success:
            self._broadcast_game_state()
            
        return self._create_response(success, message)
    
    def _handle_end_turn(self, player_id, action_data):
        """处理结束回合操作"""
        success, message = self.game_engine.end_turn()
        
        if success:
            self._broadcast_game_state()
            
            # 如果游戏结束，通知所有客户端
            if self.game_engine.game_phase.value == "游戏结束":
                self._broadcast_game_end(message)
        
        return self._create_response(success, message)
    
    def _handle_sell_asset(self, player_id, action_data):
        """处理卖出资产操作"""
        if not action_data:
            return self._create_response(False, "缺少必要的操作数据")
        
        success, message = self.game_engine.handle_market_action("sell_asset", action_data)
        
        if success:
            self._broadcast_game_state()
            
        return self._create_response(success, message)
    
    def _handle_get_game_state(self, player_id):
        """获取游戏状态"""
        game_state = self.game_engine.get_game_state()
        return self._create_response(True, "获取游戏状态成功", game_state)
    
    def _create_response(self, success, message, data=None):
        """创建响应数据"""
        response = {
            'success': success,
            'message': message,
            'timestamp': self._get_timestamp()
        }
        
        if data:
            response['data'] = data
            
        return response
    
    def _broadcast_game_state(self):
        """向所有客户端广播游戏状态"""
        if not self.connected_clients:
            return
            
        game_state = self.game_engine.get_game_state()
        broadcast_data = {
            'type': 'game_state_update',
            'data': game_state,
            'timestamp': self._get_timestamp()
        }
        
        # 这里实际应该通过网络发送给每个客户端
        # 现在只是预留接口
        for player_id, client_info in self.connected_clients.items():
            # self._send_to_client(client_info, broadcast_data)
            pass
    
    def _broadcast_game_end(self, end_message):
        """广播游戏结束消息"""
        if not self.connected_clients:
            return
            
        broadcast_data = {
            'type': 'game_end',
            'message': end_message,
            'final_state': self.game_engine.get_game_state(),
            'timestamp': self._get_timestamp()
        }
        
        for player_id, client_info in self.connected_clients.items():
            # self._send_to_client(client_info, broadcast_data)
            pass
    
    def _get_timestamp(self):
        """获取当前时间戳"""
        import time
        return int(time.time())
    
    def get_connected_clients(self):
        """获取已连接的客户端列表"""
        return list(self.connected_clients.keys())
    
    def get_client_count(self):
        """获取客户端数量"""
        return len(self.connected_clients)
    
    def is_client_connected(self, player_id):
        """检查客户端是否已连接"""
        return player_id in self.connected_clients

# 未来可能的网络通信类
class NetworkManager:
    """网络管理器 - 预留用于未来的网络功能"""
    
    def __init__(self, host="localhost", port=8888):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_sockets = {}
        
    def start_server(self):
        """启动服务器"""
        # 预留接口，实际实现需要使用socket或其他网络库
        pass
    
    def stop_server(self):
        """停止服务器"""
        pass
    
    def send_to_client(self, client_id, data):
        """发送数据到客户端"""
        pass
    
    def broadcast_to_all(self, data):
        """广播数据到所有客户端"""
        pass

# 未来可能的屏幕投射类
class ScreenCastManager:
    """屏幕投射管理器 - 预留用于未来的投屏功能"""
    
    def __init__(self):
        self.cast_enabled = False
        self.cast_device = None
        
    def enable_casting(self, device_info):
        """启用屏幕投射"""
        pass
    
    def disable_casting(self):
        """禁用屏幕投射"""
        pass
    
    def update_display(self, game_state):
        """更新投射显示"""
        pass 