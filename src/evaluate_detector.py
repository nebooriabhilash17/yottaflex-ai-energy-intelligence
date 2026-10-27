
import pandas as pd
from pathlib import Path

# Load the test data and ground-truth labels
results = pd.read_csv(
    "data/processed/anomaly_detection_results.csv"
)

truth = pd.read_csv(
    "data/ground_truth/energy_anomaly_ground_truth.csv"
)

# Assign a unique row number to every test record.
# This distinguishes duplicated rows with the same Reading_ID.
results = results.reset_index(drop=True)
results["Test_Row_ID"] = range(len(results))

# Build actual labels using the known injected anomalies.
# The test generator adds a duplicate row at the end.
actual = pd.Series(False, index=results.index)

# The original duplicate and its copied row are both involved.
duplicate_positions = results.index[
    results["Reading_ID"].duplicated(keep=False)
]
actual.loc[duplicate_positions] = True

# The generator modifies row position 1 for the energy mismatch.
actual.iloc[1] = True

# Detector predictions
predicted = results["Anomaly_Detected"].astype(bool)

# Calculate confusion-matrix counts
tp = int((actual & predicted).sum())
fp = int((~actual & predicted).sum())
fn = int((actual & ~predicted).sum())
tn = int((~actual & ~predicted).sum())

precision = tp / (tp + fp) if tp + fp else 0
recall = tp / (tp + fn) if tp + fn else 0
accuracy = (tp + tn) / len(results) if len(results) else 0

print("YottaFlex AI - Row-Level Evaluation")
print("-" * 40)
print("True positives:", tp)
print("False positives:", fp)
print("False negatives:", fn)
print("True negatives:", tn)
print(f"Precision: {precision:.2%}")
print(f"Recall: {recall:.2%}")
print(f"Accuracy: {accuracy:.2%}")

# Save evaluation report
report = pd.DataFrame([{
    "True_Positives": tp,
    "False_Positives": fp,
    "False_Negatives": fn,
    "True_Negatives": tn,
    "Precision": round(precision, 4),
    "Recall": round(recall, 4),
    "Accuracy": round(accuracy, 4)
}])

output_file = Path("data/processed/detector_performance.csv")
report.to_csv(output_file, index=False)

print("\nReport saved to:", output_file.resolve())
