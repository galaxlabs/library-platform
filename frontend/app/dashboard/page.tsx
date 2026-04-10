'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

import RequireAuth from '../../components/RequireAuth';
import { SurfaceCard, StatusBadge } from '../../components/ui';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../lib/api';

type DashboardData = {
  my_books: number;
  ingestion_jobs: number;
  recent_queries_count: number;
  institutes_count: number;
  recent_books: Array<{ public_id: string; title: string; review_status: string; visibility: string }>;
  recent_ingestion_jobs: Array<{ public_id: string; status: string; current_stage: string; book__title: string }>;
  recent_queries: Array<{ public_id: string; question: string; detected_subject: string; search_scope: string }>;
  scholar_profile?: { verification_status: string; review_count: number; trust_score: string } | null;
};

export default function DashboardPage() {
  const { user } = useAuth();
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      try {
        const response = await api.get('/analytics/dashboard/');
        setData(response.data);
      } catch {
        setError('Could not load the dashboard summary.');
      }
    };

    load();
  }, []);

  const statCards = [
    { label: 'Books', value: data?.my_books ?? 0 },
    { label: 'Ingestion Jobs', value: data?.ingestion_jobs ?? 0 },
    { label: 'Questions', value: data?.recent_queries_count ?? 0 },
    { label: 'Institutes', value: data?.institutes_count ?? 0 },
  ];

  return (
    <RequireAuth>
      <div className="grid gap-6">
        <section className="glass-panel rounded-[2rem] p-6 md:p-8">
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">Overview</p>
          <div className="mt-3 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <h2 className="text-4xl font-extrabold tracking-[-0.06em] text-slate-950">
                {user?.arabic_name || user?.full_name || 'Learning Workspace'}
              </h2>
              <p className="mt-3 max-w-2xl text-sm leading-7 text-slate-600">
                Track your books, ingestion jobs, grounded answers, institute access, and scholar status from one place.
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <Link href="/upload" className="rounded-[1rem] bg-slate-950 px-4 py-3 text-sm font-semibold text-white">
                Upload a book
              </Link>
              <Link href="/chat" className="rounded-[1rem] bg-white px-4 py-3 text-sm font-semibold text-slate-900 ring-1 ring-slate-200">
                Ask grounded Q&A
              </Link>
            </div>
          </div>
        </section>

        {error ? <div className="rounded-[1.4rem] border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div> : null}

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {statCards.map((item) => (
            <div key={item.label} className="rounded-[1.6rem] border border-slate-200 bg-white/85 p-5">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">{item.label}</p>
              <p className="mt-3 text-3xl font-bold tracking-[-0.05em] text-slate-950">{item.value}</p>
            </div>
          ))}
        </div>

        <div className="grid gap-6 xl:grid-cols-2">
          <SurfaceCard title="Recent Books" eyebrow="Library">
            <div className="grid gap-3">
              {(data?.recent_books ?? []).map((book) => (
                <Link key={book.public_id} href={`/library/${book.public_id}`} className="rounded-[1.2rem] border border-slate-200 bg-[rgba(247,244,238,0.9)] p-4">
                  <div className="flex items-center justify-between gap-3">
                    <p className="font-semibold text-slate-900">{book.title}</p>
                    <StatusBadge>{book.review_status}</StatusBadge>
                  </div>
                  <p className="mt-2 text-sm text-slate-600">{book.visibility}</p>
                </Link>
              ))}
              {!data?.recent_books?.length ? <p className="text-sm text-slate-600">No books uploaded yet.</p> : null}
            </div>
          </SurfaceCard>

          <SurfaceCard title="Recent Ingestion Jobs" eyebrow="Pipeline">
            <div className="grid gap-3">
              {(data?.recent_ingestion_jobs ?? []).map((job) => (
                <div key={job.public_id} className="rounded-[1.2rem] border border-slate-200 bg-[rgba(247,244,238,0.9)] p-4">
                  <div className="flex items-center justify-between gap-3">
                    <p className="font-semibold text-slate-900">{job.book__title || 'Book upload'}</p>
                    <StatusBadge tone={job.status === 'failed' ? 'danger' : job.status === 'review_pending' ? 'warning' : 'neutral'}>
                      {job.status}
                    </StatusBadge>
                  </div>
                  <p className="mt-2 text-sm text-slate-600">Current stage: {job.current_stage}</p>
                </div>
              ))}
              {!data?.recent_ingestion_jobs?.length ? <p className="text-sm text-slate-600">No ingestion jobs yet.</p> : null}
            </div>
          </SurfaceCard>

          <SurfaceCard title="Recent Questions" eyebrow="Q&A">
            <div className="grid gap-3">
              {(data?.recent_queries ?? []).map((query) => (
                <div key={query.public_id} className="rounded-[1.2rem] border border-slate-200 bg-[rgba(247,244,238,0.9)] p-4">
                  <p className="font-semibold text-slate-900">{query.question}</p>
                  <p className="mt-2 text-sm text-slate-600">
                    Scope: {query.search_scope} {query.detected_subject ? `| Subject: ${query.detected_subject}` : ''}
                  </p>
                </div>
              ))}
              {!data?.recent_queries?.length ? <p className="text-sm text-slate-600">No questions asked yet.</p> : null}
            </div>
          </SurfaceCard>

          <SurfaceCard title="Scholar Status" eyebrow="Review">
            {data?.scholar_profile ? (
              <div className="grid gap-3">
                <div className="flex flex-wrap gap-2">
                  <StatusBadge tone={data.scholar_profile.verification_status === 'verified' ? 'success' : 'warning'}>
                    {data.scholar_profile.verification_status}
                  </StatusBadge>
                  <StatusBadge>Reviews: {data.scholar_profile.review_count}</StatusBadge>
                  <StatusBadge>Trust: {data.scholar_profile.trust_score}</StatusBadge>
                </div>
                <Link href="/scholars" className="text-sm font-semibold text-emerald-800">
                  Open scholar profile
                </Link>
              </div>
            ) : (
              <div>
                <p className="text-sm leading-7 text-slate-600">
                  No scholar profile yet. You can apply for verification and review source-grounded answers from the scholar page.
                </p>
                <Link href="/scholars" className="mt-4 inline-flex text-sm font-semibold text-emerald-800">
                  Go to scholar profile
                </Link>
              </div>
            )}
          </SurfaceCard>
        </div>
      </div>
    </RequireAuth>
  );
}
