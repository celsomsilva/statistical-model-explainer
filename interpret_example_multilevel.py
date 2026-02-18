import re
from typing import Dict, List
from retrieval.search import semantic_search
from retrieval.logging_config import setup_logging
logger = setup_logging("interpret.linear")



def clean_markdown(text: str) -> str:
    """
    Remove markdown artifacts and bullet symbols for clean reporting.
    """
    cleaned_lines = []

    for line in text.splitlines():

        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("#"):
            continue

        if stripped.startswith("##"):
            continue

        if stripped.startswith("###"):
            continue

        if stripped.startswith("---"):
            continue

        if stripped.startswith("- "):
            stripped = stripped[2:]

        cleaned_lines.append(stripped)

    return "\n".join(cleaned_lines)


def unique_and_trim(results: List[str]) -> List[str]:

    seen = set()
    unique = []

    for r in results:

        key = r[:120]

        if key not in seen:

            seen.add(key)
            unique.append(r)

    return unique


def extract_multilevel_signals(text: str) -> Dict[str, List[str]]:

    signals = {}

    if "lme(" in text or "Random effects" in text:

        signals["model_type"] = [
            "interpretation of nlme lme model with nested random effects"
        ]

    if "Fixed effects" in text:

        signals["fixed"] = [
            "interpretation of fixed effects in multilevel model"
        ]

    if "Random effects" in text:

        signals["variance"] = [
            "interpretation of random effects variance components"
        ]

    if "AIC" in text or "BIC" in text:

        signals["metrics"] = [
            "model selection criteria in multilevel models AIC BIC REML ML"
        ]

    return signals


def interpret_multilevel_output(text: str):

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Invalid model output")


    print("=== MULTILEVEL MODEL INTERPRETATION ===\n")
    
    logger.info("Interpreting model output (%d chars)", len(text))

    signals = extract_multilevel_signals(text)
    
    logger.info("Detected signals: %s", list(signals.keys()))

    if "model_type" in signals:

        print("## Model Type\n")

        for q in signals["model_type"]:
        
            logger.debug("Searching KB for signal: %s", q)
            try:
                results = semantic_search(q, k=3)
            except Exception as e:
                logger.error("Search failed for signal '%s': %s", q, e)
                continue

            results = unique_and_trim(results)

            results = results[:1]

            for r in results:

                formatted = clean_markdown(r)

                for p in formatted.split("\n"):

                    if p.strip():

                        print(" ", p)

                print()

    if "fixed" in signals:

        print("## Fixed Effects\n")

        for q in signals["fixed"]:
        
            logger.debug("Searching KB for signal: %s", q)
            try:
                results = semantic_search(q, k=3)
            except Exception as e:
                logger.error("Search failed for signal '%s': %s", q, e)
                continue

            results = unique_and_trim(results)

            results = results[:1]

            for r in results:

                formatted = clean_markdown(r)

                for p in formatted.split("\n"):

                    if p.strip():

                        print(" ", p)

                print()

    if "variance" in signals:

        print("## Variance Components\n")

        for q in signals["variance"]:
        
            logger.debug("Searching KB for signal: %s", q)
            try:	
                results = semantic_search(q, k=3)
            except Exception as e:
                logger.error("Search failed for signal '%s': %s", q, e)
                continue

            results = unique_and_trim(results)

            results = results[:1]

            for r in results:

                formatted = clean_markdown(r)

                for p in formatted.split("\n"):

                    if p.strip():

                        print(" ", p)

                print()

    if "metrics" in signals:

        print("## Model Metrics\n")

        for q in signals["metrics"]:

            logger.debug("Searching KB for signal: %s", q)
            try:
                results = semantic_search(q, k=3)
            except Exception as e:
                logger.error("Search failed for signal '%s': %s", q, e)
                continue


            results = unique_and_trim(results)

            results = results[:1]

            for r in results:

                formatted = clean_markdown(r)

                for p in formatted.split("\n"):

                    if p.strip():

                        print(" ", p)

                print()

    print("=== END OF REPORT ===")


if __name__ == "__main__":

    with open("examples/hlm_output_multilevel_R.txt") as f:

        text = f.read()

    interpret_multilevel_output(text)
