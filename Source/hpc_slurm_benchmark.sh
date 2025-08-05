#!/bin/bash
#SBATCH --job-name=dna_benchmark
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err
#SBATCH --time=02:00:00
#SBATCH --mem=8G
#SBATCH --cpus-per-task=4

# Load conda environment
module load anaconda          # adapt if your cluster uses different module name
source $(conda info --base)/etc/profile.d/conda.sh
conda activate dna_project_env

# Set variables
PATH_ORIGINAL_DATA="/../Data/Original/"
PATH_BENCHMARK_PY="benchmark_hpc.py"
PATH_MERGE_PY="merge_benchmark_hpc.py"
NUM_OF_RUNS=5

# Get array size dynamically (files only, exclude directories)
mapfile -t FILES < <(find "$PATH_ORIGINAL_DATA" -maxdepth 1 -type f -printf '%f\n')
NUM_FILES=${#FILES[@]}

if [ $NUM_FILES -eq 0 ]; then
  echo "No files found in $PATH_ORIGINAL_DATA. Exiting."
  exit 1
fi

echo "Found $NUM_FILES files to process."

# If this script is called with an SLURM_ARRAY_TASK_ID, run the corresponding job
if [ -n "$SLURM_ARRAY_TASK_ID" ]; then
  if [ "$SLURM_ARRAY_TASK_ID" -ge "$NUM_FILES" ]; then
    echo "SLURM_ARRAY_TASK_ID ($SLURM_ARRAY_TASK_ID) out of bounds (max index $((NUM_FILES - 1))). Exiting."
    exit 1
  fi

  FILE=${FILES[$SLURM_ARRAY_TASK_ID]}
  BASENAME="${FILE%.*}"
  echo "Running benchmark on file: $FILE (basename: $BASENAME)"

  python "$PATH_BENCHMARK_PY" --file "$BASENAME" --num_of_runs "$NUM_OF_RUNS"
  exit 0
fi

# Otherwise (no SLURM_ARRAY_TASK_ID) this is the submission point: submit the array job
echo "Submitting array job with $NUM_FILES tasks..."

JOB_ID=$(sbatch --parsable --array=0-$((NUM_FILES - 1)) $0)

echo "Submitted array job with JOB_ID=$JOB_ID"

# Wait for array job completion
echo "Waiting for job $JOB_ID to complete..."
squeue --job $JOB_ID > /dev/null
while squeue --job $JOB_ID | grep "$JOB_ID" > /dev/null; do
  sleep 30
done

echo "Array job $JOB_ID finished."

# Run the merge script after all jobs finished
echo "Running merging script..."
python "$PATH_MERGE_PY"

echo "All done."
