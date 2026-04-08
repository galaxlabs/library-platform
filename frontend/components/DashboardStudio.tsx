'use client';

import Link from 'next/link';

type PanelMode = 'user' | 'admin';

type DashboardStudioProps = {
  mode: PanelMode;
};

const userHighlights = [
  {
    title: 'Today’s Study Flow',
    value: '4 guided blocks',
    detail: 'Nahw lesson, verified answer review, focused practice, and a live revision queue.',
  },
  {
    title: 'Reading Focus',
    value: 'Sharh + Sources',
    detail: 'Open commentary, compare passages, and keep citations visible while you study.',
  },
  {
    title: 'Saved Evidence',
    value: '18 passages',
    detail: 'Collected across books, notes, and scholar-reviewed explanations for quick recall.',
  },
];

const adminHighlights = [
  {
    title: 'Publishing Queue',
    value: '12 pending items',
    detail: 'Books, answer reviews, and draft skill packs waiting for moderation or approval.',
  },
  {
    title: 'Model Governance',
    value: 'Sensitive mode active',
    detail: 'Grounded-answer enforcement and scholar-priority rules are visible in one panel.',
  },
  {
    title: 'Provider Health',
    value: '3 active routes',
    detail: 'System, institute, and private model routing can be tuned without leaving the workspace.',
  },
];

const adminOperations = [
  {
    title: 'Content Review',
    value: '28 items',
    detail: 'Triage newly ingested books, draft skills, and flagged answers from one moderation lane.',
  },
  {
    title: 'Scholar Escalations',
    value: '6 active',
    detail: 'Keep disputed answers and policy-sensitive claims visible until they receive a final ruling.',
  },
  {
    title: 'Provider Routing',
    value: 'Stable',
    detail: 'Route institutes, private keys, and system defaults with clearer fallback visibility.',
  },
  {
    title: 'Release Window',
    value: 'Tonight 20:00',
    detail: 'Scheduled publishing, queue freeze, and rollback notes remain grouped in one release surface.',
  },
];

const adminRail = [
  {
    label: 'Moderation Queue',
    hint: 'Pending',
    detail: 'Books, answers, and skill packs waiting for a decision.',
  },
  {
    label: 'Platform Health',
    hint: 'Live',
    detail: 'Provider status, failed jobs, and queue throughput.',
  },
  {
    label: 'Policy Overrides',
    hint: 'Watch',
    detail: 'Sensitive-answer rules and institute-specific governance.',
  },
];

const adminWorkflow = [
  'Review scholar escalations before publication changes.',
  'Approve ingestion batches with source visibility and rollback notes.',
  'Adjust provider routing only after checking queue health and institute impact.',
  'Publish branded institute settings after moderation passes green.',
];

const userModules = [
  'My Institute',
  'My Class / Darjah',
  'Practice Zone',
  'Saved Questions',
  'Reference Drawer',
  'Revision Lists',
];

const adminModules = [
  'Book Workflow',
  'Scholar Verification',
  'Provider Routing',
  'Answer Policies',
  'Publishing Control',
  'Institute Branding',
];

