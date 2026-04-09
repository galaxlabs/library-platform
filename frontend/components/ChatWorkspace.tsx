'use client';

import Link from 'next/link';
import { FormEvent, useEffect, useState } from 'react';

import api from '../lib/api';

type Source = {
  id: string | number;
  book_title: string;
  page_number: number | null;
  score: string;
  excerpt: string;
};

type Answer = {
  id: string | number;
  direct_answer: string;
  detailed_explanation: string;
  simplified_explanation: string;
  verification_status: string;
  confidence: string;
  sources: Source[];
  created_at: string;
};

type QueryItem = {
  id: string | number;
  question: string;
  created_at: string;
  latest_answer: Answer | null;
};

export default function ChatWorkspace() {
  const [question, setQuestion] = useState('');
  const [items, setItems] = useState<QueryItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [error, setError] = useState('');
  const [needsLogin, setNeedsLogin] = useState(false);

  useEffect(() => {
    const loadHistory = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setNeedsLogin(true);
        setInitialLoading(false);
        return;
      }

      try {
        const response = await api.get('/qa/chat/');
        setItems(response.data);
      } catch (err: any) {
        if (err?.response?.status === 401) {
          setNeedsLogin(true);
          setError('Please sign in first to use chat.');
        } else {
          setError(err?.response?.data?.detail || 'Could not load chat history.');
        }
      } finally {
        setInitialLoading(false);
      }
    };

    loadHistory();
  }, []);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    if (!question.trim()) return;

    if (needsLogin) {
      setError('Please sign in first to ask a question.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await api.post('/qa/chat/', {
        question: question.trim(),
        language_pair: 'ar-en',
      });

      setItems((current) => [response.data, ...current]);
      setQuestion('');
    } catch (err: any) {
      if (err?.response?.status === 401) {
        setNeedsLogin(true);
        setError('Please sign in first to use chat.');
      } else {
        setError(err?.response?.data?.detail || 'Could not send your question.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid gap-6 xl:grid-cols-[360px_minmax(0,1fr)]">
      <aside className="glass-panel rounded-[2rem] p-6">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">
          Ask AI
        </p>
        <h2 className="mt-3 text-3xl font-bold tracking-[-0.05em] text-slate-950">
          Study chat
        </h2>
        <p className="mt-3 text-sm leading-7 text-slate-600">
          Ask a clear question about a lesson, a rule, or a book. The system will try to return a simple answer with matching source passages.
        </p>

        {needsLogin ? (
          <div className="mt-6 rounded-[1.4rem] border border-amber-200 bg-amber-50 p-5">
            <p className="text-sm font-semibold text-amber-900">Sign in required</p>
            <p className="mt-2 text-sm leading-6 text-amber-800">
              Chat history and AI answers are saved per user account. Please sign in first.
            </p>
            <div className="mt-4 flex flex-wrap gap-3">
              <Link
                href="/login"
                className="rounded-[1rem] bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white"
              >
                Go to login
              </Link>
              <Link
                href="/register"
                className="rounded-[1rem] bg-white px-4 py-2.5 text-sm font-semibold text-slate-900 ring-1 ring-slate-200"
              >
                Create account
              </Link>
            </div>
          </div>
        ) : (
        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            rows={6}
            placeholder="Ask a question about nahw, sarf, a passage, or a book..."
            className="w-full rounded-[1.4rem] border border-slate-200 bg-white px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-transparent focus:ring-2 focus:ring-emerald-700"
          />
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-[1.2rem] bg-slate-950 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? 'Sending question...' : 'Ask question'}
          </button>
        </form>
        )}

        {error ? (
          <div className="mt-4 rounded-[1.2rem] border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        ) : null}
      </aside>

      <section className="grid gap-4">
        <div className="glass-panel rounded-[2rem] p-6">
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">
                Recent chat
              </p>
              <h3 className="mt-2 text-2xl font-bold tracking-[-0.04em] text-slate-950">
                Your questions and answers
              </h3>
            </div>
            <span className="rounded-full bg-slate-950 px-3 py-1 text-xs font-semibold text-white">
              {items.length} items
            </span>
          </div>
        </div>

        {initialLoading ? (
          <div className="rounded-[1.6rem] border border-slate-200 bg-white/85 p-6 text-sm text-slate-600">
            Loading chat history...
          </div>
        ) : null}

        {!initialLoading && items.length === 0 ? (
          <div className="rounded-[1.6rem] border border-slate-200 bg-white/85 p-6 text-sm text-slate-600">
            No questions yet. Ask your first question to start the chat.
          </div>
        ) : null}

        {items.map((item) => (
          <article
            key={item.id}
            className="rounded-[1.8rem] border border-slate-200 bg-white/90 p-6 shadow-[0_18px_40px_rgba(40,39,33,0.08)]"
          >
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">
              Question
            </p>
            <h4 className="mt-3 text-xl font-semibold tracking-[-0.03em] text-slate-950">
              {item.question}
            </h4>

            {item.latest_answer ? (
              <>
                <div className="mt-6 rounded-[1.4rem] bg-slate-950 px-5 py-5 text-white">
                  <p className="text-xs uppercase tracking-[0.24em] text-emerald-300">
                    Answer
                  </p>
                  <p className="mt-3 whitespace-pre-line text-sm leading-7 text-slate-100">
                    {item.latest_answer.direct_answer}
                  </p>
                </div>

                <div className="mt-5 flex flex-wrap gap-2">
                  <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-800">
                    {item.latest_answer.verification_status}
                  </span>
                  <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">
                    Confidence: {item.latest_answer.confidence}
                  </span>
                </div>

                {item.latest_answer.sources.length > 0 ? (
                  <div className="mt-5 grid gap-3">
                    {item.latest_answer.sources.map((source) => (
                      <div
                        key={source.id}
                        className="rounded-[1.3rem] border border-slate-200 bg-[rgba(247,244,238,0.9)] p-4"
                      >
                        <p className="text-sm font-semibold text-slate-900">
                          {source.book_title || 'Source'}
                          {source.page_number ? ` - page ${source.page_number}` : ''}
                        </p>
                        <p className="mt-2 text-sm leading-6 text-slate-600">
                          {source.excerpt}
                        </p>
                      </div>
                    ))}
                  </div>
                ) : null}
              </>
            ) : null}
          </article>
        ))}
      </section>
    </div>
  );
}
