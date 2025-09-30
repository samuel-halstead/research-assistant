from app.schemas.doc_list import DocListResponse


class DocListManager:
    def __init__(self):
        pass

    def build_doc_list_response(self, nodes_with_scores) -> list[DocListResponse]:
        doc_list = []
        for i, nws in enumerate(nodes_with_scores):
            # Handle both LangChain documents and LlamaIndex nodes
            if hasattr(nws.node, "metadata"):
                metadata = nws.node.metadata or {}
            else:
                metadata = getattr(nws.node, "metadata", {}) or {}

            doc_score = nws.score if nws.score else 0
            doc_list.append(
                DocListResponse(
                    index=i + 1,
                    title=metadata.get("title", "No Title"),
                    abstract=metadata.get("abstract", "No Abstract"),
                    source_id=metadata.get("source", f"doc_{i}"),
                    similarity=round(doc_score, 4),
                )
            )

        return doc_list


doc_list_manager = DocListManager()
