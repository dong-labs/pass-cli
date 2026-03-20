import WebSocket from 'ws';

const GATEWAY_URL = process.env.OPENCLAW_GATEWAY_URL || 'ws://127.0.0.1:18789';
const GATEWAY_TOKEN = process.env.OPENCLAW_GATEWAY_TOKEN || '';

let gatewayWs = null;
let requestId = 1;
const pendingRequests = new Map();

export async function callOpenClawAgent(agentId, message) {
  // Connect to Gateway if not connected
  if (!gatewayWs || gatewayWs.readyState !== WebSocket.OPEN) {
    await connectToGateway();
  }
  
  return new Promise((resolve, reject) => {
    const id = String(requestId++);
    
    pendingRequests.set(id, { resolve, reject });
    
    // Send chat request
    gatewayWs.send(JSON.stringify({
      type: 'req',
      id,
      method: 'chat',
      params: {
        agent_id: agentId,
        message
      }
    }));
    
    // Timeout after 30 seconds
    setTimeout(() => {
      if (pendingRequests.has(id)) {
        pendingRequests.delete(id);
        reject(new Error('Request timeout'));
      }
    }, 30000);
  });
}

async function connectToGateway() {
  return new Promise((resolve, reject) => {
    gatewayWs = new WebSocket(GATEWAY_URL);
    
    gatewayWs.on('open', () => {
      // Send handshake
      gatewayWs.send(JSON.stringify({
        type: 'req',
        id: '1',
        method: 'connect',
        params: {
          minProtocol: 1,
          maxProtocol: 1,
          client: {
            id: 'xbot',
            displayName: 'XBot',
            version: '1.0.0'
          },
          auth: {
            token: GATEWAY_TOKEN
          }
        }
      }));
    });
    
    gatewayWs.on('message', (data) => {
      const message = JSON.parse(data.toString());
      
      if (message.type === 'res') {
        if (message.id === '1') {
          // Handshake response
          if (message.ok) {
            console.log('[OpenClaw] Connected to Gateway');
            resolve();
          } else {
            reject(new Error('Handshake failed'));
          }
        } else {
          // Regular response
          const pending = pendingRequests.get(message.id);
          if (pending) {
            pendingRequests.delete(message.id);
            if (message.ok) {
              pending.resolve(message.payload?.response || message.payload?.message || 'OK');
            } else {
              pending.reject(new Error(message.error?.message || 'Unknown error'));
            }
          }
        }
      } else if (message.type === 'event') {
        // Handle events if needed
        console.log('[OpenClaw] Event:', message.event);
      }
    });
    
    gatewayWs.on('error', (error) => {
      console.error('[OpenClaw] WebSocket error:', error);
      reject(error);
    });
    
    gatewayWs.on('close', () => {
      console.log('[OpenClaw] Disconnected from Gateway');
      gatewayWs = null;
    });
  });
}
