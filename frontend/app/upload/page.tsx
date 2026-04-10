'use client';

import { FormEvent, useState } from 'react';

import RequireAuth from '../../components/RequireAuth';
import { StatusBadge, SurfaceCard } from '../../components/ui';
import api from '../../lib/api';

type UploadResult = {
  bookPublicId?: string;
  ingestionPublicId?: string;
  ingestionStatus?: string;
};

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [form, setForm] = useState({
    title: '',
    arabicTitle: '',
    author: '',
    language: 'Arabic',
    level: '',
    visibility: 'public',
    metadataSummary: '',
  });
  const [result, setResult] = useState<UploadResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!file) {
      setError('Choose a source file before submitting the metadata form.');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const payload = new FormData();
      payload.append('title', form.title);
      payload.append('arabic_title', form.arabicTitle);
      payload.append('author', form.author);
      payload.append('language', form.language);
      payload.append('level', form.level);
      payload.append('visibility', form.visibility);
      payload.append('file', file);
      payload.append('file_kind', 'pdf');
      payload.append(
        'metadata_identity',
        JSON.stringify({
          title: form.title,
          arabic_title: form.arabicTitle,
          author: form.author,
          uploader_summary: form.metadataSummary,
        })
      );
      payload.append(
        'metadata_classification',
        JSON.stringify({
          language: form.language,
          level: form.level,
          visibility: form.visibility,
        })
      );

      const bookResponse = await api.post('/library/books/', payload, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      const ingestionResponse = await api.post('/ingestion/jobs/', {
        book_public_id: bookResponse.data.public_id,
        source_note: form.metadataSummary,
      });
      setResult({
        bookPublicId: bookResponse.data.public_id,
        ingestionPublicId: ingestionResponse.data.public_id,
        ingestionStatus: ingestionResponse.data.status,
      });
    } catch (err: any) {
      setError(err?.response?.data?.error?.message || 'Could not submit the upload flow.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <RequireAuth>
      <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
        <SurfaceCard title="Book Upload Wizard" eyebrow="Step 1 and 2">
          <form onSubmit={handleSubmit} className="grid gap-4">
            <input className="h-12 rounded-[1rem] border border-slate-200 bg-white px-4 text-sm" placeholder="Title" value={form.title} onChange={(e) => setForm((current) => ({ ...current, title: e.target.value }))} required />
            <input className="h-12 rounded-[1rem] border border-slate-200 bg-white px-4 text-sm" placeholder="Arabic title" value={form.arabicTitle} onChange={(e) => setForm((current) => ({ ...current, arabicTitle: e.target.value }))} />
            <input className="h-12 rounded-[1rem] border border-slate-200 bg-white px-4 text-sm" placeholder="Author" value={form.author} onChange={(e) => setForm((current) => ({ ...current, author: e.target.value }))} />
            <div className="grid gap-4 md:grid-cols-3">
              <input className="h-12 rounded-[1rem] border border-slate-200 bg-white px-4 text-sm" placeholder="Language" value={form.language} onChange={(e) => setForm((current) => ({ ...current, language: e.target.value }))} required />
              <input className="h-12 rounded-[1rem] border border-slate-200 bg-white px-4 text-sm" placeholder="Level" value={form.level} onChange={(e) => setForm((current) => ({ ...current, level: e.target.value }))} />
              <select className="h-12 rounded-[1rem] border border-slate-200 bg-white px-4 text-sm" value={form.visibility} onChange={(e) => setForm((current) => ({ ...current, visibility: e.target.value }))}>
                <option value="public">Public</option>
                <option value="private">Private</option>
                <option value="institute">Institute</option>
              </select>
            </div>
            <textarea className="min-h-[140px] rounded-[1rem] border border-slate-200 bg-white px-4 py-3 text-sm" placeholder="Mandatory metadata note: provenance, edition notes, or anything the reviewer should know." value={form.metadataSummary} onChange={(e) => setForm((current) => ({ ...current, metadataSummary: e.target.value }))} required />
            <input type="file" accept=".pdf,.txt,.epub" onChange={(e) => setFile(e.target.files?.[0] ?? null)} className="rounded-[1rem] border border-slate-200 bg-white px-4 py-3 text-sm" required />
            <button type="submit" disabled={loading} className="rounded-[1rem] bg-slate-950 px-4 py-3 text-sm font-semibold text-white">
              {loading ? 'Submitting...' : 'Submit book and start ingestion'}
            </button>
          </form>
          {error ? <div className="mt-4 rounded-[1.2rem] border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div> : null}
        </SurfaceCard>

        <SurfaceCard title="Submission Status" eyebrow="Step 3">
          {result ? (
            <div className="grid gap-3">
              <StatusBadge tone="success">Book created</StatusBadge>
              <p className="text-sm text-slate-700">Book ID: {result.bookPublicId}</p>
              <p className="text-sm text-slate-700">Ingestion job ID: {result.ingestionPublicId}</p>
              <div className="flex flex-wrap gap-2">
                <StatusBadge tone={result.ingestionStatus === 'review_pending' ? 'warning' : 'neutral'}>
                  {result.ingestionStatus}
                </StatusBadge>
              </div>
            </div>
          ) : (
            <p className="text-sm leading-7 text-slate-600">
              After submission, the pipeline will queue extraction, page mapping, chunking, topic draft generation, and skill draft creation. Scanned PDFs without extractable text will be marked for OCR review instead of returning fabricated content.
            </p>
          )}
        </SurfaceCard>
      </div>
    </RequireAuth>
  );
}
