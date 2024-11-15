#!/bin/bash
#SBATCH --job-name=unit-test-networks
#SBATCH --partition=ckpt
#SBATCH --account=cse
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=500G
#SBATCH --gres=gpu:0
#SBATCH --time=10:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=wagnew3@uw.edu

source ~/.bashrc
conda activate whatisai
cd /gscratch/prl/wagnew3/whatisai/src/
echo "-----------"
echo $1
PYTHONPATH=/gscratch/prl/wagnew3/whatisai/ python save_ml_patents.py --data_dir=/gscratch/prl/wagnew3/microsoft_academic_graph/ $1


