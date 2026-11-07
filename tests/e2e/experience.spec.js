const { test, expect } = require('@playwright/test');

test.describe('Experience Page', () => {
  test('should load successfully with correct content', async ({ page }) => {
    const response = await page.goto('/experience');
    expect(response.status()).toBeLessThan(400);

    await expect(page).toHaveTitle(/Experience.*Gabriele Giardino/);
    await expect(page.locator('body')).toHaveClass(/page-experience/);

    await expect(page.locator('header')).toBeVisible();
    await expect(page.locator('header nav')).toBeVisible();

    await expect(page.locator('.breadcrumb-bar')).toBeVisible();
    const breadcrumbLinks = page.locator('.breadcrumbs a');
    await expect(breadcrumbLinks).toHaveCount(2);
    await expect(breadcrumbLinks.nth(0)).toHaveText(/🏠\s*Home/);
    await expect(breadcrumbLinks.nth(1)).toHaveText('Experience');

    await expect(page.locator('#experience-single')).toBeVisible();
    await expect(page.locator('.experience-list')).toBeVisible();

    await page.screenshot({ path: 'test-results/experience-page.png' });
  });

  test('should list the experience entries, most recent first', async ({ page }) => {
    await page.goto('/experience');

    const entries = page.locator('.experience');
    await expect(entries).toHaveCount(5);

    const first = entries.nth(0);
    await expect(first.locator('.experience__title')).toHaveText(/Technical Sales Manager/);
    await expect(first.locator('.experience__company')).toContainText('Duagon');

    const second = entries.nth(1);
    await expect(second.locator('.experience__title')).toHaveText(/Embedded Software Developer/);
    await expect(second.locator('.experience__company')).toContainText('Hofmann');

    const third = entries.nth(2);
    await expect(third.locator('.experience__company')).toContainText('Vector');
  });

  test('should have working navigation links', async ({ page }) => {
    await page.goto('/experience');

    await expect(page.locator('header nav a[href*="#about"]')).toBeVisible();
    await expect(page.locator('header nav a[href*="#experience-single"]')).toBeVisible();
    await expect(page.locator('header nav a[href*="#contact"]')).toBeVisible();

    await page.click('header a[href*="#about"]');
    await expect(page).toHaveURL(/.*#about/);

    await page.click('header a[href*="#experience-single"]');
    await expect(page).toHaveURL(/.*#experience-single/);

    await page.click('header a[href*="#contact"]');
    await expect(page).toHaveURL(/.*#contact/);
  });

  test('should link each entry to its detail page', async ({ page }) => {
    await page.goto('/experience');

    const links = page.locator('.experience__link');
    await expect(links.nth(0)).toHaveAttribute('href', /\/experience\/duagon\/$/);
    await expect(links.nth(1)).toHaveAttribute('href', /\/experience\/bmw\/$/);
    await expect(links.nth(2)).toHaveAttribute('href', /\/experience\/vector\/$/);
  });

  test('should have correct meta information', async ({ page }) => {
    await page.goto('/experience');

    await expect(page.locator('meta[name="description"]')).toHaveAttribute('content', /Gabriele Giardino/);
    await expect(page.locator('meta[property="og:title"]')).toHaveAttribute('content', 'Experience');
    await expect(page.locator('meta[property="og:type"]')).toHaveAttribute('content', 'website');
    await expect(page.locator('meta[property="og:url"]')).toHaveAttribute('content', /.*\/experience/);
  });

  test('should be responsive and accessible', async ({ page }) => {
    await page.goto('/experience');

    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('.experience-list')).toBeVisible();
    await expect(page.locator('.experience').first()).toBeVisible();

    await page.setViewportSize({ width: 768, height: 1024 });
    await expect(page.locator('.experience-list')).toBeVisible();

    await page.setViewportSize({ width: 1200, height: 800 });
    await expect(page.locator('.experience-list')).toBeVisible();

    await expect(page.locator('.skip-to-content-link')).toBeVisible();
    await expect(page.locator('.skip-to-content-link')).toHaveAttribute('href', '#main-content');
  });
});
