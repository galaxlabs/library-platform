import PanelShell from '../../components/PanelShell';

export default function UploadLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <PanelShell
      active="upload"
      eyebrow="Maktaba Ilmiah"
      title="Upload Book"
      description="Upload a source file, complete the mandatory metadata form, and submit the book into the ingestion pipeline with visible status."
    >
      {children}
    </PanelShell>
  );
}
