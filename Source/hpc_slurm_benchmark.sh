#!/bin/bash
#SBATCH --job-name=dna_benchmark
#SBATCH --output=logs/%x_%A_%a.out
#SBATCH --error=logs/%x_%A_%a.err
#SBATCH --partition=long
#SBATCH --time=10-02
#SBATCH --mem=50G
#SBATCH --cpus-per-task=8
#SBATCH --mail-user=AnzelA@rki.de

# Load conda environment
module load anaconda
source $(conda info --base)/etc/profile.d/conda.sh
conda activate unacorm_env

mkdir -p logs
rm -f logs/*

echo "Started benchmark"

python benchmark_hpc.py

echo "Benchmark and merge done"
