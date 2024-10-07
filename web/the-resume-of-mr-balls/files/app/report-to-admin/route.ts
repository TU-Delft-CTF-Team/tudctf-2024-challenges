import type { NextRequest } from "next/server";
import { z } from "zod";

// Reuse the Puppeteer browser instance
import "../pdf/route";

const envSchema = z.object({
  FLAG: z.string().min(1),
  APP_ORIGIN: z
    .string()
    .url()
    .transform((url) => new URL(url)),
});

let config: z.infer<typeof envSchema> | null = null;

export async function POST(req: NextRequest) {
  if (!config) {
    config = envSchema.parse(process.env);
  }

  const url = await req.text();
  if (!url) {
    return new Response("Empty body", { status: 400 });
  }

  const parsed = new URL(url);
  if (parsed.origin !== config.APP_ORIGIN.origin) {
    return new Response(
      `Invalid origin: ${parsed.origin}, expected ${config.APP_ORIGIN.origin}`,
      { status: 400 }
    );
  }

  const context = await (await globalThis.browser).createBrowserContext({});
  const page = await context.newPage();
  const id = crypto.randomUUID();

  try {
    page.setCookie({
      name: "flag",
      value: config.FLAG,
      domain: config.APP_ORIGIN.hostname,
    });

    console.log(`[${id}] Navigating to ${parsed.href}`);

    const start = Date.now();

    await page.goto(parsed.href, {
      waitUntil: "networkidle0",
      timeout: 60000,
      signal: req.signal,
    });

    console.log(`[${id}] Network idle in ${Date.now() - start}ms`);

    await page.waitForSelector(".sp-loading", { signal: req.signal });

    await page.waitForFunction(() => !document.querySelector(".sp-loading"), {
      timeout: 120000,
      signal: req.signal,
    });

    console.log(`[${id}] Loading screen lifted in ${Date.now() - start}ms`);

    const bundleError = await page.evaluate(() => {
      const error = document.querySelector(
        ".sp-overlay > .sp-error-message"
      ) as HTMLElement | null;
      return error?.innerText ?? null;
    });

    if (bundleError) {
      console.error(`[${id}] Error while bundling: ${bundleError}`);
      return new Response(`Error while bundling:\n\n${bundleError}`, {
        status: 500,
      });
    }

    try {
      await page.waitForSelector(".react-pdf__Page", {
        timeout: 30000,
        signal: req.signal,
      });
    } catch (error) {
      console.error(
        `[${id}] Timed out waiting for PDF to render in ${Date.now() - start}ms`
      );
      await page.close();
      await context.close();
      console.log(`[${id}] Page closed`);
      return new Response("PDF render timed out", { status: 500 });
    }

    console.log(`[${id}] PDF generated in ${Date.now() - start}ms`);

    return new Response("Report sent", { status: 200 });
  } finally {
    setTimeout(async () => {
      // await page.screenshot({ path: "./test.png" });
      if (!page.isClosed()) {
        await page.close();
        console.log(`[${id}] Page closed`);
      }
      if (!context.closed) {
        await context.close();
      }
    }, 5000);
  }
}
