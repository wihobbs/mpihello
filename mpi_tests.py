#! /usr/bin/python3
import subprocess as sp

import flux
import flux.job

def main():
    handle = flux.Flux()
    failed_jobs = []
    compilers = []
    with open("/g/g0/hobbs17/mpihello/mpis_on_corona.txt") as textfile:
        compilers = [s.rstrip() for s in textfile.readlines()]
    for compiler in compilers:
        print("Using compiler: " + compiler)
        sp.run([compiler, "-o", "/g/g0/hobbs17/mpihello/mpi_handshake", "/g/g0/hobbs17/mpihello/mpi_handshake.c"])
        jobspec = flux.job.JobspecV1.from_command(["/g/g0/hobbs17/mpihello/mpi_handshake"], num_tasks=2, num_nodes=2)
        jobid = flux.job.submit(handle, jobspec, debug=True)
        for stream, data in flux.job.output_watch(handle, jobid):
            print(f"{stream}: {data}", end="")
        jobinfo = flux.job.result(handle, jobid)
        # print("Flux job " + jobid.f58 + " has finished with return code " + str(jobinfo.returncode))
        if jobinfo.returncode != 0:
            failed_jobs.append(compiler)      
    print("The following compilers returned a non-zero exit code: ")
    for compiler in failed_jobs:
        print("    " + compiler)

main()
