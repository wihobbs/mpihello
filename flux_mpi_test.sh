#! /bin/bash

module load $1 $2
module list
mpicc -o /g/g0/hobbs17/mpihello/mpi_handshake /g/g0/hobbs17/mpihello/mpi_handshake.c
echo "PATH="$PATH
echo "FLUX_EXEC_PATH="$FLUX_EXEC_PATH
FLUX_PYCLI_LOGLEVEL=10 flux start flux run -N2 -n2 -vvv /g/g0/hobbs17/mpihello/mpi_handshake 
