# Beyond Memorization: Traffic Classification Under Changing Network Identifiers

**Project summary.** We will test how much operating-system and video-service classifiers depend on network identifiers, and whether changing IP addresses during training makes them more robust. This matters because shortcuts may produce high test accuracy without working on new networks. This project extends the ML/Net leaderboard benchmarks.

**Data.** We will use two public nPrint datasets:

- [OS detection](https://nprint.github.io/benchmarks/os_detection/nprint_os_detection.html): 100-packet samples, 13 operating-system classes, under 1 GB.
- [Streaming video services](https://nprint.github.io/benchmarks/application_identification/streaming_video_services.html): the first 10 SYN packets per session, four service classes, under 2 GB.

**Machine learning.** We will train random forest and logistic regression models separately on each dataset, comparing three approaches:

1. **Standard:** original IPv4/TCP nPrint features.
2. **Identifier removal:** remove source/destination IP addresses, TCP ports, and TCP sequence/acknowledgment numbers.
3. **Augmentation:** train on original samples plus copies with consistently remapped IP addresses, preserving labels and address relationships within each sample.

We will exclude checksums from all approaches so they cannot reveal the original addresses. The OS benchmark prohibits the fields removed in approach 2, so approaches 1 and 3 are diagnostic experiments for that task. The video benchmark has no prohibited fields.

**Evaluation.** We will split original samples into training, validation, and test sets before creating copies. Using the same splits across approaches, we will report balanced accuracy on original and newly remapped test samples, training time, and prediction flip rate: how often remapping changes a prediction. One plot will show the tradeoff between original and remapped accuracy. Where metadata and class coverage allow, we will also test on unseen hosts or capture groups. Remapping measures sensitivity to addresses; it does not establish generalization to real new networks.

**Learning objective.** We want to learn how strongly classifiers depend on identifiers and whether augmentation improves robustness more effectively than simply removing those fields.

**Work plan and deliverables.** Each teammate will handle one dataset and share the preprocessing and evaluation code. We will submit a clean notebook that runs end-to-end with results and data instructions.
