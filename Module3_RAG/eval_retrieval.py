# eval_retrieval.py
import warnings
warnings.filterwarnings("ignore")  # ignore all Python warnings

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from sentence_transformers import CrossEncoder

from config import EMBEDDING_MODEL  # same model as in ingest


def load_eval_queries(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)



def evaluate_metrics(
    db_dir: str,
    eval_file: str,
    k: int = 5,
    rerank: bool = False,
    pre_k: int = 20,
):
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = FAISS.load_local(
        db_dir,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    if rerank:
        if pre_k < k:
            pre_k = k
        reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        retriever = None
    else:
        reranker = None
        retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    queries = load_eval_queries(eval_file)

    total = len(queries)
    doc_type_hits = 0
    rank_scores = []

    details = []

    for q in queries:
        question = q["question"]
        expected_doc_type = q.get("expected_doc_type")

        # --- list of expected basenames (multi-doc friendly) ---
        expected_basenames = q.get("expected_source_basenames") or []

        # backward compat: if old single key exists, merge it into the list
        single_basename = q.get("expected_source_basename")
        if single_basename and single_basename not in expected_basenames:
            expected_basenames.append(single_basename)

        # -------- retrieve documents --------
        if rerank:
            docs = vectorstore.similarity_search(question, k=pre_k)
            if not docs:
                rank_scores.append(0.0)
                details.append(
                    {
                        "id": q["id"],
                        "question": question,
                        "expected_doc_type": expected_doc_type,
                        "expected_source_basenames": expected_basenames,
                        "retrieved_doc_types": [],
                        "retrieved_sources": [],
                        "doc_type_hit": False,
                        "file_hit": False,
                        "file_rank": None,
                        "rank_score": 0.0,
                    }
                )
                continue

            pairs = [(question, d.page_content) for d in docs]
            scores = reranker.predict(pairs)
            scored_docs = list(zip(docs, scores))
            scored_docs.sort(key=lambda x: x[1], reverse=True)
            top_docs = [d for d, _ in scored_docs[:k]]
        else:
            top_docs = retriever.get_relevant_documents(question)

        retrieved_types = [d.metadata.get("doc_type", "unknown") for d in top_docs]
        retrieved_sources = [d.metadata.get("source", "") for d in top_docs]

        # ---------- Hit@k on doc_type ----------
        type_hit = False
        if expected_doc_type and expected_doc_type in retrieved_types:
            type_hit = True
            doc_type_hits += 1

        # ---------- RankScore@k on file (using list) ----------
        rank_score = 0.0
        file_hit = False
        file_rank = None

        if expected_basenames:
            match_positions = []
            for idx, src in enumerate(retrieved_sources):
                if not src:
                    continue
                base = os.path.basename(src)
                if base in expected_basenames:
                    match_positions.append(idx)

            if match_positions:
                file_hit = True
                file_rank = min(match_positions)  # best rank among matches
                rank_score = (k - file_rank) / float(k)  # 1st→1.0, kth→1/k

        rank_scores.append(rank_score)

        details.append(
            {
                "id": q["id"],
                "question": question,
                "expected_doc_type": expected_doc_type,
                "expected_source_basenames": expected_basenames,
                "retrieved_doc_types": retrieved_types,
                "retrieved_sources": retrieved_sources,
                "doc_type_hit": type_hit,
                "file_hit": file_hit,
                "file_rank": file_rank,
                "rank_score": rank_score,
            }
        )

    hit_at_k = doc_type_hits / total if total else 0.0
    avg_rank_score = sum(rank_scores) / total if total else 0.0

    metrics = {
        "num_queries": total,
        "hit_at_k_doc_type": hit_at_k,
        "avg_rank_score": avg_rank_score,
    }

    return metrics, details


def append_to_report(
    report_path: str,
    label: str,
    db_dir: str,
    eval_file: str,
    k: int,
    metrics: dict,
    rerank: bool,
    pre_k: int | None,
):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    header = f"\n\n---\n\n### Evaluation Run – {now} ({label})\n\n"
    body = (
        f"**Vector DB directory:** `{db_dir}`  \n"
        f"**Eval file:** `{eval_file}`  \n"
        f"**Top-K (k):** `{k}`  \n"
        f"**Rerank:** `{rerank}`  \n"
    )
    if rerank and pre_k is not None:
        body += f"**Top-pre-K (before rerank):** `{pre_k}`  \n"

    body += (
        f"\n**Hit@{k} (doc_type):** `{metrics['hit_at_k_doc_type']:.3f}`  \n"
        f"**Avg RankScore@{k} (file-level):** `{metrics['avg_rank_score']:.3f}`  \n"
    )

    path = Path(report_path)
    if not path.exists():
        path.write_text(
            f"# Improvement of RAG-based AI system – {label}\n\n",
            encoding="utf-8",
        )

    with path.open("a", encoding="utf-8") as f:
        f.write(header)
        f.write(body)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--db-dir",
        type=str,
        default="vector_db",
        help="Directory with FAISS index.",
    )
    parser.add_argument(
        "--eval-file",
        type=str,
        default="eval_queries.jsonl",
        help="JSONL with eval questions.",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=5,
        help="Top-K for retrieval (and after rerank).",
    )
    parser.add_argument(
        "--rerank",
        action="store_true",
        help="Use cross-encoder reranker on top of FAISS.",
    )
    parser.add_argument(
        "--pre-k",
        type=int,
        default=25,
        help="Top-pre-K from FAISS before rerank (only used if --rerank).",
    )
    parser.add_argument(
        "--label",
        type=str,
        default="baseline_k5",
        help="Config label (baseline / overlap / rerank / ...).",
    )
    parser.add_argument(
        "--report",
        type=str,
        default="Improvement_of_RAG-based_AI_system_Assylnur_Lesken.md",
        help="Markdown report file.",
    )

    args = parser.parse_args()

    metrics, details = evaluate_metrics(
        db_dir=args.db_dir,
        eval_file=args.eval_file,
        k=args.k,
        rerank=args.rerank,
        pre_k=args.pre_k,
    )

    with open(f"details{args.label}.json", "w", encoding="utf-8") as f:
        json.dump(details, f, indent=4, ensure_ascii=False)

    print(json.dumps(metrics, indent=2))
    append_to_report(
        report_path=args.report,
        label=args.label,
        db_dir=args.db_dir,
        eval_file=args.eval_file,
        k=args.k,
        metrics=metrics,
        rerank=args.rerank,
        pre_k=args.pre_k if args.rerank else None,
    )


if __name__ == "__main__":
    main()
