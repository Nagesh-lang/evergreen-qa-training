import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests-ui', timeout: 15000, workers: 1, retries: 0,
  reporter: [['list'], ['junit', { outputFile: 'reports/ui-junit.xml' }],
             ['html', { outputFolder: 'reports/playwright-html', open: 'never' }]],
  use: { browserName: 'chromium', headless: true, screenshot: 'only-on-failure', trace: 'retain-on-failure' },
  outputDir: 'reports/playwright-results',
});
