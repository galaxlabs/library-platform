# Architecture & System Design

## System Overview

The Library Platform is a multi-tenant, source-grounded AI learning system with the following components:

### Core Components

1. **Django Backend (DRF)**
   - Modular app architecture
   - JWT authentication
   - Role-based permissions
   - RESTful API

2. **Next.js Frontend**
   - App Router (React 18+)
   - Mobile-first responsive design
   - RTL/LTR support
   - Arabic-first UX

3. **AI Adapter Layer**
   - Provider abstraction (Gemini, OpenRouter, Ollama)
   - Fallback mechanism
   - Key management (system/institute/user)

4. **Background Workers (Celery)**
   - OCR & PDF processing
   - Embedding generation
   - Task orchestration
   - Email notifications

5. **Data Storage**
   - PostgreSQL (primary data)
   - pgvector (semantic search)
   - Redis (caching, queues)

## Data Model

### User Management
- User (custom auth model with roles)
- Role (Admin, Scholar, Teacher, Student, etc.)
- Institute (multi-tenant grouping)
- ClassDarjah (student grouping by level)

### Library System
- Book (metadata, status)
- BookFile (PDF storage)
- BookChunk (text segmentation)
- BookMetadata (user/AI/reviewed states)

### Knowledge System
- KnowledgeObject (concepts, rules)
- Topic (extracted topics from books)
- Relation (knowledge graph edges)

### Answer System
- Query (user questions)
- Answer (grounded responses)
- Citation (source references)
- ScholarReview (expert verification)

### Learning System
- Exercise (practice items)
- Progress (user performance)
- WeakTopic (adaptive learning targets)

## API Architecture

### Authentication
```
POST   /api/v1/auth/register/
POST   /api/v1/auth/login/
POST   /api/v1/auth/token/refresh/
```

### User Management
```
GET    /api/v1/users/me/
PATCH  /api/v1/users/me/
POST   /api/v1/auth/password-change/
```

### Library
```
GET    /api/v1/library/books/
POST   /api/v1/library/upload/
GET    /api/v1/library/books/{id}/
```

### Q&A Engine
```
POST   /api/v1/qa/query/
GET    /api/v1/qa/results/{id}/
POST   /api/v1/qa/review/
```

## Deployment Architecture

```
Internet
   ↓
Nginx (Reverse Proxy)
   ├── library.digigalaxy.cloud → Next.js (3000)
   └── library.digigalaxy.cloud/api → Django (8001)
      ↓
   Django + DRF (8001)
      ├── PostgreSQL
      ├── Redis
      ├── Celery Workers
      └── AI Adapters
```

## Security Layers

1. **Authentication**: JWT with refresh rotation
2. **Authorization**: Role-based permissions
3. **Encryption**: Sensitive data at rest and in transit
4. **Audit**: All actions logged
5. **Rate Limiting**: API endpoints throttled
6. **Validation**: Input sanitization

## Scalability Considerations

- Horizontal scaling for Celery workers
- Database replication for read scaling
- Caching layer (Redis) for frequent queries
- CDN for static assets
- Load balancing for multiple app instances
