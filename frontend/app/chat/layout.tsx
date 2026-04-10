import PanelShell from '../../components/PanelShell';

export default function ChatLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <PanelShell
      active="chat"
      eyebrow="Maktaba Ilmiah"
      title="Ask AI"
      description="Ask simple study questions, read source-based answers, and keep your recent chat history in one place."
    >
      {children}
    </PanelShell>
  );
}
