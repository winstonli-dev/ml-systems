# Assignment 2: NetDiffusion

Open **[NetDiffusion_Simple.ipynb](NetDiffusion_Simple.ipynb)**. It contains the original seven questions, short answers, image comparisons, and a simple random forest using the first three packets of each trace.

## Run

1. Select your Python 3 notebook kernel. If dependencies are missing, run `%pip install -r requirements.txt` from a cell in this folder.
2. The data is already downloaded locally. On a fresh checkout, download [nd_data.zip](https://drive.google.com/file/d/1hY6nNXEYOwl1l-O_nCknO9xezcHr6ZXi/view) and extract it **inside `nd_data/`**, so it contains `real_nprints/` and `generated_traffic_images/`.
3. Run the notebook from top to bottom, starting in this folder or the repository root. Conversion takes a few minutes. No GPU or diffusion-model installation is required.

There are 200 real traces and 100 generated images, covering 10 applications. Downloaded data and intermediate conversions stay in the ignored `nd_data/` folder. Small plots and classification summaries are saved in `results/` and in the notebook outputs.

## What was completed

- **Q1–Q3:** inspect packet fields, create grayscale images from at most 1,024 packets, run the NetDiffusion color conversion, and compare the encodings.
- **Q4–Q6:** compare real/generated images, explain reconstruction, run the provided correction and decoding scripts, and check every reconstructed table.
- **Q7:** flatten the first three packets, train a random forest on synthetic nPrints, test it on real nPrints, and report accuracy, macro F1, a majority-class baseline, per-application scores, and a confusion matrix.

Q7 follows **synthetic → real**: train on `generated_nprint/` and evaluate on `real_nprints/`. The data does not identify the generator's training captures, so these results cannot establish generalization to captures unseen by the generator.

## Results

All 14 code cells executed successfully. All 100 reconstructed tables have the expected 1,024 rows, 1,088 header-bit columns, and only `-1/0/1` values.

| Training → testing | Accuracy | Macro F1 | Majority baseline |
|---|---:|---:|---:|
| Synthetic → real | 26.5% | 0.176 | 10.0% |

The model beats the baseline, but four applications have no correct predictions. The synthetic data transfers application information poorly in this experiment. See the notebook's conclusion and [saved metrics](results/classification_results.csv).

## Source and small fixes

Imported from [noise-courses/netdiffusion](https://github.com/noise-courses/netdiffusion/tree/eb813253cc3174c05eef1f9f8e2935bbe313bec2), commit `eb813253cc3174c05eef1f9f8e2935bbe313bec2`.

All supplied scripts and reference files are included. `scripts/nprint_to_png.py` was simplified for the assignment's `-1/0/1` data: it drops the saved row index, enforces the 1,024-packet limit, checks the input values, and overwrites existing images on reruns. It preserves the supplied color mapping and padding. The original script's alpha-channel encoding of other integers is unnecessary once the row index is removed.

`color_processor.py` and `image_to_nprint.py` are unchanged. Q6 explains the unreachable green/blue threshold branches in the supplied color processor. Table validation does not prove protocol correctness or replayability. The optional PCAP reconstruction and GPU training scripts are included but are not needed for the assignment and were not run; their extra dependencies are outside `requirements.txt`.