export default function DashboardStudio({ mode }: DashboardStudioProps) {
  const isAdmin = mode === 'admin';
  const highlights = isAdmin ? adminHighlights : userHighlights;
  const modules = isAdmin ? adminModules : userModules;
  const layoutCards = isAdmin
    ? [
        'Review queue and decision stream',
        'Book ingestion monitor',
        'Provider routing and key scopes',
        'Institute and role controls',
      ]
    : [
        'Answer stream with citations first',
        'Book reading and notes rail',
        'Practice and revision cards',
        'Institute and class context rail',
      ];

  return (
    <div className="grid gap-6 xl:grid-cols-[320px_minmax(0,1fr)]">
      <aside className="panel-sidebar rounded-[2rem] p-5 lg:p-6 xl:sticky xl:top-6 xl:self-start">
        <div
          className={`rounded-[1.7rem] p-5 text-white ${
            isAdmin
              ? 'bg-[linear-gradient(145deg,#172033_0%,#1f5f57_55%,#d48d3f_140%)]'
              : 'bg-slate-950'
          }`}
        >
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-emerald-200">
            Maktaba Ilmiah
          </p>
          <h1 className="mt-3 text-3xl font-extrabold tracking-[-0.06em]">
            {isAdmin ? 'Admin Panel' : 'User Dashboard'}
          </h1>
          <p className="mt-3 text-sm leading-7 text-slate-300">
            {isAdmin
              ? 'A modern governance workspace for moderation, model control, scholar review, and publishing.'
              : 'A modern scholarly study workspace for reading, retrieval, evidence review, and guided practice.'}
          </p>
        </div>

        <div className="mt-6 grid gap-3">
          <Link
            href="/dashboard"
            className={`rounded-[1.3rem] border px-4 py-4 text-left transition ${
              !isAdmin
                ? 'border-emerald-800 bg-emerald-950 text-white shadow-[0_18px_36px_rgba(21,72,61,0.24)]'
                : 'border-slate-200 bg-white/75 text-slate-700 hover:bg-white'
            }`}
          >
            <div className="text-sm font-semibold">User Panel</div>
            <div className="mt-2 text-sm opacity-80">
              Student and learner-facing study surface with books, answers, and revision flows.
            </div>
          </Link>
          <Link
            href="/admin-panel"
            className={`rounded-[1.3rem] border px-4 py-4 text-left transition ${
              isAdmin
                ? 'border-amber-700 bg-[linear-gradient(135deg,#b66d24_0%,#d79144_100%)] text-white shadow-[0_18px_36px_rgba(183,121,51,0.28)]'
                : 'border-slate-200 bg-white/75 text-slate-700 hover:bg-white'
            }`}
          >
            <div className="text-sm font-semibold">Admin Panel</div>
            <div className="mt-2 text-sm opacity-80">
              Policy, publishing, provider routing, moderation, and institutional controls.
            </div>
          </Link>
        </div>

        <div className="mt-8 rounded-[1.5rem] border border-slate-200 bg-white/70 p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">
            Panel Modules
          </p>
          <div className="mt-4 flex flex-wrap gap-2">
            {modules.map((module) => (
              <span
                key={module}
                className="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-600"
              >
                {module}
              </span>
            ))}
          </div>
        </div>

        {isAdmin ? (
          <div className="mt-6 rounded-[1.6rem] border border-slate-200 bg-[rgba(250,248,242,0.92)] p-4">
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">
              Command Rail
            </p>
            <div className="mt-4 space-y-3">
              {adminRail.map((item) => (
                <div
                  key={item.label}
                  className="rounded-[1.2rem] border border-slate-200 bg-white/90 p-4"
                >
                  <div className="flex items-center justify-between gap-4">
                    <p className="text-sm font-semibold text-slate-900">{item.label}</p>
                    <span className="rounded-full bg-slate-100 px-2.5 py-1 text-[10px] font-bold uppercase tracking-[0.18em] text-slate-600">
                      {item.hint}
                    </span>
                  </div>
                  <p className="mt-2 text-sm leading-6 text-slate-600">{item.detail}</p>
                </div>
              ))}
            </div>
          </div>
        ) : null}
      </aside>

      <section className="grid gap-6">
        <div className={`rounded-[2rem] p-6 md:p-8 ${isAdmin ? 'admin-stage' : 'glass-panel'}`}>
          <div className="flex flex-col gap-6 xl:flex-row xl:items-end xl:justify-between">
            <div className="max-w-2xl">
              <p className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-500">
                {isAdmin ? 'Governance Workspace' : 'Scholarly Learning Workspace'}
              </p>
              <h2 className="mt-3 text-4xl font-extrabold tracking-[-0.06em] text-slate-950 md:text-5xl">
                {isAdmin
                  ? 'A cleaner operations layout for the front admin'
                  : 'Welcome to Maktaba Ilmiah'}
              </h2>
              <p className="mt-4 max-w-xl text-sm leading-7 text-slate-600 md:text-base">
                {isAdmin
                  ? 'The admin surface now centers decisions, operational status, and release controls so the workspace feels designed instead of improvised.'
                  : 'Designed with stronger typography, clearer reading rhythm, and a calmer panel layout for serious learners.'}
              </p>
            </div>
            {isAdmin ? (
              <div className="grid gap-3 sm:grid-cols-3 xl:min-w-[420px]">
                <div className="rounded-[1.4rem] border border-white/70 bg-white/80 px-4 py-4">
                  <p className="text-[10px] font-bold uppercase tracking-[0.22em] text-slate-500">
                    Review SLA
                  </p>
                  <p className="mt-2 text-2xl font-bold tracking-[-0.05em] text-slate-950">4h</p>
                </div>
                <div className="rounded-[1.4rem] border border-white/70 bg-white/80 px-4 py-4">
                  <p className="text-[10px] font-bold uppercase tracking-[0.22em] text-slate-500">
                    Failed Jobs
                  </p>
                  <p className="mt-2 text-2xl font-bold tracking-[-0.05em] text-slate-950">2</p>
                </div>
                <div className="rounded-[1.4rem] border border-white/70 bg-white/80 px-4 py-4">
                  <p className="text-[10px] font-bold uppercase tracking-[0.22em] text-slate-500">
                    Release State
                  </p>
                  <p className="mt-2 text-2xl font-bold tracking-[-0.05em] text-slate-950">Green</p>
                </div>
              </div>
            ) : (
              <div className="rounded-[1.5rem] border border-slate-200 bg-white/80 px-5 py-4">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">
                  Active Layout
                </p>
                <p className="mt-2 text-2xl font-bold tracking-[-0.04em] text-slate-900">
                  Learning Studio
                </p>
              </div>
            )}
          </div>
        </div>

        <div className="grid gap-4 lg:grid-cols-3">
          {highlights.map((item) => (
            <div
              key={item.title}
              className="rounded-[1.6rem] border border-slate-200 bg-white/85 p-5 shadow-[0_18px_40px_rgba(40,39,33,0.08)]"
            >
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">
                {item.title}
              </p>
              <p className="mt-4 text-3xl font-bold tracking-[-0.05em] text-slate-950">
                {item.value}
              </p>
              <p className="mt-3 text-sm leading-7 text-slate-600">{item.detail}</p>
            </div>
          ))}
        </div>

        {isAdmin ? (
          <div className="grid gap-6 xl:grid-cols-[1.08fr_0.92fr]">
            <div className="glass-panel rounded-[2rem] p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">
                    Operations Board
                  </p>
                  <h3 className="mt-2 text-2xl font-bold tracking-[-0.04em] text-slate-950">
                    Core control surfaces
                  </h3>
                </div>
                <span className="rounded-full bg-slate-950 px-3 py-1 text-xs font-semibold text-white">
                  Front Admin
                </span>
              </div>

              <div className="mt-6 grid gap-4 md:grid-cols-2">
                {adminOperations.map((item) => (
                  <div
                    key={item.title}
                    className="rounded-[1.5rem] border border-slate-200 bg-white/85 p-5"
                  >
                    <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">
                      {item.title}
                    </p>
                    <p className="mt-4 text-3xl font-bold tracking-[-0.05em] text-slate-950">
                      {item.value}
                    </p>
                    <p className="mt-3 text-sm leading-7 text-slate-600">{item.detail}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="glass-panel rounded-[2rem] p-6">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">
                Release Workflow
              </p>
              <div className="mt-5 space-y-4">
                {adminWorkflow.map((item, index) => (
                  <div
                    key={item}
                    className="flex gap-4 rounded-[1.4rem] border border-slate-200 bg-white/85 p-4"
                  >
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[var(--brand-soft)] text-sm font-bold text-[var(--brand)]">
                      {index + 1}
                    </div>
                    <p className="pt-1 text-sm leading-7 text-slate-700">{item}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
            <div className="glass-panel rounded-[2rem] p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">
                    Layout Blueprint
                  </p>
                  <h3 className="mt-2 text-2xl font-bold tracking-[-0.04em] text-slate-950">
                    Reading-first panel map
                  </h3>
                </div>
                <span className="rounded-full bg-slate-950 px-3 py-1 text-xs font-semibold text-white">
                  Modern Panel
                </span>
              </div>

              <div className="mt-6 grid gap-4 md:grid-cols-2">
                {layoutCards.map((item) => (
                  <div
                    key={item}
                    className="rounded-[1.4rem] border border-slate-200 bg-white/80 p-4 text-sm font-medium text-slate-700"
                  >
                    {item}
                  </div>
                ))}
              </div>
            </div>

            <div className="glass-panel rounded-[2rem] p-6">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">
                Typography and Layout
              </p>
              <div className="mt-5 space-y-4">
                <div className="rounded-[1.4rem] bg-slate-950 p-5 text-white">
                  <p className="text-xs uppercase tracking-[0.24em] text-emerald-300">
                    Editorial Hierarchy
                  </p>
                  <p className="mt-3 text-sm leading-7 text-slate-200">
                    Large headings, soft panel contrast, and wider spacing make the workspace feel premium instead of utilitarian.
                  </p>
                </div>
                <div className="rounded-[1.4rem] border border-slate-200 bg-white/80 p-5">
                  <p className="text-xs uppercase tracking-[0.24em] text-slate-500">
                    No Django Admin Feel
                  </p>
                  <p className="mt-3 text-sm leading-7 text-slate-600">
                    This panel is designed as a branded product surface for Maktaba Ilmiah, not as a default framework back office.
                  </p>
                </div>
                <div className="rounded-[1.4rem] border border-slate-200 bg-white/80 p-5">
                  <p className="text-xs uppercase tracking-[0.24em] text-slate-500">
                    Config-Ready Structure
                  </p>
                  <p className="mt-3 text-sm leading-7 text-slate-600">
                    Modules are grouped as configurable product sections so future forms, policies, and workflows can slot in directly.
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </section>
    </div>
  );
}
