# Dataset Preparation Toolkit for Hate Speech Detection Experiments

This repository contains the dataset preprocessing and preparation scripts used in the paper:

> **Temporal Robustness in Hate Speech Detection: Updating German Classifiers with Advanced AI Infrastructures**  
> Submitted to **ECAI 2025**.

These scripts form the **data processing backbone** of our experimental pipeline.  
They are responsible for transforming heterogeneous, noisy, and temporally distributed hate speech datasets into clean, standardized formats ready for model training and evaluation.

## Why these scripts are needed

Working with multilingual hate speech data — especially across **time periods** — presents unique challenges:

- **Inconsistent formats** — datasets may arrive as TSV, CSV, or even broken exports with misaligned rows.
- **Noisy labels** — labels might be long text descriptions, integers, or missing entirely.
- **Variable structure** — different datasets may have different column names, orders, or delimiters.
- **Quality assurance** — detecting malformed lines, incorrect label formats, and structural inconsistencies is essential before training.
- **Reproducibility** — standardized preprocessing ensures experimental results are replicable.

Our scripts address these issues through **automated cleaning, normalization, merging, and verification**.

## Script categories & purposes

- **TSV utilities**: shuffle, split, validate, compute label distributions, detect special cases (emoji/single-word), combine datasets.
- **CSV utilities**: normalize label formats, repair malformed exports, extract specific columns, merge multiple datasets, format into `text,label`.
- **Validation & formatting tools**: check file integrity across directories, enforce column naming conventions, ensure reproducible preprocessing steps.

---
# TSV & CSV Utilities Toolkit

A small collection of Python scripts for wrangling **tab‑separated (TSV)** and **comma‑separated (CSV)** datasets.
Common tasks include shuffling and splitting datasets, validating and combining files, normalizing labels, extracting
text fields, and fixing quirky, semi‑structured CSV dumps.

> **Assumptions**
>
> - TSV scripts expect `\t` as the delimiter; CSV scripts expect `,`.
> - Most TSV helpers assume a header on the first row.
> - Several tools expect a two‑column layout: `text,label` (or `sentence,label`) with integer labels (e.g., `0`/`1`).

## Requirements

- Python 3.8+
- Packages:
  - `pandas` (used by: `splitter.py`, `shuffle.py`, `combine_tsv.py`, `extractor.py`)

Install:
```bash
pip install pandas
```

---

## TSV Scripts

### `splitter.py`
Randomly shuffles a TSV and splits it into two parts (default **80% / 20%**) while **preserving the header**.

**Usage**
```bash
python splitter.py <input_tsv_file> <output_file1> <output_file2>
```
**Notes**
- Loads TSV with `pandas`, shuffles rows, computes split by `split_ratio` (default 0.8), and writes two TSVs with the original header.
- Example: `python splitter.py data/all.tsv data/train.tsv data/dev.tsv`

---

### `shuffle.py`
Shuffles all rows of a TSV **without dropping the header** and writes the result to a new file.

**Usage**
```bash
python shuffle.py <input_tsv_file> <output_tsv_file>
```

---

### `tsv_split.py`
Creates a standard **train/dev** split from a single TSV (default **80% / 20%**), preserving the header in both outputs.

**Usage**
```bash
python tsv_split.py <input_file_path>
# -> outputs train.tsv and dev.tsv in the current folder
```

---

### `check_last_column_tsv.py`
Validates that each data row has **exactly two columns** and that the **last column** is an **integer**.
Prints a summary plus the **1‑based line numbers** of malformed rows.

**Usage**
```bash
python check_last_column_tsv.py <input_file_path>
```

---

### `percentage_calc.py`
Reports counts & percentages of rows whose **last field** is `0` vs `1`.

**Usage**
```bash
python percentage_calc.py <input_file_path>
```

---

### `emoji_detector.py`
Detect rows whose **text** is either (a) **only emojis** or (b) a **single word** (no spaces/punctuation).
Prints counts & percentages (header excluded).

**Usage**
```bash
python emoji_detector.py <input_file_path>
```

---

### `combine_tsv.py`
Concatenates **three** TSV files into one, **preserving headers** and column structure.

**Usage**
```bash
python combine_tsv.py <file1> <file2> <file3> <output_file>
```

---

## CSV Scripts

### `csv_combine.py`
Concatenate **N CSVs** into one CSV with a **standard header** `text,label`. Skips the header of each input and writes only
rows that have **exactly two columns**.

**Usage**
```bash
python csv_combine.py <output_file_path> <input_file_1> <input_file_2> ...
```
**When to use**
- You have multiple two‑column CSV shards and want a single `text,label` file.

---

### `labelling_csv.py`
Normalize string labels to **numeric** labels and standardize the header to `sentence,label`.
Mapping (as implemented):
- `"derogatory extreme speech"` → `0`
- `"exclusionary extreme speech"`, `"dangerous speech"` → `1`

Lines not matching these labels are **skipped**.

**Usage**
```bash
python labelling_csv.py <input_file_path> <output_file_path>
```

---

### `process_csv.py`
Cleans up messy, semi‑structured CSV dumps where label phrases (e.g. `"exclusionary extreme speech,"`, `"derogatory extreme speech,"`,
`"dangerous speech,"`) appear inline and rows may include a leading **timestamp** like `YYYY-MM-DD HH:MM:SS`.

