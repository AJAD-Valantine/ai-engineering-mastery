import sys
import types

dummy_module = types.ModuleType("langchain_community.chat_models.vertexai")
dummy_module.ChatVertexAI = type("ChatVertexAI", (object,), {})
sys.modules["langchain_community.chat_models.vertexai"] = dummy_module

from datasets import Dataset
from generator import generate_rag_response

# 2. Updated Langchain Imports (Uses the new dedicated Ollama package!)
from langchain_ollama import ChatOllama, OllamaEmbeddings
from ragas import evaluate
from ragas.metrics import (
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
    Faithfulness,
)
from ragas.run_config import RunConfig

# ==========================================
# 3. EVALUATION DATASET
# ==========================================
eval_questions = [
    "How often should infants be breastfed?",
    "What are symptoms of pellagra?",
    "How does saliva help with digestion?",
    "What is the recommended protein intake per day, based on your weight?",
    "What are micronutrients?",
]

ground_truth_answers = [
    "A newborn infant (birth to 28 days) requires feedings eight to twelve times a day or more.",
    "The common signs and symptoms of pellagra are known as the '4D's-diarrhea, dermatitis, dementia, and death.'",
    "Saliva provides lubrication and enables food movement downward. It also contains enzymes, such as salivary amylase that starts the breakdown of large starch molecules.",
    "The RDA for protein is 0.8 grams per kilogram of body weight per day.",
    "Micronutrients are nutrients required by the body in lesser amounts, but are still essential for carrying out bodily functions. They include minerals and vitamins.",
]

# ==========================================
# 4. RUN PIPELINE TO GATHER MODEL ANSWERS
# ==========================================
rag_answers = []
rag_contexts = []

print("Running pipeline across evaluation dataset...\n")

for i, q in enumerate(eval_questions):
    print(f"[{i+1}/{len(eval_questions)}] Processing: {q}")

    result = generate_rag_response(q, top_k=5)

    rag_answers.append(result["answer"])
    rag_contexts.append(result["contexts"])

# ==========================================
# 5. FORMAT FOR RAGAS (NEW V1.0 SCHEMA)
# ==========================================
evaluation_data = {
    "user_input": eval_questions,
    "response": rag_answers,
    "retrieved_contexts": rag_contexts,
    "reference": ground_truth_answers,
}

hf_dataset = Dataset.from_dict(evaluation_data)

# ==========================================
# 6. CONFIGURE LOCAL EVALUATOR (THE "JUDGE")
# ==========================================
print("\nInitializing local RAGAS evaluator models...")

# Clamp the temperature to 0 so Llama 3.2 doesn't hallucinate during JSON generation
evaluator_llm = ChatOllama(model="llama3.2", temperature=0)

# Point RAGAS to your local embeddings model
evaluator_embeddings = OllamaEmbeddings(model="nomic-embed-text")

# ==========================================
# 7. RUN RAGAS EVALUATION
# ==========================================
print("\nStarting RAGAS Evaluation... (This may take a few minutes locally)\n")

# Increase the timeout drastically just in case CPU generation is slow
custom_run_config = RunConfig(timeout=1000, max_workers=1)

results = evaluate(
    dataset=hf_dataset,
    metrics=[
        ContextPrecision(),
        ContextRecall(),
        Faithfulness(),
        AnswerRelevancy(),
    ],
    llm=evaluator_llm,
    embeddings=evaluator_embeddings,
    run_config=custom_run_config,
)

# ==========================================
# 8. EXPORT & VIEW RESULTS
# ==========================================
results_df = results.to_pandas()

print("\n--- RAGAS EVALUATION RESULTS ---")
# Print using the new 'user_input' column name
print(
    results_df[
        [
            "user_input",
            "context_precision",
            "context_recall",
            "faithfulness",
            "answer_relevancy",
        ]
    ]
)

results_df.to_csv("ragas_evaluation_results.csv", index=False)
print("\nDetailed results saved to 'ragas_evaluation_results.csv'")
