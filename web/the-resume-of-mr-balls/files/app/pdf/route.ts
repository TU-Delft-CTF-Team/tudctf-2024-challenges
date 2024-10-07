import { PHASE_PRODUCTION_BUILD } from "next/dist/shared/lib/constants";
import type { NextRequest } from "next/server";
import puppeteer, { Browser, Page, PDFOptions } from "puppeteer";

declare global {
  // Create a global browser instance that can be reused across requests
  // and hot reloads
  var browser: Promise<Browser>;
}

// Prevent the browser instance from being created while building the app
if (process.env.NEXT_PHASE !== PHASE_PRODUCTION_BUILD) {
  globalThis.browser ??= puppeteer.launch({
    headless: "shell",
    pipe: true,
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--js-flags=--noexpose_wasm,--jitless",
    ],
    dumpio: true,
  });
}

async function createPDFStreamResponse(
  page: Page,
  options: PDFOptions,
  onClose: () => Promise<void>
) {
  try {
    const pdfStream = await page.createPDFStream(options);

    const streamWithCloseHandler = pdfStream.pipeThrough(
      new TransformStream({
        flush(controller) {
          onClose().catch(console.error);
        },
      })
    );

    return new Response(streamWithCloseHandler, {
      headers: { "Content-Type": "application/pdf" },
    });
  } catch (error) {
    console.error("Error generating PDF:", error);
    await page.close();
    throw error;
  }
}

export async function POST(req: NextRequest) {
  const html = `<!DOCTYPE html><html><body>${await req.text()}</body></html>`;

  let page = await (await browser).newPage();
  page.setJavaScriptEnabled(false);

  setTimeout(() => {
    // Prevent memory leak if someone keeps the stream open
    if (!page.isClosed()) {
      page.close();
    }
  }, 10000);

  await page.setContent(html, {
    timeout: 1000,
  });

  return createPDFStreamResponse(
    page,
    {
      omitBackground: true,
      printBackground: true,
      format: "A4",
    },
    async () => {
      await page.close();
    }
  );
}
