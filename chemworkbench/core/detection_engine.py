from chemworkbench.core.technique_anchors import TECHNIQUE_ANCHORS
from chemworkbench.utils.normalization import (
    normalize_text,
    normalize_token,
    tokenize_header,
    normalize_path,
)
from chemworkbench.core.models import Technique


class DetectionEngine:
    """
    Technique detection engine for ChemWorkBench v2.

    Applies canonical normalization to all extracted text before
    scoring against weighted anchors and negative markers.
    """

    def __init__(self):
        self.anchors = TECHNIQUE_ANCHORS

    def detect(self, file_path: str, header: list[str], sample_text: str) -> Technique:
        """
        Detect the technique of a file using:
        - normalized file path
        - normalized header tokens
        - normalized sample text
        """
        norm_path = normalize_path(file_path)
        norm_header_tokens = [tok for h in header for tok in tokenize_header(h)]
        norm_text = normalize_text(sample_text)

        scores = {}

        for tech, block in self.anchors.items():
            score = 0

            # Structural: extensions
            for ext in block["extensions"]:
                if isinstance(ext, tuple):
                    pattern, weight = ext
                    if norm_path.endswith(pattern):
                        score += weight
                else:
                    if norm_path.endswith(ext):
                        score += 1

            # Semantic: header keywords
            for kw in block["header_keywords"]:
                if isinstance(kw, tuple):
                    pattern, weight = kw
                    if pattern in norm_header_tokens:
                        score += weight
                else:
                    if kw in norm_header_tokens:
                        score += 1

            # Semantic: keywords in text
            for kw in block["keywords"]:
                if isinstance(kw, tuple):
                    pattern, weight = kw
                    if pattern in norm_text:
                        score += weight
                else:
                    if kw in norm_text:
                        score += 1

            # Negative markers
            for neg in block["negative_markers"]:
                if isinstance(neg, tuple):
                    pattern, weight = neg
                    if pattern in norm_text or pattern in norm_path:
                        score += weight
                else:
                    if neg in norm_text or neg in norm_path:
                        score -= 1

            scores[tech] = score

        return max(scores, key=scores.get)
