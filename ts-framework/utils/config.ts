import * as fs from 'fs';
import * as path from 'path';

export class Config {
  // Load environment variables (simulate dotenv)
  private static loadEnv() {
    // In Node.js, use process.env, assume .env is loaded or set manually
  }

  // --- LOGGING CONFIGURATION ---
  static LOG_LEVEL = process.env.LOG_LEVEL || 'INFO';
  static LOG_FILE = process.env.LOG_FILE || 'automation.log';

  // Environment settings
  static BASE_URL = process.env.BASE_URL || 'https://insurance-portal.example.com';
  static API_URL = process.env.API_URL || 'https://api.insurance-portal.example.com';

  // Browser Settings
  static HEADLESS = (process.env.HEADLESS || 'false').toLowerCase() === 'true';
  static BROWSER = process.env.BROWSER || 'chromium';
  static BROWSER_TIMEOUT = parseInt(process.env.BROWSER_TIMEOUT || '30000');

  // Viewport Settings
  static BROWSER_VIEWPORT: { width: number; height: number } | null = null;
  static BROWSER_LAUNCH_ARGS = [
    '--window-size=1280,800',
    '--force-device-scale-factor=1',
    '--disable-blink-features=AutomationControlled'
  ];

  // Authentication Settings
  static TEST_USERNAME = process.env.USERNAME || 'testuser';
  static TEST_PASSWORD = process.env.PASSWORD || 'testpass';

  // Database Settings
  static DB_HOST = process.env.DB_HOST || 'localhost';
  static DB_PORT = parseInt(process.env.DB_PORT || '5432');

  // Timeouts
  static PAGE_LOAD_TIMEOUT = 30000;
  static ELEMENT_WAIT_TIMEOUT = 10000;
  static AJAX_WAIT_TIMEOUT = 5000;

  static getPlaywrightLaunchConfig() {
    return {
      headless: this.HEADLESS,
      args: this.BROWSER_LAUNCH_ARGS
    };
  }

  static getContextConfig() {
    return {
      viewport: this.BROWSER_VIEWPORT,
      ignoreHTTPSErrors: true
    };
  }
}