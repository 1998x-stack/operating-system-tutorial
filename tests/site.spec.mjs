import { chromium } from "playwright";

const baseURL = process.env.SITE_BASE_URL || "http://127.0.0.1:4173";
const browser = await chromium.launch({ headless: true });
const failures = [];
const viewports = [
  { name: "mobile-360", width: 360, height: 800 },
  { name: "mobile-390", width: 390, height: 844 },
  { name: "desktop-1440", width: 1440, height: 1000 },
];

try {
  const page = await browser.newPage();
  for (const viewport of viewports) {
    await page.setViewportSize({ width: viewport.width, height: viewport.height });
    const response = await page.goto(baseURL, { waitUntil: "networkidle" });
    if (!response?.ok()) failures.push(`index.html [${viewport.name}]: HTTP ${response?.status()}`);
    const home = await page.evaluate(() => ({
      title: document.title,
      h1: document.querySelectorAll("h1").length,
      main: document.querySelectorAll("main").length,
      width: document.documentElement.scrollWidth,
      viewport: window.innerWidth,
      routes: document.querySelectorAll(".route-card").length,
      chapterCards: document.querySelectorAll(".course-card").length,
    }));
    if (home.h1 !== 1) failures.push(`index.html [${viewport.name}]: expected one H1, got ${home.h1}`);
    if (home.main !== 1) failures.push(`index.html [${viewport.name}]: expected one main, got ${home.main}`);
    if (home.width > home.viewport + 1) failures.push(`index.html [${viewport.name}]: horizontal overflow ${home.width} > ${home.viewport}`);
    if (home.routes !== 4) failures.push(`index.html [${viewport.name}]: expected 4 learning routes, got ${home.routes}`);
    if (home.chapterCards !== 28) failures.push(`index.html [${viewport.name}]: expected 28 chapter cards, got ${home.chapterCards}`);
  }

  for (let number = 1; number <= 28; number += 1) {
    const path = `${String(number).padStart(2, "0")}.html`;
    for (const viewport of [{ width: 360, height: 800 }, { width: 1440, height: 1000 }]) {
      await page.setViewportSize(viewport);
      const response = await page.goto(`${baseURL}/${path}`, { waitUntil: "domcontentloaded" });
      if (!response?.ok()) {
        failures.push(`${path}: HTTP ${response?.status()}`);
        continue;
      }
      const result = await page.evaluate(() => ({
        h1: document.querySelectorAll("h1").length,
        main: document.querySelectorAll("main").length,
        toc: Boolean(document.querySelector(".page-toc")),
        width: document.documentElement.scrollWidth,
        viewport: window.innerWidth,
      }));
      if (result.h1 !== 1) failures.push(`${path}: expected one H1, got ${result.h1}`);
      if (result.main !== 1) failures.push(`${path}: expected one main, got ${result.main}`);
      if (!result.toc) failures.push(`${path}: missing section navigation`);
      if (result.width > result.viewport + 1) failures.push(`${path} [${viewport.width}px]: horizontal overflow ${result.width} > ${result.viewport}`);
    }
  }

  await page.setViewportSize({ width: 360, height: 800 });
  await page.goto(baseURL, { waitUntil: "domcontentloaded" });
  await page.keyboard.press("Tab");
  const skipLinkVisible = await page.locator(".skip-link").evaluate(el => {
    const rect = el.getBoundingClientRect();
    return rect.top >= 0 && rect.bottom <= window.innerHeight;
  });
  if (!skipLinkVisible) failures.push("index.html: skip link is not visible on keyboard focus");

  if (failures.length) {
    console.error("BROWSER QA FAILED");
    for (const failure of failures) console.error(" - " + failure);
    process.exitCode = 1;
  } else {
    console.log("BROWSER QA PASS: homepage at 360/390/1440px; 28 chapter pages; keyboard skip link.");
  }
} finally {
  await browser.close();
}
