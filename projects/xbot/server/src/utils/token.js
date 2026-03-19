import { randomBytes } from 'crypto';

export function generateToken() {
  // Generate 32 bytes of random data and convert to hex
  const randomData = randomBytes(32);
  const token = 'xbot_' + randomData.toString('hex');
  return token;
}
