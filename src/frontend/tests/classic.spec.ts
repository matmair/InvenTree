import { test, expect } from '@playwright/test';
import exp from 'constants';

test('Check classic index site', async ({ page }) => {
  await page.goto('./api/');
  await page.goto('./index/');
  await expect(page).toHaveTitle('InvenTree Demo Server | Sign In');
  await expect(
    page.getByRole('heading', { name: 'InvenTree Demo Server' })
  ).toBeVisible();

  await page.getByLabel('username').fill('testuser');
  await page.getByLabel('password').fill('inventree');
  await page.click('button', { text: 'Sign In' });
  await page.waitForURL('**/index/');

  await page.waitForLoadState('networkidle');
  await expect(page).toHaveTitle('InvenTree Demo Server | Index');
  await expect(page.getByRole('button', { name: 'testuser' })).toBeVisible();
  await expect(
    page.getByRole('link', { name: 'Parts', exact: true })
  ).toBeVisible();
  await expect(
    page.getByRole('link', { name: 'Stock', exact: true })
  ).toBeVisible();
  await expect(
    page.getByRole('link', { name: 'Build', exact: true })
  ).toBeVisible();
  await expect(page.getByRole('button', { name: 'Buy' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Sell' })).toBeVisible();
});
