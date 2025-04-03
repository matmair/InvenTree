import { test } from '../baseFixtures.js';
import {
  clearTableFilters,
  clickButtonIfVisible,
  loadTab,
  navigate,
  openFilterDrawer,
  setTableChoiceFilter
} from '../helpers.js';
import { doCachedLogin } from '../login.js';

test('Stock - Basic Tests', async ({ browser }) => {
  const page = await doCachedLogin(browser, { url: 'stock/location/index/' });

  await page.waitForURL('**/web/stock/location/**');

  await loadTab(page, 'Location Details');
  await page.waitForURL('**/web/stock/location/index/details');

  await loadTab(page, 'Stock Items');
  await page.getByText('1551ABK').first().click();

  await page.getByRole('tab', { name: 'Stock', exact: true }).click();
  await page.waitForURL('**/web/stock/**');
  await loadTab(page, 'Stock Locations');
  await page.getByRole('cell', { name: 'Electronics Lab' }).first().click();
  await loadTab(page, 'Default Parts');
  await loadTab(page, 'Stock Locations');
  await loadTab(page, 'Stock Items');
  await loadTab(page, 'Location Details');

  await navigate(page, 'stock/item/1194/details');
  await page.getByText('D.123 | Doohickey').waitFor();
  await page.getByText('Batch Code: BX-123-2024-2-7').waitFor();
  await loadTab(page, 'Stock Tracking');
  await loadTab(page, 'Test Data');
  await page.getByText('395c6d5586e5fb656901d047be27e1f7').waitFor();
  await loadTab(page, 'Installed Items');
});

test('Stock - Location Tree', async ({ browser }) => {
  const page = await doCachedLogin(browser, { url: 'stock/location/index/' });

  await page.waitForURL('**/web/stock/location/**');
  await loadTab(page, 'Location Details');

  await page.getByLabel('nav-breadcrumb-action').click();
  await page.getByLabel('nav-tree-toggle-1}').click();
  await page.getByLabel('nav-tree-item-2').click();

  await page.getByLabel('breadcrumb-2-storage-room-a').waitFor();
  await page.getByLabel('breadcrumb-1-factory').click();

  await page.getByRole('cell', { name: 'Factory' }).first().waitFor();
});

test('Stock - Filters', async ({ browser }) => {
  const page = await doCachedLogin(browser, {
    username: 'steven',
    password: 'wizardstaff',
    url: '/stock/location/index/'
  });

  await loadTab(page, 'Stock Items');

  await openFilterDrawer(page);
  await clickButtonIfVisible(page, 'Clear Filters');

  // Filter by updated date
  await page.getByRole('button', { name: 'Add Filter' }).click();
  await page.getByPlaceholder('Select filter').fill('updated');
  await page.getByText('Updated After').click();
  await page.getByPlaceholder('Select date value').fill('2010-01-01');
  await page.getByText('Show items updated after this date').waitFor();

  // Filter by batch code
  await page.getByRole('button', { name: 'Add Filter' }).click();
  await page.getByPlaceholder('Select filter').fill('batch');
  await page
    .getByRole('option', { name: 'Batch Code', exact: true })
    .locator('span')
    .click();
  await page.getByPlaceholder('Enter filter value').fill('TABLE-B02');
  await page.getByLabel('apply-text-filter').click();

  // Close dialog
  await page.keyboard.press('Escape');

  // Ensure correct result is displayed
  await page
    .getByRole('cell', { name: 'A round table - with blue paint' })
    .waitFor();

  // Filter by custom status code
  await clearTableFilters(page);
  await setTableChoiceFilter(page, 'Status', 'Incoming goods inspection');
  await page.getByText('1 - 8 / 8').waitFor();
  await page.getByRole('cell', { name: '1551AGY' }).first().waitFor();
  await page.getByRole('cell', { name: 'widget.blue' }).first().waitFor();
  await page.getByRole('cell', { name: '002.01-PCBA' }).first().waitFor();

  await clearTableFilters(page);
});

