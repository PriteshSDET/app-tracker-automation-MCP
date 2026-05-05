import * as fs from 'fs';
import * as path from 'path';
import { Config } from './config';

export class Logger {
  private logger: any; // Use a simple console logger for now, or integrate winston if needed

  constructor(name?: string) {
    // Simple logger implementation
    this.logger = {
      info: (msg: string) => console.log(`[${new Date().toISOString()}] INFO - ${name || 'Logger'}: ${msg}`),
      debug: (msg: string) => console.log(`[${new Date().toISOString()}] DEBUG - ${name || 'Logger'}: ${msg}`),
      error: (msg: string) => console.error(`[${new Date().toISOString()}] ERROR - ${name || 'Logger'}: ${msg}`),
      warn: (msg: string) => console.warn(`[${new Date().toISOString()}] WARN - ${name || 'Logger'}: ${msg}`)
    };
  }

  info(msg: string) {
    this.logger.info(msg);
  }

  debug(msg: string) {
    this.logger.debug(msg);
  }

  error(msg: string) {
    this.logger.error(msg);
  }

  warn(msg: string) {
    this.logger.warn(msg);
  }
}