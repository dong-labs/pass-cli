import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:uuid/uuid.dart';
import '../models/bot.dart';
import '../models/message.dart';

class BotsProvider with ChangeNotifier {
  WebSocketChannel? _channel;
  String? _deviceId;
  List<Bot> _bots = [];
  Map<int, List<Message>> _messages = {};
  final _uuid = const Uuid();
  final Map<String, Completer> _pendingRequests = {};

  List<Bot> get bots => _bots;
  
  void connect(String deviceId) {
    _deviceId = deviceId;
    
    // TODO: Replace with your server URL
    final wsUrl = Uri.parse('ws://localhost:3001?device_id=$deviceId');
    _channel = WebSocketChannel.connect(wsUrl);
    
    _channel!.stream.listen((data) {
      _handleMessage(jsonDecode(data));
    });
  }
  
  void _handleMessage(Map<String, dynamic> message) {
    if (message['type'] == 'event') {
      _handleEvent(message);
    } else if (message['type'] == 'res') {
      _handleResponse(message);
    }
  }
  
  void _handleEvent(Map<String, dynamic> message) {
    final event = message['event'];
    final payload = message['payload'];
    
    if (event == 'message') {
      final botId = payload['bot_id'];
      final msg = Message.fromJson(payload['message']);
      
      if (_messages[botId] == null) {
        _messages[botId] = [];
      }
      _messages[botId]!.add(msg);
      notifyListeners();
    }
  }
  
  void _handleResponse(Map<String, dynamic> message) {
    final id = message['id'];
    final completer = _pendingRequests.remove(id);
    
    if (completer != null) {
      if (message['ok'] == true) {
        completer.complete(message['payload']);
        
        // Update local state
        final payload = message['payload'];
        if (payload['bots'] != null) {
          _bots = (payload['bots'] as List)
              .map((b) => Bot.fromJson(b))
              .toList();
          notifyListeners();
        } else if (payload['bot'] != null) {
          final bot = Bot.fromJson(payload['bot']);
          final index = _bots.indexWhere((b) => b.id == bot.id);
          if (index >= 0) {
            _bots[index] = bot;
          } else {
            _bots.insert(0, bot);
          }
          notifyListeners();
        }
      } else {
        completer.completeError(message['error']);
      }
    }
  }
  
  Future<void> createBot(String name, String agentId) async {
    final id = _uuid.v4();
    final completer = Completer();
    _pendingRequests[id] = completer;
    
    _channel!.sink.add(jsonEncode({
      'type': 'req',
      'id': id,
      'method': 'create_bot',
      'params': {
        'name': name,
        'agent_id': agentId,
      },
    }));
    
    return completer.future;
  }
  
  Future<void> listBots() async {
    final id = _uuid.v4();
    final completer = Completer();
    _pendingRequests[id] = completer;
    
    _channel!.sink.add(jsonEncode({
      'type': 'req',
      'id': id,
      'method': 'list_bots',
      'params': {},
    }));
    
    return completer.future;
  }
  
  Future<void> sendMessage(int botId, String content) async {
    final id = _uuid.v4();
    final completer = Completer();
    _pendingRequests[id] = completer;
    
    _channel!.sink.add(jsonEncode({
      'type': 'req',
      'id': id,
      'method': 'send_message',
      'params': {
        'bot_id': botId,
        'content': content,
      },
    }));
    
    return completer.future;
  }
  
  List<Message> getMessages(int botId) {
    return _messages[botId] ?? [];
  }
  
  @override
  void dispose() {
    _channel?.sink.close();
    super.dispose();
  }
}

class Completer<T> {
  final _completer = Completer<T>();
  
  void complete([T? value]) => _completer.complete(value);
  void completeError([Object? error]) => _completer.completeError(error);
  Future<T> get future => _completer.future;
}
