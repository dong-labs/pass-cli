import { generateToken } from '../utils/token.js';

export async function createBot(deviceId, params, prisma) {
  const { name, agentId = 'cang' } = params;
  
  if (!name || name.length < 3) {
    throw new Error('Bot name must be at least 3 characters');
  }
  
  const token = generateToken();
  
  const bot = await prisma.bot.create({
    data: {
      deviceId,
      name,
      token,
      agentId
    }
  });
  
  return { bot };
}

export async function listBots(deviceId, prisma) {
  const bots = await prisma.bot.findMany({
    where: { deviceId },
    orderBy: { createdAt: 'desc' }
  });
  
  return { bots };
}

export async function getBot(deviceId, botId, prisma) {
  const bot = await prisma.bot.findFirst({
    where: { id: botId, deviceId },
    include: {
      messages: {
        orderBy: { createdAt: 'desc' },
        take: 50
      }
    }
  });
  
  if (!bot) {
    throw new Error('Bot not found');
  }
  
  return { bot };
}

export async function deleteBot(deviceId, botId, prisma) {
  const bot = await prisma.bot.findFirst({
    where: { id: botId, deviceId }
  });
  
  if (!bot) {
    throw new Error('Bot not found');
  }
  
  await prisma.bot.delete({
    where: { id: botId }
  });
  
  return { success: true };
}
