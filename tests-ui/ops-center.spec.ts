import { test, expect } from '@playwright/test';
import path from 'path';
import { pathToFileURL } from 'url';
const localPage = pathToFileURL(path.resolve(__dirname, '../ui/mock_ops_center.html')).href;

test('LAB UI: auditor cannot resume a parked campaign', async ({ page }) => {
  await page.goto(localPage);
  await expect(page.getByText('TRAINING SIMULATOR ONLY')).toBeVisible();
  await expect(page.getByText('PARKED')).toBeVisible();
  await expect(page.getByRole('button', { name: 'Resume campaign' })).toBeDisabled();
});

test('LAB UI: patch ops can explicitly resume a parked campaign', async ({ page }) => {
  await page.goto(localPage);
  await page.getByRole('combobox', { name: 'Persona' }).selectOption('patch_ops_engineer');
  await page.getByRole('button', { name: 'Resume campaign' }).click();
  await expect(page.locator('#status')).toHaveText('READY');
});
