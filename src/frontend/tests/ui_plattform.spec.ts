import { test, expect } from '@playwright/test';

test('Basic Platform UI test', async ({ page }) => {
  await page.goto('./index/');
  await expect(page).toHaveTitle('InvenTree Demo Server | Sign In');
  await expect(
    page.getByRole('heading', { name: 'InvenTree Demo Server' })
  ).toBeVisible();

  await page.getByLabel('username').fill('allaccess');
  await page.getByLabel('password').fill('nolimits');
  await page.click('button', { text: 'Sign In' });

  await page.goto('./platform/');

  await expect(page).toHaveTitle('InvenTree Demo Server');
  await expect(
    page.getByRole('heading', { name: 'Welcome to the new frontend!' })
  ).toBeVisible();
});
