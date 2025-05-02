"""
Evaluation module for RAG responses
This module provides metrics to evaluate the quality of RAG-generated responses.
"""

from sentence_transformers import SentenceTransformer, util
import numpy as np


class RAGEvaluator:
    """Evaluator for RAG-generated responses."""
    
    def __init__(self):
        """Initialize the RAG Evaluator."""
        # Load a pre-trained model for semantic similarity
        self.similarity_model = None
        try:
            self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"Warning: Could not load similarity model: {e}")
    
    def compute_similarity(self, text1, text2):
        """
        Compute semantic similarity between two texts.
        
        Args:
            text1 (str): First text
            text2 (str): Second text
            
        Returns:
            float: Similarity score between 0 and 1
        """
        if not self.similarity_model:
            raise ValueError("Similarity model not loaded")
            
        try:
            embeddings1 = self.similarity_model.encode(text1, convert_to_tensor=True)
            embeddings2 = self.similarity_model.encode(text2, convert_to_tensor=True)
            similarity = util.cos_sim(embeddings1, embeddings2).item()
            return similarity
        except Exception as e:
            raise ValueError(f"Error computing similarity: {str(e)}")
    
    def exact_match(self, generated, reference):
        """
        Check if the generated answer exactly matches the reference.
        
        Args:
            generated (str): Generated answer
            reference (str): Reference answer
            
        Returns:
            int: 1 if exact match, 0 otherwise
        """
        return 1 if generated.strip().lower() == reference.strip().lower() else 0
    
    def evaluate_single(self, generated, reference):
        """
        Evaluate a single generated answer against its reference.
        
        Args:
            generated (str): Generated answer
            reference (str): Reference answer
            
        Returns:
            dict: Evaluation metrics
        """
        metrics = {
            "exact_match": self.exact_match(generated, reference)
        }
        
        # Add semantic similarity if model is available
        if self.similarity_model:
            try:
                metrics["similarity_score"] = self.compute_similarity(generated, reference)
            except Exception:
                metrics["similarity_score"] = 0.0
                
        return metrics
    
    def evaluate_batch(self, generations, references):
        """
        Evaluate a batch of generated answers against their references.
        
        Args:
            generations (list): List of generated answers
            references (list): List of reference answers
            
        Returns:
            dict: Aggregated evaluation metrics
        """
        if len(generations) != len(references):
            raise ValueError("Number of generated answers must match number of references")
            
        results = []
        for gen, ref in zip(generations, references):
            results.append(self.evaluate_single(gen, ref))
            
        # Aggregate metrics
        avg_exact_match = np.mean([r["exact_match"] for r in results])
        metrics = {
            "exact_match": avg_exact_match,
            "individual_results": results
        }
        
        # Add semantic similarity if available
        if self.similarity_model and "similarity_score" in results[0]:
            avg_similarity = np.mean([r["similarity_score"] for r in results])
            metrics["similarity_score"] = avg_similarity
            
        return metrics


def evaluate_against_ground_truth(rag_pipeline, ground_truth):
    """
    Evaluate a RAG pipeline against ground truth question-answer pairs.
    
    Args:
        rag_pipeline: The RAG pipeline to evaluate
        ground_truth (list): List of dicts with 'question' and 'answer' keys
        
    Returns:
        dict: Evaluation results
    """
    evaluator = RAGEvaluator()
    generated_answers = []
    reference_answers = []
    
    # Generate answers for all questions
    for item in ground_truth:
        question = item["question"]
        reference = item["answer"]
        
        try:
            generated = rag_pipeline.answer_question(question)
            generated_answers.append(generated)
            reference_answers.append(reference)
        except Exception as e:
            print(f"Error generating answer for question '{question}': {e}")
    
    # Evaluate the answers
    metrics = evaluator.evaluate_batch(generated_answers, reference_answers)
    
    # Add detailed results with questions
    detailed_results = []
    for i, (gen, ref) in enumerate(zip(generated_answers, reference_answers)):
        detailed_results.append({
            "question": ground_truth[i]["question"],
            "ground_truth": ref,
            "generated": gen,
            "metrics": evaluator.evaluate_single(gen, ref)
        })
    
    metrics["detailed_results"] = detailed_results
    
    return metrics