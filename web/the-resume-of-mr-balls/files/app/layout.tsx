import { SandpackCSS } from "@/components/sandpack-styles";

import "./global.css";

export const metadata = {
  title: "ResumeSX",
  description: "Fine-tune your resume in React",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <SandpackCSS />
      </head>
      <body style={{ margin: 0 }}>{children}</body>
    </html>
  );
}
