import PanelShell from '../../components/PanelShell';

export default function LibraryLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <PanelShell
      active="library"
      eyebrow="Maktaba Ilmiah"
      title="Library"
      description="Browse public and institute books, inspect references and chunks, and move straight into grounded study from the same library surface."
    >
      {children}
    </PanelShell>
  );
}
