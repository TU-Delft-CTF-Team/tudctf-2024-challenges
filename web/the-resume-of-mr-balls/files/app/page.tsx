"use client";

import { PDFViewer } from "@/components/pdf-viewer";
import {
  SandpackCodeEditor,
  SandpackLayout,
  SandpackPreview,
  SandpackProvider,
  useActiveCode,
} from "@codesandbox/sandpack-react";
import MonacoEditor from "@/components/monaco-editor";
import { useEffect, useState } from "react";

export default function Home() {
  return (
    <div>
      <SandpackProvider
        theme="dark"
        template="react-ts"
        customSetup={{
          dependencies: {
            "@fileforge/react-print": "^0.1.144",
          },
        }}
        files={{
          "/App.tsx": {
            code: source,
          },
          "/render.ts": {
            code: renderSource,
            hidden: true,
          },
          "/index.tsx": {
            code: indexSource,
            hidden: true,
          },
        }}
        options={{
          bundlerTimeOut: 90_000,
        }}
      >
        <HashUpdater />
        <SandpackLayout style={{ position: "relative" }}>
          <MonacoEditor />
          {/* <SandpackCodeEditor style={{ height: "100vh" }} /> */}
          <SandpackPreview
            style={{ height: "100vh" }}
            actionsChildren={<DownloadButton />}
          />
          <PDFViewer />
        </SandpackLayout>
      </SandpackProvider>
    </div>
  );
}

function DownloadButton() {
  const [html, setHtml] = useState<string | null>(null);

  useEffect(() => {
    function handleMessage(event: MessageEvent<any>) {
      if (
        typeof event.data !== "object" ||
        event.data.type !== "rendered-to-html" ||
        typeof event.data.html !== "string"
      ) {
        return;
      }

      setHtml(event.data.html);
    }

    window.addEventListener("message", handleMessage);

    return () => {
      window.removeEventListener("message", handleMessage);
    };
  }, []);

  return (
    <form
      action="http://localhost:3000/pdf"
      method="POST"
      target="_blank"
      encType="text/plain"
    >
      <input type="hidden" name="<!--html" value={"--!>\n" + html} />
      <button className="sandpack-button" type="submit">
        Download PDF
      </button>
    </form>
  );
}

function HashUpdater() {
  const { code } = useActiveCode();

  useEffect(() => {
    window.history.replaceState(null, "", `#${btoa(code)}`);
  }, [code]);

  return null;
}

