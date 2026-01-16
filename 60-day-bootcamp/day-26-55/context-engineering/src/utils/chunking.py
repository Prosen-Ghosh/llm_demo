# src/utils/chunking.py
import uuid
import tiktoken
from typing import List, Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.models.schema import Document, Chunk

class ChunkingService:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.tokenizer = tiktoken.get_encoding("cl100k_base")

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=self._token_len,
            separators=["\n\n", "\n", " ", ""]
        )

    def _token_len(self, text: str) -> int:
        return len(self.tokenizer.encode(text))
    
    def chunk_document(self, doc: Document) -> List[Chunk]:
        text_chunks = self.splitter.split_text(doc.content)

        chunk_objects = []
        for i, text in enumerate(text_chunks):
            chunk_objects.append(
                Chunk(
                    id=uuid.uuid4(),
                    document_id=doc.id,
                    content=text,
                    chunk_index=i,
                    metadata={
                        **doc.metadata,
                        "chunk_size": self._token_len(text),
                        "strategy": "recursive"
                    }
                )
            )
        return chunk_objects
    
    def chunk_document_hierarchical(self, doc: Document, parent_size: int = 1000, child_size: int = 200) -> List[Chunk]:
        parent_splitter = RecursiveCharacterTextSplitter(
            chunk_size=parent_size,
            chunk_overlap=0,
            length_function=self._token_len
        )

        child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=child_size,
            chunk_overlap=20,
            length_function=self._token_len
        )

        chunks = []
        parent_texts = parent_splitter.split_text(doc.content)

        global_index = 0
        for p_idx, p_text in enumerate(parent_texts):
            parent_id = uuid.uuid4()

            chunks.append(Chunk(
                id=parent_id,
                document_id=doc.id,
                content=p_text,
                chunk_index=global_index,
                metadata={**doc.metadata, "type": "parent", "level": 0}
            ))
            global_index += 1

            child_texts = child_splitter.split_text(p_text)
            for c_text in child_texts:
                chunks.append(Chunk(
                    id=uuid.uuid4(),
                    document_id=doc.id,
                    content=c_text,
                    chunk_index=global_index,
                    metadata={
                        **doc.metadata, 
                        "type": "child", 
                        "parent_id": str(parent_id),
                        "level": 1
                    }
                ))
                global_index += 1
        
        return chunks