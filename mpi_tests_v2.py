#! /usr/bin/python3
import subprocess as sp
import os

import flux
import flux.job

compilers = ["openmpi"]
mpis = ["clang"]

def main():
    handle = flux.Flux()
    failed_jobs = []
    for mpi in mpis:
        for compiler in compilers:
            jobspec = flux.job.JobspecV1.from_command(["/g/g0/hobbs17/mpihello/flux_mpi_test.sh", compiler, mpi], num_tasks=2, num_nodes=2)
            # jobspec.environment = dict(os.environ)
            jobid = flux.job.submit(handle, jobspec, debug=True)
            for stream, data in flux.job.output_watch(handle, jobid):
                print(f"{stream}: {data}", end="")
            jobinfo = flux.job.result(handle, jobid)
            if jobinfo.returncode != 0:
                failed_jobs.append(compiler)      
        print("The following compilers returned a non-zero exit code: ")
        for compiler in failed_jobs:
            print("    " + compiler)

main()
