# Architecture

Sentinel Delta is designed as a collection of loosely-coupled components:

- API layer (FastAPI): handles HTTP requests, delegates heavy work to background jobs, and exposes model endpoints.
- Ingestion: modules that fetch and normalize on-chain events. Production connectors could be: Alchemy/Infura RPC, archive nodes, The Graph, or webhook listeners.
- Processing: deterministic, testable transforms from raw events to numeric features (pandas/Numpy).
- Model layer (PyTorch): encapsulated models with wrappers for prediction and persistence.
- Storage: lightweight SQL storage is provided for metadata; production systems would use dedicated analytic stores.
- Background Jobs: training and heavy tasks are executed outside the request lifecycle (FastAPI BackgroundTasks or external workers).

Design goals: modularity, small surface for replacement, testability, and minimal dependencies.
