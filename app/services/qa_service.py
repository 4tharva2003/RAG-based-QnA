from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import Document, QAHistory
from app.services.embedding_service import embedding_service
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.core.config import settings

class QAService:
    def __init__(self, db: Session):
        self.db = db
        self.llm = Ollama(model="llama2")
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""
            Based on the following context, please answer the question. If the context doesn't contain enough information to answer the question, please say so.

            Context:
            {context}

            Question: {question}

            Answer:"""
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
    
    def get_relevant_context(self, question: str, documents: List[Document], top_k: int = 3) -> str:
        """Get relevant context from documents based on the question."""
        question_embedding = embedding_service.generate_embedding(question)
        document_embeddings = [doc.embedding for doc in documents]
        
        if not document_embeddings:
            return ""
        
        similar_indices = embedding_service.find_similar_documents(
            question_embedding,
            document_embeddings,
            top_k=top_k
        )
        
        context_parts = []
        for idx in similar_indices:
            context_parts.append(documents[idx].content)
        
        return "\n\n".join(context_parts)
    
    def generate_answer(self, question: str, context: str) -> str:
        """Generate an answer using the LLM chain."""
        if not context:
            return "I don't have enough context to answer this question."
        
        response = self.chain.run(context=context, question=question)
        return response.strip()
    
    def ask_question(self, question: str, user_id: int, document_id: Optional[int] = None) -> str:
        """Process a question and generate an answer."""
        # Get relevant documents
        if document_id:
            document = self.db.query(Document).filter(
                Document.id == document_id,
                Document.user_id == user_id
            ).first()
            if not document:
                return "Document not found."
            documents = [document]
        else:
            documents = self.db.query(Document).filter(
                Document.user_id == user_id,
                Document.is_selected == True
            ).all()
        
        # Get relevant context
        context = self.get_relevant_context(question, documents)
        
        # Generate answer
        answer = self.generate_answer(question, context)
        
        # Save to history
        if documents:
            history = QAHistory(
                question=question,
                answer=answer,
                user_id=user_id,
                document_id=documents[0].id if document_id else documents[0].id
            )
            self.db.add(history)
            self.db.commit()
        
        return answer
    
    def get_qa_history(self, user_id: int, limit: int = 10) -> List[QAHistory]:
        """Get Q&A history for a user."""
        return self.db.query(QAHistory).filter(
            QAHistory.user_id == user_id
        ).order_by(QAHistory.created_at.desc()).limit(limit).all() 