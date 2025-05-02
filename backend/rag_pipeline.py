"""
RAG Pipeline for YouTube Chat Application
This module implements a Retrieval-Augmented Generation pipeline
for processing YouTube video transcripts and answering questions.
"""

import re
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser


class RAGPipeline:
    """RAG Pipeline for YouTube video transcripts."""
    
    def __init__(self, api_key=None):
        """
        Initialize the RAG Pipeline.
        
        Args:
            api_key (str): Groq API key
        """
        self.api_key = api_key
        self.vector_store = None
        self.llm = None
        self.chain = None
        self.video_id = None
        self.transcript = None
    
    def extract_video_id(self, youtube_url):
        """
        Extract the video ID from a YouTube URL.
        
        Args:
            youtube_url (str): YouTube URL
            
        Returns:
            str: YouTube video ID
        """
        # Common YouTube URL patterns
        patterns = [
            r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, youtube_url)
            if match:
                return match.group(1)
        
        # If the input is already just an ID (11 characters)
        if re.match(r'^[a-zA-Z0-9_-]{11}$', youtube_url):
            return youtube_url
            
        raise ValueError("Could not extract YouTube video ID from URL")
    
    def get_transcript(self, video_id):
        """
        Get the transcript for a YouTube video.
        
        Args:
            video_id (str): YouTube video ID
            
        Returns:
            str: Transcript text
        """
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
            transcript = " ".join(chunk["text"] for chunk in transcript_list)
            return transcript
        except TranscriptsDisabled:
            raise ValueError("No captions available for this video.")
        except Exception as e:
            raise ValueError(f"Failed to fetch transcript: {str(e)}")
    
    def build_pipeline(self, transcript, api_key=None):
        """
        Build the RAG pipeline with the given transcript.
        
        Args:
            transcript (str): Video transcript
            api_key (str, optional): Groq API key
            
        Returns:
            RunnableParallel: The assembled RAG pipeline
        """
        if api_key:
            self.api_key = api_key
            
        if not self.api_key:
            raise ValueError("Groq API key is required")
        
        # Split the transcript into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.create_documents([transcript])
        
        # Create embeddings and vector store
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_store = FAISS.from_documents(chunks, embeddings)
        retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
        
        # Initialize LLM
        self.llm = ChatGroq(
            api_key=self.api_key,
            model="llama-3.1-70b-versatile",  # Using an available model
            temperature=0.2
        )
        
        # Create prompt template
        prompt = PromptTemplate(
            template="""
              You are a helpful assistant answering questions about a YouTube video based on its transcript.
              Answer ONLY from the provided transcript context.
              If the context is insufficient, just say you don't know.
              Keep your answers concise but informative.

              {context}
              Question: {question}
            """,
            input_variables=['context', 'question']
        )
        
        # Format documents function
        def format_docs(retrieved_docs):
            context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
            return context_text
        
        # Build the chain
        parallel_chain = RunnableParallel({
            'context': retriever | RunnableLambda(format_docs),
            'question': RunnablePassthrough()
        })
        
        parser = StrOutputParser()
        self.chain = parallel_chain | prompt | self.llm | parser
        
        return self.chain
    
    def initialize(self, youtube_url, api_key=None):
        """
        Initialize the RAG pipeline with a YouTube video.
        
        Args:
            youtube_url (str): YouTube video URL
            api_key (str, optional): Groq API key
            
        Returns:
            dict: Status information
        """
        if api_key:
            self.api_key = api_key
            
        try:
            # Extract video ID
            self.video_id = self.extract_video_id(youtube_url)
            
            # Get transcript
            self.transcript = self.get_transcript(self.video_id)
            
            # Build pipeline
            self.build_pipeline(self.transcript, self.api_key)
            
            return {
                "status": "success",
                "message": "RAG pipeline initialized successfully",
                "video_id": self.video_id,
                "transcript_length": len(self.transcript)
            }
        except Exception as e:
            raise Exception(f"Failed to initialize RAG pipeline: {str(e)}")
    
    def answer_question(self, question):
        """
        Answer a question using the RAG pipeline.
        
        Args:
            question (str): The question to answer
            
        Returns:
            str: The answer
        """
        if not self.chain:
            raise ValueError("RAG pipeline not initialized. Call initialize() first.")
        
        try:
            answer = self.chain.invoke(question)
            return answer
        except Exception as e:
            raise Exception(f"Failed to answer question: {str(e)}")