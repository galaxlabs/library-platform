from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable

from django.db import transaction

from apps.library.models import Book, BookChunk, BookFile, BookStructureMap, BookTopicMap
from apps.skills.models import SkillPack

from .models import IngestionStageRun, UploadSession, UploadTask

logger = logging.getLogger(__name__)

try:
    from pypdf import PdfReader
except Exception:  # pragma: no cover - optional dependency during development
    PdfReader = None


@dataclass
class ExtractionResult:
    text: str
    page_map: list[dict]
    ocr_pending: bool = False
    notes: str = ''


def create_ingestion_job(*, book: Book, initiated_by) -> UploadSession:
    with transaction.atomic():
        session = UploadSession.objects.create(
            book=book,
            initiated_by=initiated_by,
            status='queued',
            current_stage='queued',
            confirmation_snapshot={
                'book_public_id': str(book.public_id),
                'title': book.title,
            },
        )
        for stage in [
            'file_saved',
            'page_extraction',
            'page_mapping',
            'chunking',
            'concept_extraction',
            'skill_pack_draft_generation',
            'review',
        ]:
            IngestionStageRun.objects.get_or_create(
                upload_session=session,
                stage=stage,
                defaults={'status': 'pending'},
            )
    return session


def _mark_stage(session: UploadSession, stage: str, status: str, diagnostics=None):
    IngestionStageRun.objects.update_or_create(
        upload_session=session,
        stage=stage,
        defaults={'status': status, 'diagnostics': diagnostics or {}},
    )
    session.current_stage = stage
    if status == 'running':
        session.status = 'processing'
    session.save(update_fields=['current_stage', 'status', 'updated_at'])


def _task_record(session: UploadSession, task_name: str, stage: str, status: str, payload=None, result=None):
    UploadTask.objects.create(
        upload_session=session,
        status=status,
        task_name=task_name,
        stage=stage,
        payload=payload or {},
        result=result or {},
    )


def extract_book_text(book_file: BookFile) -> ExtractionResult:
    if book_file.file_kind == 'text':
        raw = book_file.file.read().decode('utf-8', errors='ignore')
        return ExtractionResult(text=raw, page_map=[{'page_number': 1, 'chars': len(raw)}])

    if book_file.file_kind != 'pdf':
        return ExtractionResult(text='', page_map=[], notes='Unsupported file type for extraction')

    if PdfReader is None:
        return ExtractionResult(
            text='',
            page_map=[],
            ocr_pending=True,
            notes='pypdf not installed; PDF extraction unavailable',
        )

    try:
        reader = PdfReader(book_file.file)
        page_map = []
        page_text = []
        for index, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or '').strip()
            page_map.append({'page_number': index, 'chars': len(text)})
            if text:
                page_text.append(f'[Page {index}]\n{text}')
        full_text = '\n\n'.join(page_text).strip()
        if not full_text:
            return ExtractionResult(
                text='',
                page_map=page_map,
                ocr_pending=True,
                notes='No extractable PDF text found; OCR pending',
            )
        return ExtractionResult(text=full_text, page_map=page_map, ocr_pending=False)
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception('PDF extraction failed for book_file=%s', book_file.pk)
        return ExtractionResult(
            text='',
            page_map=[],
            ocr_pending=True,
            notes=f'Extraction failed: {exc.__class__.__name__}',
        )


def build_chunks(text: str) -> list[dict]:
    if not text:
        return []
    paragraphs = [segment.strip() for segment in text.split('\n\n') if segment.strip()]
    chunks = []
    for index, paragraph in enumerate(paragraphs, start=1):
        chunks.append(
            {
                'chunk_type': 'paragraph',
                'page_number': None,
                'section_title': f'Section {index}',
                'content': paragraph[:4000],
                'normalized_content': paragraph[:4000],
                'metadata': {'chunk_index': index},
            }
        )
    return chunks[:200]


def create_topic_map(book: Book, chunks: Iterable[BookChunk]) -> BookTopicMap:
    words = []
    for chunk in chunks:
        words.extend([word for word in chunk.content.split() if len(word) > 4][:10])
    topics = sorted({word.strip('.,:;()[]') for word in words if word})[:20]
    return BookTopicMap.objects.create(
        book=book,
        topics=topics,
        concept_links=[],
        graph_snapshot={'generated_by': 'placeholder_v1', 'topic_count': len(topics)},
    )