**What it does**
- Reads header, flattens the rest into a single string, then **splits by the key label phrases** to reconstruct rows.
- Writes a provisional CSV (re‑using the original header), then **re‑opens and strips the leading timestamp** (keeps content **after** it).
- Final output is a cleaned CSV suitable for further processing.

**Usage**
```bash
python process_csv.py <input_csv_path> <output_csv_path>
```

---

### `csv_generator.py`
From a loosely formatted CSV line, **extracts the 3rd column** (handles quotes with embedded commas) and the **last field**
(often a label or trailing sentence fragment), then **writes them in switched order** as `third_column,last_field`.

**Usage**
```bash
python csv_generator.py <input_file_path> <output_file_path>
```

**Notes**
- Useful when you need a quick `text,label` style CSV from a source where the text is in the 3rd column and the label is the last field.

---

### `extractor.py`
Two‑stage helper for **repairing malformed CSVs** and **extracting selected columns**.

1) **Cleaning** — `clean_and_save_csv(input, temp)`
   - Ensures every row has the **expected number of columns** (based on the header).
   - Reassembles rows that were split across lines and preserves the original header.

2) **Column extraction** — `extract_columns(input, output, [col1 [col2 [col3]]])`
   - Uses `pandas` to select **1–3 named columns** and write a clean CSV.

**Usage**
```bash
# Clean + then extract specific columns
python extractor.py <input_csv_path> <output_csv_path> <column1> [<column2> <column3>]
```

---

### `text_extractor.py`
For each input line, extracts:
- **Texts inside double quotes** (if present), and
- The **last sentence before the final comma**

Then writes the extracted pair(s) to the output file. Handy when mining text from logs or loosely structured exports.

**Usage**
```bash
python text_extractor.py <input_file_path> <output_file_path>
```

---

## Example Workflows

### A) From messy CSV dumps → clean `text,label` CSV
```bash
# 1) Normalize/repair the CSV structure (if rows are broken across lines)
python extractor.py raw.csv cleaned.csv text label

# 2) If labels are spelled out as long phrases, normalize them to 0/1
python labelling_csv.py cleaned.csv labeled.csv

# 3) If you have multiple shards, combine them
python csv_combine.py all.csv shard1.csv shard2.csv shard3.csv
```

### B) TSV classification set → train/dev
```bash
python shuffle.py data/all.tsv data/all_shuffled.tsv
python splitter.py data/all_shuffled.tsv data/train.tsv data/dev.tsv
python percentage_calc.py data/train.tsv
python percentage_calc.py data/dev.tsv
python emoji_detector.py data/all.tsv
```

---

## Repository Layout (suggested)
```
.
├─ TSV/
│  ├─ splitter.py
│  ├─ shuffle.py
│  ├─ tsv_split.py
│  ├─ check_last_column_tsv.py
│  ├─ percentage_calc.py
│  ├─ emoji_detector.py
│  └─ combine_tsv.py
├─ CSV/
│  ├─ csv_combine.py
│  ├─ labelling_csv.py
│  ├─ process_csv.py
│  ├─ csv_generator.py
│  ├─ extractor.py
│  └─ text_extractor.py
└─ README.md
```

## License
Add your preferred license (e.g. MIT).

---

Want me to tailor this README with **your project name**, sample commands using **your real paths**, or expand the
label mappings? I can update it right away.

---

## Additional CSV Scripts

### `csv_extractor.py`
Extracts a specific set of columns from an input CSV and writes them to a new CSV.
- **Reads**: an input CSV (expects a header row).
- **Outputs**: CSV with only the requested columns, in the specified order.

**Usage**
```bash
python csv_extractor.py <input_csv> <output_csv> <colname1> [<colname2> ...]
```
- Accepts **1 or more** column names after the input/output arguments.

---

### `extractor_updated.py`
An updated/refactored version of `extractor.py` with potentially improved CSV repair logic or more flexible column extraction.
- Supports cleaning malformed CSVs (ensuring each row matches the expected header length).
- Can extract **1–N columns** by name.

**Usage**
```bash
python extractor_updated.py <input_csv> <output_csv> <colname1> [<colname2> ...]
```

---

### `file_checker.py`
Scans a directory for CSV/TSV files and validates:
- Presence of expected columns.
- Whether files have consistent column counts across rows.

Prints a summary report to the console.

**Usage**
```bash
python file_checker.py <directory_path>
```

---

### `formatter.py`
Reads a CSV and formats specific columns into a normalized `text,label` form.
- Can trim whitespace, unify case, or perform other basic cleaning.
- Writes the reformatted rows to a new CSV.

**Usage**
```bash
python formatter.py <input_csv> <output_csv>
```

---

## Repo Layout
```
.
├─ TSV/
│  ├─ splitter.py
│  ├─ shuffle.py
│  ├─ tsv_split.py
│  ├─ check_last_column_tsv.py
│  ├─ percentage_calc.py
│  ├─ emoji_detector.py
│  └─ combine_tsv.py
├─ CSV/
│  ├─ csv_combine.py
│  ├─ labelling_csv.py
│  ├─ process_csv.py
│  ├─ csv_generator.py
│  ├─ extractor.py
│  ├─ extractor_updated.py
│  ├─ csv_extractor.py
│  ├─ file_checker.py
│  ├─ formatter.py
│  └─ text_extractor.py
└─ README.md
```

---
