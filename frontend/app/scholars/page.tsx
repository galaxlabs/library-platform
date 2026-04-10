'use client';

import { FormEvent, useEffect, useState } from 'react';

import RequireAuth from '../../components/RequireAuth';
import { StatusBadge, SurfaceCard } from '../../components/ui';
import api, { extractResults } from '../../lib/api';

type ScholarProfile = {
  full_name: string;
  arabic_name: string;
  specialization: string;
  short_bio: string;
  verification_status: string;
};

type ReviewQueue = {
  pending_answers: Array<{ answer_public_id: string; question: string; verification_status: string; confidence: string }>;
  recent_reviews: Array<{ id: number; answer_question: string; decision: string; commentary: string }>;
};

export default function ScholarsPage() {
  const [profile, setProfile] = useState<ScholarProfile | null>(null);
  const [queue, setQueue] = useState<ReviewQueue | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      try {
        const [profileResponse, queueResponse] = await Promise.all([
          api.get('/scholars/me/'),
          api.get('/scholars/review-queue/'),
        ]);
        setProfile(profileResponse.data);
        setQueue(queueResponse.data);
      } catch {
        try {
          const profileResponse = await api.get('/scholars/me/');
          setProfile(profileResponse.data);
        } catch {
          setError('Could not load scholar data.');
        }
      }
    };

    load();
  }, []);

  const submitApplication = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    try {
      const response = await api.post('/scholars/applications/', {
        full_name: formData.get('full_name'),
        arabic_name: formData.get('arabic_name'),
        specialization: formData.get('specialization'),
        short_bio: formData.get('short_bio'),
      });
      setProfile(response.data);
    } catch (err: any) {
      setError(err?.response?.data?.error?.message || 'Could not submit the scholar application.');
    }
  };

  return (
    <RequireAuth>
      <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
        <SurfaceCard title="Scholar Profile" eyebrow="Profile">
          {profile ? (
            <div className="grid gap-3">
              <div className="flex flex-wrap gap-2">
                <StatusBadge tone={profile.verification_status === 'verified' ? 'success' : 'warning'}>
                  {profile.verification_status}
                </StatusBadge>
              </div>
              <p className="text-sm text-slate-700">{profile.full_name || profile.arabic_name || 'Scholar profile'}</p>
              <p className="text-sm text-slate-600">{profile.specialization || 'No specialization added yet.'}</p>
              <p className="text-sm leading-7 text-slate-600">{profile.short_bio || 'No scholar bio yet.'}</p>
            </div>
          ) : null}

          <form onSubmit={submitApplication} className="mt-6 grid gap-3">
            <input name="full_name" className="h-12 rounded-[1rem] border border-slate-200 bg-white px-4 text-sm" placeholder="Full name" defaultValue={profile?.full_name || ''} />
            <input name="arabic_name" className="h-12 rounded-[1rem] border border-slate-200 bg-white px-4 text-sm" placeholder="Arabic name" defaultValue={profile?.arabic_name || ''} />
            <input name="specialization" className="h-12 rounded-[1rem] border border-slate-200 bg-white px-4 text-sm" placeholder="Specialization" defaultValue={profile?.specialization || ''} />
            <textarea name="short_bio" className="min-h-[120px] rounded-[1rem] border border-slate-200 bg-white px-4 py-3 text-sm" placeholder="Short bio" defaultValue={profile?.short_bio || ''} />
            <button type="submit" className="rounded-[1rem] bg-slate-950 px-4 py-3 text-sm font-semibold text-white">
              Submit verification application
            </button>
          </form>
          {error ? <div className="mt-4 rounded-[1.2rem] border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div> : null}
        </SurfaceCard>

        <SurfaceCard title="Scholar Review Queue" eyebrow="Queue">
          {queue?.pending_answers?.length ? (
            <div className="grid gap-3">
              {queue.pending_answers.map((answer) => (
                <div key={answer.answer_public_id} className="rounded-[1.2rem] border border-slate-200 bg-[rgba(247,244,238,0.9)] p-4">
                  <div className="flex items-center justify-between gap-3">
                    <p className="font-semibold text-slate-900">{answer.question}</p>
                    <StatusBadge tone="warning">{answer.verification_status}</StatusBadge>
                  </div>
                  <p className="mt-2 text-sm text-slate-600">Confidence: {answer.confidence}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm leading-7 text-slate-600">
              No scholar queue items are currently visible for this account. Verified scholars will see pending reviewed answers here when they exist.
            </p>
          )}
        </SurfaceCard>
      </div>
    </RequireAuth>
  );
}