const source =
  typeof window !== "undefined" && window.location.hash
    ? atob(window.location.hash.slice(1))
    : `
import { CSS, PageBottom, PageBreak, Tailwind } from "@fileforge/react-print";
import * as React from "react";
// @ts-ignore
import { render } from "./render";

// No JSX syntax highlighting sadly, I tried

type SectionProps = {
  children: React.ReactNode;
};

const Section = ({ children }: SectionProps) => (
  <div className="mt-8 mx-6">{children}</div>
);

type SectionHeadingProps = {
  children: React.ReactNode;
};

const SectionHeading = ({ children }: SectionHeadingProps) => (
  <h2 className="bg-yellow-400 text-gray-900 font-extrabold py-2 px-4 uppercase">
    {children}
  </h2>
);

type ExperienceItemProps = {
  title: string;
  role: string;
  date: string;
  link: string;
  displayLink?: string;
  className?: string;
  children: React.ReactNode;
};

const ExperienceItem = ({
  title,
  role,
  date,
  link,
  displayLink,
  className,
  children,
}: ExperienceItemProps) => (
  <div className={\`mt-4 break-inside-avoid \${className || ""}\`}>
    <h3 className="font-bold">{title}</h3>
    <span className="text-gray-400">
      {role} | {date}
    </span>
    <a href={link} className="underline text-yellow-400 ml-2">
      {displayLink || link}
    </a>
    <p className="mt-2">{children}</p>
  </div>
);

type EducationItemProps = {
  school: string;
  degree: string;
  date: string;
};

const EducationItem = ({ school, degree, date }: EducationItemProps) => (
  <div className="mt-4 break-inside-avoid">
    <h3 className="font-bold">{degree}</h3>
    <span className="text-gray-400">
      {school} | {date}
    </span>
  </div>
);

type ListSectionProps = {
  title: string;
  items: string[];
};

const ListSection = ({ title, items }: ListSectionProps) => (
  <Section>
    <SectionHeading>{title}</SectionHeading>
    <ul className="list-disc pl-5 mt-2">
      {items.map((item, index) => (
        <li key={index}>{item}</li>
      ))}
    </ul>
  </Section>
);

export default function Document() {
  return (
    <Tailwind>
      <CSS>{\`
        body {
          background-color: #1a1a1a;
          color: #ffffff;
        }
        .onedoc-page-bottom {
          position: fixed;
          bottom: 0px;
          width: unset;
          height: unset;
        }
      \`}</CSS>

      <Section>
        <div className="text-4xl font-bold mt-6 mb-2">
          Mr. <span className="text-yellow-400">Balls</span>
        </div>
        <div className="text-lg text-gray-300">
          Professional Software Engineer
        </div>
        <div className="text-lg text-gray-300">
          Specializing in Yapping and Ballin'
        </div>
        <div className="mt-4">
          <SectionHeading>Summary</SectionHeading>
          <p className="mt-2">
            Experienced software engineer with a unique specialization in
            "yapping" and "ballin'". Known for delivering engaging user
            experiences, Mr. Balls contributed to the infamous "Scrap Mechanic
            Casino" project, introducing gamification that, while controversial,
            was undeniably effective at captivating young users.
          </p>
        </div>
      </Section>

      <ListSection
        title="Skills"
        items={[
          "Yapping Expertise",
          "Ballin' Proficiency",
          "Full-Stack Development (TypeScript, JavaScript, Bun, Node.js, Next.js, Hono, htmx)",
          "Low-Level Programming (C++, x86_64 Assembly, Lua, Rust)",
          "Microsoft Technologies (Win32 API, C#, VB.NET, PowerShell)",
          "Front-End Development (React, TailwindCSS)",
          "Backend Systems Architecture",
          "Casino Mechanics Design",
          "More Yapping",
          "Festo Automation Suite",
          "Submitting Sanity Flags",
          "Doomfist",
          "Putting TypeScript in places it shouldn't be",
        ]}
      />

      <Section>
        <SectionHeading>Work Experience</SectionHeading>

        <ExperienceItem
          title="Scrap Mechanic Casino"
          role="Lead Software Engineer"
          date="April 2024"
          link="https://scrapmechanic.net/casino"
        >
          Led the development of an innovative casino project within the Scrap
          Mechanic game. Implemented engaging gambling systems that
          significantly increased user engagement, particularly among younger
          players. Unfortunately, 90% of gambling-addicted children quit right
          before they were about to hit it big.
        </ExperienceItem>

        <ExperienceItem
          title="ScrapPunks NFT Collection"
          role="Founder & CEO"
          date="April 2022"
          link="https://april-fools-2022.scrapmechanic.net/"
        >
          Developed and launched the ScrapPunks NFT collection on the Ethereum
          blockchain. Successfully orchestrated a large-scale pump-and-dump
          scheme, capitalizing on speculative hype around in-game assets. The
          project drew attention to blockchain-driven virtual collectibles.
        </ExperienceItem>

        <ExperienceItem
          title="Scrap Mechanic Network Protocol"
          role="Reverse Engineer"
          date="March 2023 - Ongoing"
          link="https://docs.scrapmods.io/docs/networking/packets/01-hello/"
          displayLink="https://docs.scrapmods.io/"
          className="pt-4"
        >
          Used C++ and the Win32 API to inject a DLL into the Scrap Mechanic
          game process. This DLL intercepted network traffic and forwarded it to
          a Python script for analysis. Based on this work, extensive
          documentation was created, and a{" "}
          <a
            href="https://github.com/Scrap-Mods/SM_Server"
            className="underline text-yellow-400"
          >
            dedicated server
          </a>{" "}
          is being developed in C#.
        </ExperienceItem>

        <ExperienceItem
          title="Self-Cleaning Bed"
          role="Robotics Minor"
          date="Sept 2023 - Jan 2024"
          link="https://youtu.be/hyMb6Sq1Fkg"
        >
          Developed an autonomous self-cleaning bed for hotel use. By flipping
          two mattresses, the bed cleans the dirty mattress underneath, saving
          hotel staff time and effort. Applied unique skills such as using
          TypeScript in non-traditional ways and discovering the limitations of
          Python outside of CTF challenges. Commissioned by Hotelschool The
          Hague.
        </ExperienceItem>
      </Section>

      <Section>
        <SectionHeading>Education</SectionHeading>
        <EducationItem
          school="Delft University of Technology"
          degree="BSc Computer Science and Engineering"
          date="2021-2025"
        />
        <EducationItem
          school="Delft University of Technology"
          degree="Robotics Minor"
          date="Sept 2023 - Jan 2024"
        />
      </Section>

      <ListSection
        title="Certifications"
        items={[
          "Certified Yapper - Advanced Level",
          "Master of Ballin'",
          "Outstanding use of vulnerable library versions",
        ]}
      />

      <ListSection
        title="Hobbies & Interests"
        items={[
          "Yapping at conferences and events",
          'Playing with balls ("Ballin\\'")',
          "Game development and casino mechanics",
          "Playing sourceless web and guessy stego CTF challenges",
        ]}
      />

      <PageBottom>
        <div className="text-gray-400 text-sm m-4">
          Mr. Balls - Yapping since 2024
        </div>
      </PageBottom>
    </Tailwind>
  );
}

render(<Document />);
`.trimStart();

const renderSource = `
import { compile } from "@fileforge/react-print";

let lastHtml: string | null = null;

export async function render(element: JSX.Element) {
  const html = await compile(element)

  if (html === lastHtml) {
    return;
  }

  window.parent.postMessage({
    type: "rendered-to-html",
    html
  }, "*");

  const res = await fetch("${typeof window !== "undefined" ? window.location.origin : "http://localhost:3000"}/pdf", {
    method: "POST",
    body: html
  });
  const buffer = await res.arrayBuffer();
  
  window.parent.postMessage({
    type: "render-pdf",
    buffer
  }, "*", [buffer]);

  lastHtml = html;
}
`.trimStart();

const indexSource = `
import "./App";
`.trimStart();
