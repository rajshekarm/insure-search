# InsureSearch

### Insurance Semantic Search Engine (ISSE)

*Beyond keywords. Search by meaning.*

## Overview

InsureSearch is an open-source, domain-aware semantic search engine designed to transform how insurance information is indexed, discovered, and retrieved.

The platform aims to combine vector embeddings, hybrid search, domain-specific document processing, and intelligent reranking to enable accurate and context-aware retrieval across the insurance ecosystem.

## Vision

Build a modular, scalable, secure, and model-agnostic search engine that serves as the foundational knowledge retrieval layer for insurance applications and AI systems.

## Core Objectives

- Insurance-specific semantic search
- Intelligent document ingestion and processing
- Dense and sparse vector indexing
- Hybrid search and retrieval
- Insurance-specific metadata filtering
- Context-aware document reranking
- Policy versioning and temporal retrieval
- Scalable and secure enterprise deployment
- Integration with RAG applications and AI agents

## Supported Domains

- Property and Casualty Insurance
- Health Insurance
- Life Insurance
- Auto Insurance
- Commercial Insurance
- Claims Management
- Underwriting
- Regulatory and Compliance

## Proposed Technology Stack

| Component            | Technology     |
| -------------------- | -------------- |
| Programming Language | Python         |
| Embedding Model      | BGE-M3         |
| Vector Database      | Qdrant         |
| Reranking            | BGE Reranker   |
| Document Processing  | Docling        |
| API Framework        | FastAPI        |
| Structured Storage   | PostgreSQL     |
| Containerization     | Docker         |
| Testing              | Pytest         |
| CI/CD                | GitHub Actions |

## Development Roadmap

### Phase 1 — Semantic Core

Branch: `feature/semantic-core`

- Document ingestion
- Text extraction and preprocessing
- Embedding generation
- Vector storage and indexing
- Semantic similarity search

### Phase 2 — Insurance Intelligence

Branch: `feature/insurance-intelligence`

- Insurance-aware document chunking
- Hybrid search
- Intelligent reranking
- Domain-specific metadata
- Retrieval evaluation and optimization

### Phase 3 — Enterprise Engine

Branch: `feature/enterprise-engine`

- Production REST APIs
- Authentication and authorization
- Distributed ingestion
- Security and data isolation
- Monitoring and observability
- Production deployment

## Design Principles

- Open-source first
- Model-agnostic architecture
- Modular and extensible components
- Insurance domain awareness
- Privacy and security by design
- Explainable and traceable retrieval
- Deployment flexibility
- Separation of retrieval and generation

## Project Status

Early development — Project initialization.

## License

Proposed: Apache License 2.0.
