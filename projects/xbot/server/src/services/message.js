import { callOpenClawAgent } from './openclaw.js';

export async function sendMessage(deviceId, params, prisma, ws) {
  const { botId, content } = params;
  
  // Get bot
  const bot = await prisma.bot.findFirst({
    where: { id: botId, deviceId }
  });
  
  if (!bot) {
    throw new Error('Bot not found');
  }
  
  // Save user message
  await prisma.message.create({
    data: {
      botId,
      role: 'user',
      content
    }
  });
  
  // Call OpenClaw Agent
  const agentResponse = await callOpenClawAgent(bot.agentId, content);
  
  // Save assistant message
  const assistantMessage = await prisma.message.create({
    data: {
      botId,
      role: 'assistant',
      content: agentResponse
    }
  });
  
  // Send event to client
  ws.send(JSON.stringify({
    type: 'event',
    event: 'message',
    payload: {
      botId,
      message: assistantMessage
    }
  }));
  
  return { success: true };
}

export async function getHistory(deviceId, botId, prisma) {
  const bot = await prisma.bot.findFirst({
    where: { id: botId, deviceId }
  });
  
  if (!bot) {
    throw new Error('Bot not found');
  }
  
  const messages = await prisma.message.findMany({
    where: { botId },
    orderBy: { createdAt: 'asc' },
    take: 100
  });
  
  return { messages };
}
