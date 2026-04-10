import PanelShell from '../../../components/PanelShell';

export default function MyInstituteLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <PanelShell
      active="institutes"
      eyebrow="Maktaba Ilmiah"
      title="My Institute"
      description="View your institute, classes, subject offerings, and the members or private-library access that your role is allowed to see."
    >
      {children}
    </PanelShell>
  );
}
