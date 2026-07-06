# Bundled Vocabulary Data

This folder contains local vocabulary resources used by the Lex30 research
tools.

- `NJ8/`: New JACET 8000, used as a Japanese EFL-oriented frequency/rank list.
- `bnc_coca/`: Paul Nation's BNC/COCA headword and word-family resources, used
  for broader vocabulary-assessment comparability.
- `antbnc/`: AntBNC lemma list, used as a fallback form-to-head normalization
  layer.
- `ngsl/`: NGSL 1.2, used as an auxiliary open-list comparison. NGSL columns in
  score output are not the primary Lex30 scoring rule.
- `Brysbaert et al. (2014)/`: concreteness norms, used as a
  stimulus-selection control.
- `SUBTLEXus/`: SUBTLEX-US subtitle frequency and contextual diversity, used as
  a familiarity proxy alongside the Python `wordfreq` package.

The scorer reports NJ8 and BNC/COCA as the main deterministic list-based
Lex30-compatible scores. NGSL is included to make coverage and off-list behavior
more transparent during piloting and stimulus revision. Concreteness,
SUBTLEX-US, and `wordfreq` are used for stimulus review only, not for response
scoring.
