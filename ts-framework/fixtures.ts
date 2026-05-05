import { test as base } from '@playwright/test';
import { Config } from './utils/config';
import { Logger } from './utils/logger';

type TestFixtures = {
  config: typeof Config;
  logger: Logger;
};

export const test = base.extend<TestFixtures>({
  config: async ({}, use) => {
    await use(Config);
  },
  logger: async ({}, use) => {
    const logger = new Logger();
    await use(logger);
  },
});

export { expect } from '@playwright/test';