import { expect, test } from "@playwright/test";

const E2E_EMAIL = process.env.E2E_EMAIL || "admin@ideas.com";
const E2E_PASSWORD = process.env.E2E_PASSWORD || "ChangeMe123!";

test("login, create idea, update, add log and rate", async ({ page }) => {
  const uniqueTitle = `E2E Idea ${Date.now()}`;

  await page.goto("/login");
  await page.getByLabel("Email").fill(E2E_EMAIL);
  await page.getByLabel("Password").fill(E2E_PASSWORD);
  await page.getByRole("button", { name: "Sign in" }).click();

  // Argon2 + JWT + Next.js navigation can take several seconds in CI — wait for URL first.
  await page.waitForURL("**/ideas", { timeout: 15_000 });
  await expect(page.getByRole("heading", { level: 1, name: "Ideas", exact: true })).toBeVisible();

  await page.getByPlaceholder("Idea title").fill(uniqueTitle);
  await page.getByPlaceholder("Idea description").fill("E2E flow description");
  await page.getByRole("button", { name: "Create" }).click();

  await expect(page.getByText(uniqueTitle)).toBeVisible();
  await page.locator("article", { hasText: uniqueTitle }).getByRole("link", { name: "View detail" }).click();

  await expect(page.getByRole("heading", { name: "Idea detail" })).toBeVisible();
  await page.locator("select").first().selectOption("completed");
  await page.locator('input[type="number"]').first().fill("100");
  await page.getByRole("button", { name: "Save changes" }).click();

  await page.getByLabel("Add progress comment").fill("E2E progress log");
  await page.getByRole("button", { name: "Add log" }).click();
  await expect(page.getByText("E2E progress log")).toBeVisible();

  await page.getByLabel("Rating (1..10)").fill("9");
  await page.getByLabel("Summary").fill("Excellent outcome");
  await page.getByRole("button", { name: "Save rating" }).click();
  await expect(page.getByText("Current rating")).toBeVisible();
  await expect(page.getByText("9 / 10")).toBeVisible();
});
