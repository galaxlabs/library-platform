'use client';

import { useEffect, useState } from 'react';

import RequireAuth from '../../../components/RequireAuth';
import { SurfaceCard } from '../../../components/ui';
import { useAuth } from '../../../contexts/AuthContext';
import api, { extractResults } from '../../../lib/api';

type Institute = { public_id: string; name: string; description: string; city: string; country: string };
type ClassItem = { public_id: string; name: string; language_pair: string; level: number };
type MemberItem = { public_id: string; user_full_name: string; role: string; class_darjah_name: string };

export default function MyInstitutePage() {
  const { user } = useAuth();
  const [institute, setInstitute] = useState<Institute | null>(null);
  const [classes, setClasses] = useState<ClassItem[]>([]);
  const [members, setMembers] = useState<MemberItem[]>([]);

  useEffect(() => {
    const load = async () => {
      try {
        const instituteResponse = await api.get('/institutes/');
        const instituteItems = extractResults<Institute>(instituteResponse.data);
        const currentInstitute = instituteItems.find((item) => item.public_id === user?.institute_public_id) || instituteItems[0] || null;
        setInstitute(currentInstitute);

        if (currentInstitute) {
          const [classesResponse, membersResponse] = await Promise.all([
            api.get('/institutes/classes/', { params: { institute: currentInstitute.public_id } }),
            api.get('/institutes/memberships/', { params: { institute: currentInstitute.public_id } }),
          ]);
          setClasses(extractResults<ClassItem>(classesResponse.data));
          setMembers(extractResults<MemberItem>(membersResponse.data));
        }
      } catch {
        setInstitute(null);
      }
    };

    load();
  }, [user?.institute_public_id]);

  return (
    <RequireAuth>
      <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
        <SurfaceCard title={institute?.name || 'My Institute'} eyebrow="Institute">
          <p className="text-sm leading-7 text-slate-600">
            {institute?.description || 'No institute details are available for this account yet.'}
          </p>
          {institute ? <p className="mt-3 text-sm text-slate-700">{[institute.city, institute.country].filter(Boolean).join(', ')}</p> : null}
        </SurfaceCard>

        <SurfaceCard title="Class / Darjah" eyebrow="Classes">
          <div className="grid gap-3">
            {classes.map((item) => (
              <div key={item.public_id} className="rounded-[1.2rem] border border-slate-200 bg-[rgba(247,244,238,0.9)] p-4">
                <p className="font-semibold text-slate-900">{item.name}</p>
                <p className="mt-2 text-sm text-slate-600">Level {item.level} | {item.language_pair}</p>
              </div>
            ))}
            {!classes.length ? <p className="text-sm text-slate-600">No class data is visible for this institute yet.</p> : null}
          </div>
        </SurfaceCard>

        <SurfaceCard title="Members" eyebrow="Institute members">
          <div className="grid gap-3">
            {members.map((item) => (
              <div key={item.public_id} className="rounded-[1.2rem] border border-slate-200 bg-[rgba(247,244,238,0.9)] p-4">
                <p className="font-semibold text-slate-900">{item.user_full_name}</p>
                <p className="mt-2 text-sm text-slate-600">{item.role} {item.class_darjah_name ? `| ${item.class_darjah_name}` : ''}</p>
              </div>
            ))}
            {!members.length ? <p className="text-sm text-slate-600">Member details are limited for your current role, or there are no active memberships to show.</p> : null}
          </div>
        </SurfaceCard>
      </div>
    </RequireAuth>
  );
}
