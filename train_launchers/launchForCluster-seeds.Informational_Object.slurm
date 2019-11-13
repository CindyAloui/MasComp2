#! /bin/bash
#SBATCH -J out/train_seeds.Informational_Object
#SBATCH -p skylake
#SBATCH -N 2
#SBATCH --ntasks-per-node=3
#SBATCH -t 2-12
#SBATCH -o %x.stdout
#SBATCH -e %x.stderr


# chargement des modules
module purge
module load userspace/all
module load blas/gcc72/3.7.1
module load intel-mkl/64/2018.3.222
module load lapack/gcc72/3.7.1
module load gcc/7.2.0
module load python3/3.6.3
module load cuda/10.1

python3 train.py data/seeds/seeds-super-supersenses/seeds.Informational_Object data/seeds/seeds-super-supersenses/not_seeds.Informational_Object data/frWaC/mcf_seeds.Informational_Object/ seeds.Informational_Object