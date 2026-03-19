import { createBot, listBots, getBot, deleteBot } from '../services/bot.js';
import { sendMessage, getHistory } from '../services/message.js';

export async function handleMessage(ws, message, prisma) {
  const { type, id, method, params } = message;
  
  if (type !== 'req') {
    ws.send(JSON.stringify({
      type: 'res',
      id,
      ok: false,
      error: { code: 'INVALID_TYPE', message: 'Only "req" type is supported' }
    }));
    return;
  }
  
  try {
    let result;
    
    switch (method) {
      case 'create_bot':
        result = await createBot(ws.deviceId, params, prisma);
        break;
        
      case 'list_bots':
        result = await listBots(ws.deviceId, prisma);
        break;
        
      case 'get_bot':
        result = await getBot(ws.deviceId, params.botId, prisma);
        break;
        
      case 'delete_bot':
        result = await deleteBot(ws.deviceId, params.botId, prisma);
        break;
        
      case 'send_message':
        result = await sendMessage(ws.deviceId, params, prisma, ws);
        break;
        
      case 'get_history':
        result = await getHistory(ws.deviceId, params.botId, prisma);
        break;
        
      default:
        throw new Error(`Unknown method: ${method}`);
    }
    
    ws.send(JSON.stringify({
      type: 'res',
      id,
      ok: true,
      payload: result
    }));
    
  } catch (error) {
    ws.send(JSON.stringify({
      type: 'res',
      id,
      ok: false,
      error: { code: 'ERROR', message: error.message }
    }));
  }
}
