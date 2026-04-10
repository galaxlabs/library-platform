'use client';

import { useEffect, useState } from 'react';

import RequireAuth from '../../../components/RequireAuth';
import { StatusBadge, SurfaceCard } from '../../../components/ui';
import api, { extractResults } from '../../../lib/api';

type BookDetail = {
  public_id: string;
  title: string;
  arabic_title: string;
  author: string;
  arabic_author_name: string;
  primary_subject_name: string;
  language: string;
  level: string;
  visibility: string;
  review_status: string;
  latest_metadata?: { identity?: Record<string, string>; classification?: Record<string, string> } | null;
};

type Chunk = { public_id: string; page_number: number | null; section_title: string; content: string; chunk_type: string };

export default function BookDetailPage({ params }: { params: { publicId: string } }) {
  const [book, setBook] = useState<BookDetail | null>(null);
  const [chunks, setChunks] = useState<Chunk[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      try {
        const [bookResponse, chunksResponse] = await Promise.all([
          api.get(`/library/books/${params.publicId}/`),
          api.get(`/library/books/${params.publicId}/chunks/`),
        ]);
        setBook(bookResponse.data);
        setChunks(extractResults<Chunk>(chunksResponse.data));
      } catch {
        setError('Could not load this book.');
      }
    };
    load();
  }, [params.publicId]);

  return (
    <RequireAuth>
      <div className="grid gap-6">
        {error ? <div className="rounded-[1.4rem] border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div> : null}
        {book ? (
          <>
            <SurfaceCard title={book.arabic_title || book.title} eyebrow="Book detail">
              <div className="flex flex-wrap gap-2">
                <StatusBadge>{book.review_status}</StatusBadge>
                <StatusBadge tone={book.visibility === 'public' ? 'success' : 'warning'}>{book.visibility}</StatusBadge>
              </div>
              <p className="mt-4 text-sm leading-7 text-slate-600">
                {book.author || book.arabic_author_name || 'Unknown author'} {book.primary_subject_name ? `| ${book.primary_subject_name}` : ''} {book.level ? `| ${book.level}` : ''} {book.language ? `| ${book.language}` : ''}
              </p>
            </SurfaceCard>

            <SurfaceCard title="References and Chunks" eyebrow="Evidence">
              <div className="grid gap-3">
                {chunks.slice(0, 12).map((chunk) => (
                  <div key={chunk.public_id} className="rounded-[1.3rem] border border-slate-200 bg-[rgba(247,244,238,0.9)] p-4">
                    <div className="flex items-center justify-between gap-3">
                      <p className="font-semibold text-slate-900">{chunk.section_title || chunk.chunk_type}</p>
                      {chunk.page_number ? <StatusBadge>Page {chunk.page_number}</StatusBadge> : null}
                    </div>
                    <p className="mt-2 text-sm leading-7 text-slate-600">{chunk.content}</p>
                  </div>
                ))}
                {!chunks.length ? <p className="text-sm text-slate-600">No extracted chunks yet. The ingestion pipeline may still be pending review or OCR.</p> : null}
              </div>
            </SurfaceCard>
          </>
        ) : null}
      </div>
    </RequireAuth>
  );
}
