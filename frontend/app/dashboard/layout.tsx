import PanelShell from '../../components/PanelShell';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <PanelShell
      active="dashboard"
      eyebrow="Maktaba Ilmiah"
      title="User Dashboard"
      description="A refined scholarly workspace with stronger typography, calmer spacing, and a modern panel layout for reading, evidence review, and guided learning."
    >
      {children}
    </PanelShell>
  );
}
