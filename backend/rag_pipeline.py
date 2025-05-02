from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings  # Updated import
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

class RAGPipeline:
    def __init__(self, youtube_url):
        """Initialize the RAG pipeline with a YouTube URL."""
        self.video_id = self.extract_video_id(youtube_url)
        self.transcript = self.get_transcript()
        self.chunks = self.split_transcript()
        self.vector_store = self.create_vector_store()
        self.retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
        self.llm = self.initialize_llm()
        self.prompt = self.create_prompt()
        self.main_chain = self.build_chain()

    def extract_video_id(self, youtube_url):
        """Extract the video ID from a YouTube URL."""
        if "youtube.com/watch?v=" in youtube_url:
            return youtube_url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in youtube_url:
            return youtube_url.split("youtu.be/")[1].split("?")[0]
        else:
            raise ValueError("Invalid YouTube URL")

    def get_transcript(self):
        """Fetch the transcript for the YouTube video."""
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(self.video_id, languages=["en"])
            return " ".join(chunk["text"] for chunk in transcript_list)
        except TranscriptsDisabled:
            raise Exception("No captions available for this video.")

    def split_transcript(self):
        """Split the transcript into chunks."""
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        return splitter.create_documents([self.transcript])

    def create_vector_store(self):
        """Create a vector store from the transcript chunks."""
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        return FAISS.from_documents(self.chunks, embeddings)

    def initialize_llm(self):
        """Initialize the Groq LLM."""
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.2
        )

    def create_prompt(self):
        """Create the prompt template for the LLM."""
        return PromptTemplate(
            template="""
              You are a helpful assistant.
              Answer ONLY from the provided transcript context.
              If the context is insufficient, just say you don't know.

              {context}
              Question: {question}
            """,
            input_variables=['context', 'question']
        )

    def build_chain(self):
        """Build the RAG chain."""
        def format_docs(retrieved_docs):
            return "\n\n".join(doc.page_content for doc in retrieved_docs)

        parallel_chain = RunnableParallel({
            'context': self.retriever | RunnableLambda(format_docs),
            'question': RunnablePassthrough()
        })
        parser = StrOutputParser()
        return parallel_chain | self.prompt | self.llm | parser

    def process_query(self, question):
        """Process a user query and return the answer."""
        return self.main_chain.invoke(question)