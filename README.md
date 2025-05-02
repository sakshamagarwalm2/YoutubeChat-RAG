# YouTubeChat RAG

A Retrieval-Augmented Generation (RAG) system that allows you to chat with YouTube videos by analyzing their transcripts. Ask questions about video content and get accurate, contextual answers powered by LLM and vector search technology.

## 📝 Table of Contents
- [About](#about)
- [Features](#features)
- [Architecture](#architecture)
- [Performance Evaluation](#performance-evaluation)
- [Installation](#installation)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Usage](#usage)
- [Technology Stack](#technology-stack)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## 🔍 About

YouTubeChat RAG is an interactive application that enhances the way users engage with YouTube content. By leveraging the power of Retrieval-Augmented Generation (RAG), this system enables users to ask natural language questions about YouTube videos and receive accurate answers derived directly from the video's transcript.

Instead of watching an entire video to find specific information, users can simply query the system to get precisely what they're looking for.

## ✨ Features

- **YouTube Transcript Extraction**: Automatically pulls and processes transcripts from any YouTube video
- **Intelligent Chunking**: Splits transcripts into semantically meaningful segments for accurate retrieval
- **Vector Search**: Uses FAISS and embedding models to find the most relevant content
- **LLM Integration**: Leverages Groq's LLaMA 3.3 70B model for natural language understanding and generation
- **Modern UI**: Clean, responsive interface built with Next.js and Tailwind CSS
- **Evaluation Metrics**: Built-in system to measure answer accuracy and relevance

## 🏗️ Architecture

The system follows a standard RAG (Retrieval-Augmented Generation) pipeline:

1. **Indexing**:
   - Document Ingestion: Extract YouTube video transcripts
   - Text Splitting: Chunk transcripts into manageable segments
   - Embedding Generation: Convert chunks to vector embeddings
   - Vector Storage: Store embeddings in FAISS vector database

2. **Retrieval**:
   - Query Processing: Convert user questions to vector embeddings
   - Similarity Search: Find the most relevant transcript chunks

3. **Augmentation**:
   - Context Formation: Combine retrieved chunks into context
   - Prompt Engineering: Construct effective prompts for the LLM

4. **Generation**:
   - Answer Generation: Pass the augmented prompt to the LLM
   - Response Formatting: Present the answer to the user

## 📊 Performance Evaluation

The system includes a built-in evaluation framework to measure performance:

```
Average Semantic Similarity Score: 0.9728
```

![YouTube ChatBot](https://github.com/sakshamagarwalm2/YoutubeChat-RAG/blob/main/Public/evaluation.png)

The evaluation system tests the RAG pipeline against a set of ground truth question-answer pairs, measuring both exact matches and semantic similarity. Current benchmarks show strong performance on semantic similarity metrics.

Example evaluation:
```
Evaluating question: Why was the password on the zip file a red flag?
Ground truth answer: The password on the zip file was a red flag because it prevents Google or Microsoft from scanning the file for viruses, which is a common tactic to hide malicious content like viruses.
Generated answer: The password on the zip file was a red flag because it prevented Google or Microsoft from scanning the file for viruses. This suggested that the file might contain malware, and the password was added to avoid detection.
Exact match: 0
Semantic similarity score: 0.9728
```

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn
- API key from Groq or another LLM provider

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sakshamagarwalm2/youtubechat-rag.git
   cd youtubechat-rag/backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the backend directory with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key
   ```

4. Start the Flask server:
   ```bash
   python app.py
   ```
   The backend server will run on http://localhost:5000

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```
   The frontend will be available at http://localhost:3000

## 💻 Usage

1. Open the application in your browser at http://localhost:3000
2. Enter a YouTube video URL in the input field
3. Wait for the transcript to be processed
4. Ask questions about the video content in the chat interface
5. Receive accurate answers based on the video's transcript

## 🔧 Technology Stack

### Backend
- **Flask**: Web framework for the API
- **LangChain**: Framework for building LLM applications
- **YouTube Transcript API**: For extracting video transcripts
- **FAISS**: Vector database for similarity search
- **HuggingFace Embeddings**: For generating vector representations
- **Groq API**: LLM provider for text generation

### Frontend
- **Next.js**: React framework for the web interface
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: Component library
- **TypeScript**: For type-safe code

## 🔮 Future Improvements

- Multi-language support for non-English YouTube videos
- Support for additional video platforms (Vimeo, Twitch, etc.)
- User authentication and saved conversation history
- Audio-based question input for accessibility
- Fine-tuning the LLM for better domain-specific responses
- PDF summary generation of video content

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Created by [Saksham Agarwal](https://github.com/sakshamagarwalm2)
