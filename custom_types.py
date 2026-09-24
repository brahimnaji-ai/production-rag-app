from pydantic import BaseModel


class RagChunkAndSrc(BaseModel):
    chunks: list[str]
    source_id: str = None

class RagUpsertResult(BaseModel):
    ingested: int

class RagSearchResult(BaseModel):
    contexts: list[str]
    sources: list[str]

class RagQueryResult(BaseModel):
    answer: str
    sources: list[str]
    num_contexts: int