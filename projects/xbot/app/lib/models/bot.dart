class Bot {
  final int id;
  final String name;
  final String token;
  final String? agentId;
  final DateTime createdAt;
  
  Bot({
    required this.id,
    required this.name,
    required this.token,
    this.agentId,
    required this.createdAt,
  });
  
  factory Bot.fromJson(Map<String, dynamic> json) {
    return Bot(
      id: json['id'],
      name: json['name'],
      token: json['token'],
      agentId: json['agent_id'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}
