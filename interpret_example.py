"""
Minimal interpreter for linear and GLM model outputs.
This script demonstrates the core idea of the project:
Take a model summary, detect key statistical elements,
and retrieve the relevant explanations from the knowledge base.
This version does not use LLMs.
Everything is grounded in explicit statistical knowledge.
"""


from pathlib import Path
import re
from typing import List, Dict
from retrieval.logging_config import setup_logging
logger = setup_logging("interpret.linear")


from retrieval.search import semantic_search


# =========================
# Paths
# =========================

PROJECT_ROOT = Path(__file__).resolve().parent
EXAMPLES_PATH = PROJECT_ROOT / "examples"



"""
Remove markdown formatting so explanations can be printed cleanly.
This keeps output readable and avoids leaking formatting artifacts
from the KB files.
"""

def clean_markdown(text):

    cleaned_lines = []

    for line in text.splitlines():

        stripped = line.strip()

        # remove linhas vazias
        if not stripped:
            continue

        # remove títulos markdown mesmo com "-"
        if stripped.startswith("#"):
            continue

        if stripped.startswith("- #"):
            continue

        if stripped.startswith("##"):
            continue

        if stripped.startswith("###"):
            continue

        # remove "-" inicial mas mantém conteúdo
        if stripped.startswith("- "):
            stripped = stripped[2:]

        cleaned_lines.append(stripped)

    return "\n".join(cleaned_lines)



"""
Inspect model output and detect statistical concepts present.
This is a heuristic parser, not a full statistical parser.
The goal is simply to identify which explanations should be retrieved.
"""

def extract_statistical_signals(text: str) -> Dict[str, List[str]]:
    
    #Extracts interpretable statistical signals from model output.    
    signals = {
        "coefficients": [],
        "model_metrics": []
    }

    # Detect coefficients (very simple heuristic)
    coef_pattern = re.compile(r"(-?\d+\.\d+)")
    negative_found = False

    for line in text.splitlines():
        if coef_pattern.search(line):
            if "-" in line:
                negative_found = True

    if negative_found:
        signals["coefficients"].append(
            "interpretation of coefficients in linear regression model"
        )

    # Detect AIC / BIC
    if "AIC" in text:
        signals["model_metrics"].append("AIC interpretation in linear regression model")

    if "BIC" in text:
        signals["model_metrics"].append("BIC interpretation in linear regression model")
    
    # Detect p-values
    if "Pr(>|t|)" in text or "Pr(>|z|)" in text or "p-value" in text:
        signals["inference"] = ["interpretation of p-values in linear regression model"]

    # Detect standard errors
    if "Std. Error" in text or "Std Error" in text:
        signals.setdefault("inference", []).append(
        "interpretation of standard errors in regression"
    )
    
    # Detect log-lik
    if "log-lik" in text or "loglik)" in text or "logLik" in text:
        signals["inference"] = ["interpretation of log likelihood in linear regression model"]

    return signals



"""
Remove duplicate retrieval results and limit their size.
Retrieval systems sometimes return overlapping chunks.
This keeps output concise.
"""

def unique_and_trim(texts, max_chars=400):
    seen = set()
    cleaned = []

    for t in texts:
        t = t.strip()
        if t not in seen:
            seen.add(t)
            cleaned.append(t[:max_chars])

    return cleaned



"""
Main interpretation pipeline.
This function:
- detects statistical signals
- retrieves relevant explanations
- prints a structured report
It does not modify the model output itself.
It explains it.
"""

def interpret_model_output(text: str) -> None:

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Invalid model output")
        
    print("=== INTERPRETATION REPORT ===\n")

    logger.info("Interpreting model output (%d chars)", len(text))

    signals = extract_statistical_signals(text)

    logger.info("Detected signals: %s", list(signals.keys()))


    # --- Coefficients ---
    if signals["coefficients"]:
        print("## Coefficient Interpretation\n")
        for signal in signals["coefficients"]:
            logger.debug("Searching KB for signal: %s", signal)

            try:
                results = semantic_search(signal, k=2)
            except Exception as e:
                logger.error("Search failed for signal '%s': %s", signal, e)
                continue


            results = unique_and_trim(results)
            results = results[:1]

            for r in results:
                formatted = clean_markdown(r)
                paragraphs = formatted.split("\n")

                for p in paragraphs:
                    if p.strip():
                        print(" ", p)

                print()

        print()
        
     
    if "inference" in signals:

        print("## Statistical Inference\n")

        for q in signals["inference"]:
            logger.debug("Searching KB for signal: %s", signal)
            try:
                results = semantic_search(q, k=2)
            except Exception as e:
                logger.error("Search failed for signal '%s': %s", signal, e)
                continue
            results = unique_and_trim(results)
            results = results[:1]

            for r in results:
                formatted = clean_markdown(r)
                paragraphs = formatted.split("\n")

                for p in paragraphs:
                    if p.strip():
                        print(" ", p)

                print()

        print()

    # --- Model Metrics ---
    if signals["model_metrics"]:
        print("## Model Fit and Selection\n")
        for signal in signals["model_metrics"]:
            logger.debug("Searching KB for signal: %s", signal)
            try:
                results = semantic_search(signal, k=3)
            except Exception as e:
                logger.error("Search failed for signal '%s': %s", signal, e)
                continue
            results = unique_and_trim(results)
            results = results[:1]
            
            for r in results:
                formatted = clean_markdown(r)
                paragraphs = formatted.split("\n")

                for p in paragraphs:
                    if p.strip():
                        print(" ", p)

                print()

        print()        

    print("=== END OF REPORT ===")


# =========================
# CLI entry point
# Allows running the interpreter directly on example files.
# =========================

if __name__ == "__main__":
    example_file = EXAMPLES_PATH / "glm_output_R.txt"

    if not example_file.exists():
        raise FileNotFoundError(
            f"Example file not found: {example_file}"
        )

    model_output = example_file.read_text(encoding="utf-8")
    interpret_model_output(model_output)

