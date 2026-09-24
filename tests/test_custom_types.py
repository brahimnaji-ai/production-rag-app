from custom_types import (
    RagChunkAndSrc,
    RagQueryResult,
    RagSearchResult,
    RagUpsertResult,
)


def test_rag_chunk_and_src():
    item = RagChunkAndSrc(chunks=["chunk 1", "chunk 2"], source_id="sample.pdf")
    assert item.chunks == ["chunk 1", "chunk 2"]
    assert item.source_id == "sample.pdf"


def test_rag_upsert_result():
    result = RagUpsertResult(ingested=5)
    assert result.ingested == 5


def test_rag_search_result():
    result = RagSearchResult(contexts=["ctx1", "ctx2"], sources=["source1.pdf"])
    assert result.contexts == ["ctx1", "ctx2"]
    assert result.sources == ["source1.pdf"]


def test_rag_query_result():
    result = RagQueryResult(
        answer="Paris is the capital.",
        sources=["geography.pdf"],
        num_contexts=2,
    )
    assert result.answer == "Paris is the capital."
    assert result.sources == ["geography.pdf"]
    assert result.num_contexts == 2
