from sentence_transformers import SentenceTransformer, util
import numpy as np

def evaluate_rag(rag_pipeline, ground_truth):
    """Evaluate the RAG pipeline using ground truth data."""
    # Load a model for semantic similarity
    similarity_model = SentenceTransformer('all-MiniLM-L6-v2')

    # Function to compute semantic similarity between two texts
    def compute_similarity(text1, text2):
        embeddings1 = similarity_model.encode(text1, convert_to_tensor=True)
        embeddings2 = similarity_model.encode(text2, convert_to_tensor=True)
        similarity = util.cos_sim(embeddings1, embeddings2).item()
        return similarity

    # Evaluate each question
    generation_results = []
    for item in ground_truth:
        question = item["question"]
        ground_truth_answer = item["answer"]

        # Generate an answer using the RAG pipeline
        generated_answer = rag_pipeline.process_query(question)

        # Exact match
        exact_match = 1 if generated_answer.strip().lower() == ground_truth_answer.strip().lower() else 0

        # Semantic similarity
        similarity_score = compute_similarity(generated_answer, ground_truth_answer)

        generation_results.append({
            "question": question,
            "ground_truth": ground_truth_answer,
            "generated": generated_answer,
            "exact_match": exact_match,
            "similarity_score": similarity_score
        })

    # Summarize results
    avg_exact_match = np.mean([result["exact_match"] for result in generation_results])
    avg_similarity_score = np.mean([result["similarity_score"] for result in generation_results])

    return {
        "average_exact_match": avg_exact_match,
        "average_similarity_score": avg_similarity_score,
        "detailed_results": generation_results
    }