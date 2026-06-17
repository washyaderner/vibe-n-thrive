import { test, expect } from '@playwright/test';

/**
 * E2E tests for the Vibe & Thrive homepage.
 * Covers the 2026-06 update: lymphatic drainage section + Beaverton address move.
 */

test.describe('Homepage', () => {
  test('loads with the correct title', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Vibe & Thrive Therapy/);
    await expect(page).toHaveTitle(/Beaverton, Oregon/);
  });

  test('renders without first-party console errors', async ({ page }) => {
    const errors: string[] = [];
    page.on('console', (msg) => {
      // Ignore third-party (Calendly/Datadog) noise; only fail on first-party errors.
      if (msg.type() === 'error' && !msg.location().url.includes('calendly.com')) {
        errors.push(msg.text());
      }
    });
    await page.goto('/');
    await page.waitForTimeout(1000);
    expect(errors).toEqual([]);
  });
});

test.describe('Lymphatic Drainage section', () => {
  test('exists with heading, two phases, and three benefits', async ({ page }) => {
    await page.goto('/');
    const section = page.locator('#lymphatic-drainage');
    await expect(section).toHaveCount(1);
    await expect(section.getByRole('heading', { name: 'Lymphatic Drainage' })).toBeVisible();
    await expect(section.locator('.lymph__phase')).toHaveCount(2);
    await expect(section.locator('.lymph__benefit')).toHaveCount(3);
    await expect(section.getByText('Before VAT')).toBeVisible();
    await expect(section.getByText('After VAT')).toBeVisible();
  });

  test('is linked from the nav', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('.nav__links a[href="#lymphatic-drainage"]')).toHaveCount(1);
  });
});

test.describe('Beaverton address', () => {
  test('shows the new address and no longer references Tigard', async ({ page }) => {
    await page.goto('/');
    const body = page.locator('body');
    await expect(body).toContainText('6700 SW 105th Ave, Suite 217, Beaverton, OR 97008');
    await expect(page.locator('.footer__contact')).toContainText('Beaverton, OR 97008');
    await expect(body).not.toContainText('Tigard');
    await expect(body).not.toContainText('97224');
  });
});
