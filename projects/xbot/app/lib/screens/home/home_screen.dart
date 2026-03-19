import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:uuid/uuid.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../providers/bots.dart';
import '../chat/chat_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _textController = TextEditingController();
  bool _isCreating = false;
  
  @override
  void initState() {
    super.initState();
    _init();
  }
  
  Future<void> _init() async {
    final prefs = await SharedPreferences.getInstance();
    var deviceId = prefs.getString('device_id');
    
    if (deviceId == null) {
      deviceId = const Uuid().v4();
      await prefs.setString('device_id', deviceId);
    }
    
    if (mounted) {
      context.read<BotsProvider>().connect(deviceId);
    }
  }
  
  Future<void> _createBot() async {
    final name = _textController.text.trim();
    if (name.isEmpty) return;
    
    setState(() => _isCreating = true);
    
    try {
      await context.read<BotsProvider>().createBot(name, 'cang');
      _textController.clear();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Bot 创建成功！')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('创建失败: $e')),
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isCreating = false);
      }
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('XBot'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => context.read<BotsProvider>().listBots(),
          ),
        ],
      ),
      body: Column(
        children: [
          // Bot List
          Expanded(
            child: Consumer<BotsProvider>(
              builder: (context, provider, child) {
                if (provider.bots.isEmpty) {
                  return const Center(
                    child: Text('还没有 Bot，创建一个吧！'),
                  );
                }
                
                return ListView.builder(
                  itemCount: provider.bots.length,
                  itemBuilder: (context, index) {
                    final bot = provider.bots[index];
                    return ListTile(
                      leading: CircleAvatar(
                        child: Text(bot.name[0]),
                      ),
                      title: Text(bot.name),
                      subtitle: Text(
                        'Token: ${bot.token.substring(0, 12)}...',
                        style: const TextStyle(fontSize: 12),
                      ),
                      trailing: const Icon(Icons.chevron_right),
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => ChatScreen(bot: bot),
                          ),
                        );
                      },
                    );
                  },
                );
              },
            ),
          ),
          
          // Create Bot Input
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _textController,
                    decoration: const InputDecoration(
                      hintText: 'Bot 名称',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                ElevatedButton(
                  onPressed: _isCreating ? null : _createBot,
                  child: _isCreating
                      ? const SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text('创建'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
  
  @override
  void dispose() {
    _textController.dispose();
    super.dispose();
  }
}
