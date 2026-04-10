'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

import RequireAuth from '../../components/RequireAuth';
import { StatusBadge, SurfaceCard } from '../../components/ui';
import api, { extractResults } from '../../lib/api';

type BookItem = {
  public_id: string;
  title: string;
  arabic_title: string;
  author: string;
  primary_subject_name: string;
  level: string;
  language: string;
  visibility: string;
  review_status: string;
};

export default function LibraryPage() {
  const [books, setBooks] = useState<BookItem[]>([]);
  const [filters, setFilters] = useState({ search: '', language: '', level: '', visibility: '' });
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      try {
        const response = await api.get('/library/books/', { params: filters });
        setBooks(extractResults<BookItem>(response.data));
      } catch {
        setError('Could not load the library right now.');
      }
    };
    load();
  }, [filters]);

  return (
    <RequireAuth>
      <div className="grid gap-6">
        <SurfaceCard title="Browse Books" eyebrow="Filters">
          <div className="grid gap-3 md:grid-cols-4">
            <input className="h-12 rounded-[1rem] border border-slate-200 bg-white px-4 text-sm" placeholder="Search title or author" value={filters.search} onChange={(e) => setFilters((current) => ({ ...current, search: e.target.value }))} />
            <input className="h-12 rounded-[1rem] border border-slate-200 bg-white px-4 text-sm" placeholder="Language" value={filters.language} onChange={(e) => setFilters((current) => ({ ...current, language: e.target.value }))} />
            <input className="h-12 rounded-[1rem] border border-slate-200 bg-white px-4 text-sm" placeholder="Level" value={filters.level} onChange={(e) => setFilters((current) => ({ ...current, level: e.target.value }))} />
            <select className="h-12 rounded-[1rem] border border-slate-200 bg-white px-4 text-sm" value={filters.visibility} onChange={(e) => setFilters((current) => ({ ...current, visibility: e.target.value }))}>
              <option value="">All visibility</option>
              <option value="public">Public</option>
              <option value="private">Private</option>
              <option value="institute">Institute</option>
            </select>
          </div>
        </SurfaceCard>

        {error ? <div className="rounded-[1.4rem] border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div> : null}

        <div className="grid gap-4 lg:grid-cols-2">
          {books.map((book) => (
            <Link key={book.public_id} href={`/library/${book.public_id}`} className="rounded-[1.8rem] border border-slate-200 bg-white/90 p-5 shadow-[0_18px_40px_rgba(40,39,33,0.08)]">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <p className="text-xl font-semibold text-slate-950">{book.arabic_title || book.title}</p>
                  <p className="mt-2 text-sm text-slate-600">{book.author || 'Unknown author'}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  <StatusBadge>{book.review_status}</StatusBadge>
                  <StatusBadge tone={book.visibility === 'public' ? 'success' : 'warning'}>{book.visibility}</StatusBadge>
                </div>
              </div>
              <p className="mt-4 text-sm text-slate-600">
                {book.primary_subject_name || 'General studies'} {book.level ? `| ${book.level}` : ''} {book.language ? `| ${book.language}` : ''}
              </p>
            </Link>
          ))}
          {!books.length ? <div className="rounded-[1.6rem] border border-slate-200 bg-white/85 p-6 text-sm text-slate-600">No books matched the current filters.</div> : null}
        </div>
      </div>
    </RequireAuth>
  );
}