def create_skill_pack_draft(book: Book) -> SkillPack:
    skill_pack, _ = SkillPack.objects.get_or_create(
        name=f'{book.title} Draft Pack',
        defaults={
            'subject': getattr(book.primary_subject, 'name', '') or 'General Studies',
            'level': book.level,
            'review_status': 'draft',
            'active': False,
        },
    )
    skill_pack.source_books.add(book)
    return skill_pack


def run_ingestion_pipeline(session: UploadSession) -> UploadSession:
    book = session.book
    book_file = book.files.filter(is_primary=True).first()
    if not book or not book_file:
        session.status = 'failed'
        session.error_message = 'Book or primary file missing.'
        session.save(update_fields=['status', 'error_message', 'updated_at'])
        return session

    _mark_stage(session, 'file_saved', 'completed', {'file_kind': book_file.file_kind})

    _mark_stage(session, 'page_extraction', 'running')
    extraction = extract_book_text(book_file)
    _task_record(
        session,
        task_name='extract_text',
        stage='page_extraction',
        status='completed' if extraction.text or extraction.ocr_pending else 'failed',
        result={'ocr_pending': extraction.ocr_pending, 'notes': extraction.notes},
    )
    _mark_stage(
        session,
        'page_extraction',
        'completed' if extraction.text or extraction.ocr_pending else 'failed',
        {'ocr_pending': extraction.ocr_pending, 'notes': extraction.notes},
    )

    BookStructureMap.objects.create(
        book=book,
        version_label='v1-placeholder',
        structure_data={'extraction_notes': extraction.notes},
        page_map=extraction.page_map,
        heading_index=[],
    )

    if extraction.ocr_pending and not extraction.text:
        book.metadata_flags = {**book.metadata_flags, 'ocr_status': 'OCR_PENDING'}
        book.save(update_fields=['metadata_flags', 'updated_at'])
        session.status = 'review_pending'
        session.current_stage = 'review'
        session.save(update_fields=['status', 'current_stage', 'updated_at'])
        _mark_stage(session, 'review', 'completed', {'ocr_status': 'OCR_PENDING'})
        return session

    _mark_stage(session, 'page_mapping', 'completed', {'pages': len(extraction.page_map)})

    _mark_stage(session, 'chunking', 'running')
    book.chunks.all().delete()
    chunk_payloads = build_chunks(extraction.text)
    chunks = [
        BookChunk(book=book, book_file=book_file, **payload)
        for payload in chunk_payloads
    ]
    created_chunks = BookChunk.objects.bulk_create(chunks)
    _task_record(
        session,
        task_name='create_chunks',
        stage='chunking',
        status='completed',
        result={'chunk_count': len(created_chunks)},
    )
    _mark_stage(session, 'chunking', 'completed', {'chunk_count': len(created_chunks)})

    _mark_stage(session, 'concept_extraction', 'running')
    topic_map = create_topic_map(book, created_chunks)
    _task_record(
        session,
        task_name='topic_extraction',
        stage='concept_extraction',
        status='completed',
        result={'topic_count': len(topic_map.topics)},
    )
    _mark_stage(session, 'concept_extraction', 'completed', {'topic_count': len(topic_map.topics)})

    _mark_stage(session, 'skill_pack_draft_generation', 'running')
    skill_pack = create_skill_pack_draft(book)
    _task_record(
        session,
        task_name='skill_draft_creation',
        stage='skill_pack_draft_generation',
        status='completed',
        result={'skill_pack_id': skill_pack.id},
    )
    _mark_stage(session, 'skill_pack_draft_generation', 'completed', {'skill_pack_id': skill_pack.id})

    book.review_status = 'under_review'
    book.save(update_fields=['review_status', 'updated_at'])
    session.status = 'review_pending'
    session.current_stage = 'review'
    session.save(update_fields=['status', 'current_stage', 'updated_at'])
    _mark_stage(session, 'review', 'completed', {'status': 'awaiting_human_review'})
    return session
