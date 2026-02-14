import { test, expect } from '@playwright/test';

/**
 * Example E2E test file
 * 
 * These tests verify the basic functionality of the site.
 * Add more tests as you build out features.
 */

test.describe('Homepage', () => {
  test('should load successfully', async ({ page }) => {
    // Navigate to homepage
    await page.goto('/');

    // Verify page loaded (check for any content)
    await expect(page.locator('body')).toBeVisible();
  });

  test('should have correct title', async ({ page }) => {
    await page.goto('/');

    // Check the page title - update this to match your actual title
    await expect(page).toHaveTitle(/Astro/);
  });
});

test.describe('Navigation', () => {
  test('should be accessible', async ({ page }) => {
    await page.goto('/');

    // Basic accessibility check - no console errors
    const errors: string[] = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });

    // Wait a moment for any errors to appear
    await page.waitForTimeout(1000);

    // Log errors for debugging (won't fail test, just informational)
    if (errors.length > 0) {
      console.log('Console errors found:', errors);
    }
  });
});