test('Stock - Serial Numbers', async ({ browser }) => {
  const page = await doCachedLogin(browser);

  // Use the "global search" functionality to find a part we are interested in
  // This is to exercise the search functionality and ensure it is working as expected
  await page.getByLabel('open-search').click();

  await page.getByLabel('global-search-input').clear();

  await page.waitForTimeout(250);
  await page.getByLabel('global-search-input').fill('widget green');
  await page.waitForTimeout(250);

  // Remove the "stock item" results group
  await page.getByLabel('remove-search-group-stockitem').click();

  await page
    .getByText(/widget\.green/)
    .first()
    .click();

  await page
    .getByLabel('panel-tabs-part')
    .getByRole('tab', { name: 'Stock', exact: true })
    .click();
  await page.getByLabel('action-button-add-stock-item').click();

  // Initially fill with invalid serial/quantity combinations
  await page.getByLabel('text-field-serial_numbers').fill('200-250');
  await page.getByLabel('number-field-quantity').fill('10');

  // Add delay to account to field debounce
  await page.waitForTimeout(250);

  await page.getByRole('button', { name: 'Submit' }).click();

  // Expected error messages
  await page.getByText('Errors exist for one or more form fields').waitFor();
  await page
    .getByText(/exceeds allowed quantity/)
    .first()
    .waitFor();

  // Now, with correct quantity
  await page.getByLabel('number-field-quantity').fill('51');
  await page.waitForTimeout(250);
  await page.getByRole('button', { name: 'Submit' }).click();
  await page.waitForTimeout(250);

  await page
    .getByText(
      /The following serial numbers already exist or are invalid : 200,201,202,203,204/
    )
    .first()
    .waitFor();

  // Expected error messages
  await page.getByText('Errors exist for one or more form fields').waitFor();

  // Close the form
  await page.getByRole('button', { name: 'Cancel' }).click();
});

test('Stock - Serialize', async ({ browser }) => {
  const page = await doCachedLogin(browser, { url: 'stock/item/232/details' });

  // Fill out with faulty serial numbers to check buttons and forms
  await page.getByLabel('action-menu-stock-operations').click();
  await page.getByLabel('action-menu-stock-operations-serialize').click();

  await page.getByLabel('text-field-serial_numbers').fill('200-250');

  await page.getByRole('button', { name: 'Submit' }).click();
  await page
    .getByText('Group range 200-250 exceeds allowed quantity')
    .waitFor();
  await page.getByRole('button', { name: 'Cancel' }).click();
});

/**
 * Test various 'actions' on the stock detail page
 */
test('Stock - Stock Actions', async ({ browser }) => {
  const page = await doCachedLogin(browser, { url: 'stock/item/1225/details' });

  // Helper function to launch a stock action
  const launchStockAction = async (action: string) => {
    await page.getByLabel('action-menu-stock-operations').click();
    await page.getByLabel(`action-menu-stock-operations-${action}`).click();
  };

  const setStockStatus = async (status: string) => {
    await page.getByLabel('action-button-change-status').click();
    await page.getByLabel('choice-field-status').click();
    await page.getByRole('option', { name: status }).click();
  };

  // Check for required values
  await page.getByText('Status', { exact: true }).waitFor();
  await page.getByText('Custom Status', { exact: true }).waitFor();
  await page.getByText('Attention needed').waitFor();
  await page
    .getByLabel('Stock Details')
    .getByText('Incoming goods inspection')
    .waitFor();
  await page.getByText('123').first().waitFor();

  // Add stock, and change status
  await launchStockAction('add');
  await page.getByLabel('number-field-quantity').fill('12');
  await setStockStatus('Lost');
  await page.getByRole('button', { name: 'Submit' }).click();

  await page.getByText('Lost').first().waitFor();
  await page.getByText('Unavailable').first().waitFor();
  await page.getByText('135').first().waitFor();

  // Remove stock, and change status
  await launchStockAction('remove');
  await page.getByLabel('number-field-quantity').fill('99');
  await setStockStatus('Damaged');
  await page.getByRole('button', { name: 'Submit' }).click();

  await page.getByText('36').first().waitFor();
  await page.getByText('Damaged').first().waitFor();

  // Count stock and change status (reverting to original value)
  await launchStockAction('count');
  await page.getByLabel('number-field-quantity').fill('123');
  await setStockStatus('Incoming goods inspection');
  await page.getByRole('button', { name: 'Submit' }).click();

  await page.getByText('123').first().waitFor();
  await page.getByText('Custom Status').first().waitFor();
  await page.getByText('Incoming goods inspection').first().waitFor();

  // Find an item which has been sent to a customer
  await navigate(page, 'stock/item/1014/details');
  await page.getByText('Batch Code: 2022-11-12').waitFor();
  await page.getByText('Unavailable').waitFor();
  await page.getByLabel('action-menu-stock-operations').click();
  await page.getByLabel('action-menu-stock-operations-return').click();
});

test('Stock - Tracking', async ({ browser }) => {
  const page = await doCachedLogin(browser, { url: 'stock/item/176/details' });

  await page.getByRole('link', { name: 'Widget Assembly # 2' }).waitFor();

  // Navigate to the "stock tracking" tab
  await loadTab(page, 'Stock Tracking');
  await page.getByText('- - Factory/Office Block/Room').first().waitFor();
  await page.getByRole('link', { name: 'Widget Assembly' }).waitFor();
  await page.getByRole('cell', { name: 'Installed into assembly' }).waitFor();
});
