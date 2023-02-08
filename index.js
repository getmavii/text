import { serve } from "https://deno.land/std@0.177.0/http/server.ts";
import { DOMParser } from "https://deno.land/x/deno_dom/deno-dom-wasm.ts";
import { Readability } from "https://cdn.skypack.dev/@mozilla/readability";

const USER_AGENT =
  "Mozilla/5.0 (compatible; MaviiBot/1.0; +https://mavii.com/bots)";

serve(async (req) => {
  const url = new URL(req.url);
  const pageUrl = url.searchParams.get("url");
  const startTime = new Date();

  let article = null;

  if (pageUrl) {
    try {
      const res = await fetch(pageUrl, {
        headers: {
          "User-Agent": USER_AGENT,
        },
      });

      if (res.ok) {
        const body = await res.text();
        const doc = new DOMParser().parseFromString(body, "text/html");

        // Parse article
        article = new Readability(doc).parse();

        // Delete html content
        delete article.content;
      } else {
        console.error(res.statusText);
      }
    } catch (e) {
      console.error(e);
    }
  }

  // Pretty print JSON
  const json = JSON.stringify(article, null, 2);

  console.debug({ url: pageUrl, time: new Date() - startTime });

  return new Response(json, {
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "public, max-age=86400",
    },
  });
});
