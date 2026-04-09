from __future__ import annotations

from dataclasses import dataclass

from django.db.models import Q

from apps.library.selectors import visible_chunks_queryset
from apps.skills.models import SkillPack


SENSITIVITY_TERMS = {
    'high': ['fatwa', 'haram', 'halal', 'takfir', 'kufr', 'طلاق', 'عقيدة'],
    'medium': ['ikhtilaf', 'khilaf', 'fiqh', 'hadith', 'aqidah'],
}


@dataclass
class QuestionClassification:
    subject: str
    intent: str
    sensitivity: str
    scope: str


def classify_question(question: str, scope: str, subject: str = '') -> QuestionClassification:
    lowered = question.lower()
    sensitivity = 'normal'
    for level, terms in SENSITIVITY_TERMS.items():
        if any(term in lowered or term in question for term in terms):
            sensitivity = level
            break

    intent = 'definition'
    if any(term in lowered for term in ['example', 'مثال']):
        intent = 'example_request'
    elif any(term in lowered for term in ['difference', 'compare', 'فرق']):
        intent = 'comparison'
    elif any(term in lowered for term in ['rule', 'حكم', 'قاعد']):
        intent = 'rule_lookup'

    if not subject:
        first_word = question.split()[0] if question.split() else 'General'
        subject = first_word[:80]

    return QuestionClassification(subject=subject, intent=intent, sensitivity=sensitivity, scope=scope)


def retrieve_chunks(*, user, question: str, scope: str, book_public_id=None, institute_public_id=None):
    queryset = visible_chunks_queryset(user)
    if book_public_id:
        queryset = queryset.filter(book__public_id=book_public_id)
    if institute_public_id:
        queryset = queryset.filter(book__institute__public_id=institute_public_id)

    terms = [term.strip() for term in question.split() if len(term.strip()) > 2][:10]
    score_map = {}
    for chunk in queryset[:500]:
        haystacks = ' '.join(
            filter(None, [chunk.content.lower(), chunk.normalized_content.lower(), chunk.section_title.lower()])
        )
        score = 0
        for term in terms:
            lowered = term.lower()
            score += haystacks.count(lowered)
        if score:
            score_map[chunk.pk] = score

    if not score_map:
        return []

    ordered_ids = [item[0] for item in sorted(score_map.items(), key=lambda item: item[1], reverse=True)]
    chunks = {chunk.pk: chunk for chunk in queryset.filter(pk__in=ordered_ids).select_related('book')}
    return [
        {'chunk': chunks[chunk_id], 'score': score_map[chunk_id]}
        for chunk_id in ordered_ids[:5]
        if chunk_id in chunks
    ]


def select_skill_pack(chunks, subject=''):
    if not chunks and not subject:
        return None
    book_ids = [item['chunk'].book_id for item in chunks]
    queryset = SkillPack.objects.filter(active=True).prefetch_related('source_books')
    if subject:
        queryset = queryset.filter(subject__icontains=subject)
    if book_ids:
        skill = queryset.filter(source_books__id__in=book_ids).distinct().first()
        if skill:
            return skill
    return queryset.first()
