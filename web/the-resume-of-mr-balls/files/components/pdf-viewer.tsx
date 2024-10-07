import { memo, useCallback, useEffect, useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";

import "react-pdf/dist/Page/AnnotationLayer.css";
import "react-pdf/dist/Page/TextLayer.css";

pdfjs.GlobalWorkerOptions.workerSrc = `//cdn.jsdelivr.net/npm/pdfjs-dist@${pdfjs.version}/build/pdf.worker.js`;

const options: React.ComponentProps<typeof Document>["options"] = {
  cMapUrl: `https://cdn.jsdelivr.net/npm/pdfjs-dist@${pdfjs.version}/cmaps/`,
};

/**
 * PDFViewer component that listens for messages from the parent window
 */
export const PDFViewer = () => {
  const [files, setFiles] = useState<{ key: string; file: File }[]>([]);

  useEffect(() => {
    function handleMessage(event: MessageEvent<any>) {
      if (
        typeof event.data !== "object" ||
        event.data.type !== "render-pdf" ||
        !(event.data.buffer instanceof ArrayBuffer)
      ) {
        return;
      }

      const file = new File([event.data.buffer], "document.pdf", {
        type: "application/pdf",
      });

      setFiles((files) =>
        [
          {
            key: crypto.randomUUID(),
            file,
          },
        ]
          .concat(files)
          .slice(0, 2)
      );
    }

    window.addEventListener("message", handleMessage);

    return () => {
      window.removeEventListener("message", handleMessage);
    };
  }, []);

  const onLoadSuccessReal = useCallback((removeFilesOlderThan: File) => {
    setFiles((currentFiles) => {
      let index = 0;
      for (let i = 0; i < currentFiles.length; i++) {
        if (currentFiles[i].file === removeFilesOlderThan) {
          index = i;
          break;
        }
      }

      return currentFiles.slice(0, index + 1);
    });
  }, []);

  return (
    <div className="pdf-container">
      {files.map(({ key, file }) => (
        <PDF key={key} file={file} onLoadSuccessReal={onLoadSuccessReal} />
      ))}
    </div>
  );
};

/**
 * Wrapper around react-pdf's Document component to handle loading state
 */
const PDF = memo(
  ({
    file,
    onLoadSuccessReal,
  }: {
    file: File;
    onLoadSuccessReal?: (file: File) => void;
  }) => {
    const [numPages, setNumPages] = useState(0);
    const [loading, setLoading] = useState(true);

    return (
      <Document
        file={file}
        onLoadSuccess={(pdf) => setNumPages(pdf.numPages)}
        options={options}
        className={loading ? "hidden" : ""}
      >
        {Array.from(new Array(numPages), (_, index) => (
          <Page
            key={`page_${index + 1}`}
            pageNumber={index + 1}
            onRenderSuccess={() => {
              setLoading(false);
              if (loading) {
                onLoadSuccessReal?.(file);
              }
            }}
          />
        ))}
      </Document>
    );
  }
);
