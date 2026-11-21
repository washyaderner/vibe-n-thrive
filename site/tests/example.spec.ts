import { test, expect } from '@playwright/test';

/**
 * E2E tests for the Vibe'N Thrive Vibro-Acoustic Therapy homepage.
 * Covers the 2026-06 lymphatic drainage section and the 2026-11 name change + address removal.
 */

test.describe('Homepage', () => {
  test('loads with the correct title', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Vibe'N Thrive Vibro-Acoustic Therapy/);
    await expect(page).toHaveTitle(/Portland, Oregon/);
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

  test('appears below the Our Therapies (services) section', async ({ page }) => {
    await page.goto('/');
    const servicesY = await page.locator('#services').evaluate(
      (el) => el.getBoundingClientRect().top + window.scrollY,
    );
    const lymphY = await page.locator('#lymphatic-drainage').evaluate(
      (el) => el.getBoundingClientRect().top + window.scrollY,
    );
    expect(lymphY).toBeGreaterThan(servicesY);
  });
});

test.describe('Location (2026-11: Portland only, no street address or map)', () => {
  test('says Portland and shows no street address, map, or old locations', async ({ page }) => {
    await page.goto('/');
    const body = page.locator('body');
    await expect(page.locator('.booking__area-city')).toHaveText('Portland, Oregon');
    await expect(page.locator('.footer__contact')).toContainText('Portland, Oregon');
    for (const old of ['Beaverton', 'Tigard', 'Powell', 'McDonald', '105th', 'Suite', '97008', '97224', '97206']) {
      await expect(body).not.toContainText(old);
    }
    await expect(page.locator('iframe[src*="google.com/maps"], iframe[data-src*="google.com/maps"]')).toHaveCount(0);
    await expect(page.locator('a[href*="maps.google"]')).toHaveCount(0);
  });

  test('uses the new business name in the header, footer, and Open Graph', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('.nav__logo')).toContainText("Vibe'N Thrive");
    await expect(page.locator('.nav__logo')).toContainText('Vibro-Acoustic Therapy');
    await expect(page.locator('.footer__bottom')).toContainText("Vibe'N Thrive Vibro-Acoustic Therapy");
    await expect(page.locator('meta[property="og:site_name"]')).toHaveAttribute('content', "Vibe'N Thrive Vibro-Acoustic Therapy");
    await expect(page.locator('body')).not.toContainText('Vibe & Thrive');
  });
});
