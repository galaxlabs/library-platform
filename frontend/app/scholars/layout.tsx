import PanelShell from '../../components/PanelShell';

export default function ScholarsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <PanelShell
      active="scholars"
      eyebrow="Maktaba Ilmiah"
      title="Scholar Profile"
      description="Manage scholar verification details, review history, and the current queue of answers that still need scholarly judgment."
    >
      {children}
    </PanelShell>
  );
}
