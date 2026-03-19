import express from 'express';
import { WebSocketServer } from 'ws';
import { PrismaClient } from '@prisma/client';
import dotenv from 'dotenv';
import { createWebSocketServer } from './websocket/server.js';

dotenv.config();

const app = express();
const prisma = new PrismaClient();

const PORT = process.env.PORT || 3000;
const WS_PORT = process.env.WS_PORT || 3001;

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Start HTTP server
app.listen(PORT, () => {
  console.log(`[HTTP] Server running on port ${PORT}`);
});

// Start WebSocket server
const wss = createWebSocketServer(prisma);
wss.listen(WS_PORT, () => {
  console.log(`[WS] WebSocket server running on port ${WS_PORT}`);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, shutting down...');
  await prisma.$disconnect();
  process.exit(0);
});
