const { test, expect } = require('@playwright/test');

test.describe('Homepage', () => {
  test('should load successfully', async ({ page }) => {
    // Navigate to localhost
    const response = await page.goto('http://localhost:1313');

    // Verify successful response
    expect(response.status()).toBeLessThan(400);

    // Check page title matches expected
    await expect(page).toHaveTitle('Gabriele Giardino | Mechatronics Engineer | Software Developer');

    // Verify key sections are present
    await expect(page.locator('#about')).toBeVisible();
    await expect(page.locator('#experience')).toBeVisible();
    await expect(page.locator('#contact')).toBeVisible();

    // Verify header navigation
    const headerLinks = page.locator('header nav a');
    await expect(headerLinks).toHaveCount(5); // Including home link

    // Verify social links are present
    const socialLinks = page.locator('.platform-links a');
    await expect(socialLinks).toHaveCount(7); // Based on homepage.yml config

    // Take a screenshot for visual reference
    await page.screenshot({ path: 'test-results/homepage.png' });
  });

  test('should have working navigation', async ({ page }) => {
    await page.goto('http://localhost:1313');

    // Click About link and verify scroll
    await page.click('header a[href*="#about"]');
    await expect(page.locator('#about')).toBeInViewport();

    // Click Experience link and verify scroll
    await page.click('header a[href*="#experience"]');
    await expect(page.locator('#experience')).toBeInViewport();

    // Click Contact link and verify scroll
    await page.click('header a[href*="#contact"]');
    await expect(page.locator('#contact')).toBeInViewport();
  });
}); 