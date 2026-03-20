import { WebSocketServer } from 'ws';
import { handleMessage } from './handlers.js';

export function createWebSocketServer(prisma) {
  const wss = new WebSocketServer({ port: 0 }); // Port will be set later
  
  wss.on('connection', (ws, req) => {
    const url = new URL(req.url, `http://${req.headers.host}`);
    const deviceId = url.searchParams.get('device_id');
    
    if (!deviceId) {
      ws.close(4001, 'device_id is required');
      return;
    }
    
    // Store device_id on the connection
    ws.deviceId = deviceId;
    
    console.log(`[WS] Client connected: ${deviceId}`);
    
    ws.on('message', async (data) => {
      try {
        const message = JSON.parse(data.toString());
        await handleMessage(ws, message, prisma);
      } catch (error) {
        console.error('[WS] Error handling message:', error);
        ws.send(JSON.stringify({
          type: 'res',
          id: message?.id,
          ok: false,
          error: { code: 'INTERNAL_ERROR', message: error.message }
        }));
      }
    });
    
    ws.on('close', () => {
      console.log(`[WS] Client disconnected: ${deviceId}`);
    });
    
    // Send welcome message
    ws.send(JSON.stringify({
      type: 'event',
      event: 'connected',
      payload: { message: 'Welcome to XBot!' }
    }));
  });
  
  return wss;
}
