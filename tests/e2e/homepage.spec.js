const { test, expect } = require('@playwright/test');

test.describe('Homepage', () => {
  test('should load successfully', async ({ page }) => {
    const response = await page.goto('/');
    expect(response.status()).toBeLessThan(400);

    await expect(page).toHaveTitle(/Gabriele Giardino/);

    await expect(page.locator('#about')).toBeVisible();
    await expect(page.locator('#experience-single')).toBeVisible();
    await expect(page.locator('#contact')).toBeVisible();

    // Header menu: About, Experience, Projects, Books, Contact, Search
    for (const href of ['#about', '#experience-single', '/projects', '/books', '#contact', '/search']) {
      await expect(page.locator(`header nav a[href*="${href}"]`).first()).toBeAttached();
    }

    // LinkedIn and GitHub
    await expect(page.locator('.platform-links a')).toHaveCount(2);

    // The single-CV download was removed: two resume versions now exist
    await expect(page.getByText('Download CV')).toHaveCount(0);

    await page.screenshot({ path: 'test-results/homepage.png' });
  });

  test('should have working navigation', async ({ page }) => {
    await page.goto('/');

    await page.click('header a[href*="#about"]');
    await expect(page.locator('#about')).toBeInViewport();

    await page.click('header a[href*="#experience-single"]');
    await expect(page.locator('#experience-single')).toBeInViewport();

    await page.click('header a[href*="#contact"]');
    await expect(page.locator('#contact')).toBeInViewport();
  });
});

test.describe('Projects page', () => {
  test('should show every project with a link to its code', async ({ page }) => {
    const response = await page.goto('/projects/');
    expect(response.status()).toBeLessThan(400);

    const cards = page.locator('.project-card');
    await expect(cards).toHaveCount(5);
    for (const repo of ['move_the_bot', 'the_agv_game', 'nvidia-shield-sword', 'forza', 'brainstormer']) {
      await expect(page.locator(`.project-card a[href="https://github.com/gabripo/${repo}"]`)).toHaveCount(1);
    }
    await expect(page.locator('.project-card a', { hasText: 'Try it' })).toHaveCount(2);
  });
});

test.describe('Removed template content', () => {
  test('the theme author\'s CV page is gone', async ({ page }) => {
    const response = await page.goto('/cv/');
    expect(response.status()).toBe(404);
  });
});
