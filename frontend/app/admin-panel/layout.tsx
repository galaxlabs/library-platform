import PanelShell from '../../components/PanelShell';

export default function AdminPanelLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <PanelShell
      active="admin-panel"
      eyebrow="Maktaba Ilmiah"
      title="Admin Panel"
      description="A modern control surface for governance, publishing, scholar review, provider routing, and platform configuration without the default Django-admin feel."
    >
      {children}
    </PanelShell>
  );
}
