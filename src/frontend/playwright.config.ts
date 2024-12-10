import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  timeout: 30000,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 3 : undefined,
  reporter: process.env.CI ? [['html', { open: 'never' }], ['github']] : 'list',

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome']
      }
    }
  ],

  /* Run your local dev server before starting the tests */
  webServer: [
    {
      command: 'yarn run dev',
      url: 'http://localhost:5173',
      reuseExistingServer: !process.env.CI,
      stdout: 'pipe',
      stderr: 'pipe',
      timeout: 120 * 1000
    },
    {
      command: 'invoke dev.server -a 127.0.0.1:8000',
      env: {
        INVENTREE_DEBUG: 'True',
        INVENTREE_PLUGINS_ENABLED: 'True',
        INVENTREE_ADMIN_URL: 'test-admin'
      },
      url: 'http://127.0.0.1:8000/api/',
      reuseExistingServer: !process.env.CI,
      stdout: 'pipe',
      stderr: 'pipe',
      timeout: 120 * 1000
    }
  ],
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry'
  }
});
