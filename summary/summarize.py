from summarizer import Summarizer
import warnings
import evaluate
from typing import TypedDict
from bert_score import BERTScorer

rouge = evaluate.load("rouge")
scorer = BERTScorer(model_type="bert-base-uncased")


def _setup_bert_summarizer():
    """
    Initializes and returns a BERT model Summarizer object.
    """
    warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn")
    return Summarizer()


def summarize_text(text):
    """
    Summarizes the provided text using a pre-initialized Summarizer model.

    Parameters:
        text (str): The text to summarize.
    Returns:
        str: The summarized text.
    """
    summarizer = _setup_bert_summarizer()
    summary = summarizer(text, min_length=60, max_length=500)
    return summary if summary else "No summary generated."


class RougeResult(TypedDict):
    rouge1: float
    rouge2: float
    rougeL: float
    rougeLsum: float


class BertScoreResult(TypedDict):
    precision: float
    recall: float
    f1_score: float


class Scores(RougeResult, BertScoreResult):
    pass


def rouge_score(doc: str, summarized_text: str) -> RougeResult:
    return rouge.compute(predictions=[summarized_text], references=[doc])


def bert_score(generated_answers, ground_truth) -> BertScoreResult:
    precision, recall, f1_score = scorer.score(generated_answers, ground_truth)

    return {
        "precision": precision.mean().item(),
        "recall": recall.mean().item(),
        "f1_score": f1_score.mean().item(),
    }


def calculate_scores(doc: str, summarized_text: str) -> Scores:
    """
    Calculate the ROUGE and BERT scores for the summarized text.

    Parameters:
        doc (str): The original document text.
        summarized_text (str): The summarized text.
    Returns:
        dict: A dictionary containing the ROUGE and BERT scores.
    """
    rouge_scores = rouge_score(doc, summarized_text)
    bert_scores = bert_score([summarized_text], [doc])

    return rouge_scores | bert_scores
