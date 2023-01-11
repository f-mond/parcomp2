import heapq
from operator import itemgetter
import sys

class Job:
    def __init__(self, job_id, start_time, requested_runtime, actual_runtime, cores):
        self.job_id = job_id
        self.start_time = start_time
        self.requested_runtime = requested_runtime
        self.actual_runtime = actual_runtime
        self.cores = cores
    
    def __lt__(self, other):
        return self.start_time + self.actual_runtime < other.start_time + other.actual_runtime
    
    def __repr__(self):
        return f"Job({self.job_id}, {self.start_time}, {self.requested_runtime}, {self.actual_runtime}, {self.cores})"

class Instance:
    def __init__(self, m: int, jobs: list):
        self.m = m
        self.n = len(jobs)
        self.jobs = jobs
    
    def __repr__(self):
        jobs = '[\n\t{}\n]'.format(",\n\t".join(map(str, self.jobs)))
        return f"Instance(m={self.m}, n={self.n}, jobs={jobs})"

def read_instance(infile=None):
    if infile is None:
        f = sys.stdin
    else:
        f = open(infile, "r")
    jobs = []
    p = int(f.readline().strip())
    n = int(f.readline().strip())
    for _ in range(n):
        arrival_time, job_id, requested_time, runtime, num_cpus = f.readline().split()
        jobs.append(Job(int(arrival_time), int(job_id), int(requested_time), int(runtime), int(num_cpus)))
    
    return Instance(p, jobs)

""" def schedule(num_cores, jobs):
    scheduled_jobs = []
    job_queue = []
    core_availability = [0] * num_cores
    
    for job in jobs:
        heapq.heappush(job_queue, (job.actual_runtime, job))
    
    while job_queue:
        job_runtime, job = heapq.heappop(job_queue)
        start_time = min(core_availability)
        core_idx = core_availability.index(start_time)
        
        job.start_time = max(start_time, job.start_time)
        core_availability[core_idx] = job.start_time + job.actual_runtime
        scheduled_jobs.append((job.job_id, job.start_time))
    
    return scheduled_jobs """

def schedule(num_cores, jobs):
    scheduled_jobs = []
    job_queue = []
    unscheduled_jobs = []
    core_availability = [0] * num_cores
    
    for job in jobs:
        heapq.heappush(job_queue, (job.actual_runtime, job))
    
    while job_queue:
        job_runtime, job = heapq.heappop(job_queue)
        start_time = min(core_availability)
        core_idx = core_availability.index(start_time)
        
        # Check if scheduling this job would exceed the number of available cores
        cores_in_use = sum(t > start_time for t in core_availability)
        if cores_in_use + job.cores > num_cores:
            heapq.heappush(unscheduled_jobs, (job.actual_runtime, job))
            continue

        job.start_time = max(start_time, job.start_time)
        for i in range(job.cores):
            core_availability[core_idx+i] = job.start_time + job.actual_runtime
        scheduled_jobs.append((job.job_id, job.start_time))

    for unscheduled_job in unscheduled_jobs:
        _, job = unscheduled_job
        start_time = min(core_availability)
        core_idx = core_availability.index(start_time)
        job.start_time = max(start_time, job.start_time)
        for i in range(job.cores):
            if core_idx + i >= num_cores:
                break
            core_availability[core_idx+i] = job.start_time + job.actual_runtime
        scheduled_jobs.append((job.job_id, job.start_time))
    return scheduled_jobs

""" def schedule(num_cores, jobs):
    scheduled_jobs = []
    cores_in_use = [0] * num_cores
    job_queue = []
    waiting_queue = []

    for job in jobs:
        heapq.heappush(job_queue, job)

    while job_queue:
        job = heapq.heappop(job_queue)
        
        # check if there's a job in the waiting queue that can be scheduled
        while len(waiting_queue) > 0:
            next_job = waiting_queue.pop()
            core_idx = cores_in_use.index(min(cores_in_use))
            start_time = cores_in_use[core_idx]
            print(num_cores)
            print(cores_in_use.count(0))
            print(num_cores-cores_in_use.count(0))
            available_cores = num_cores - cores_in_use.count(0)
            if available_cores >= next_job.cores:
                job = next_job
                break
            else:
                heapq.heappush(job_queue, next_job)
        
        core_idx = cores_in_use.index(min(cores_in_use))
        start_time = cores_in_use[core_idx]
        available_cores = num_cores - cores_in_use.count(0)
        
        # Check if scheduling this job would exceed the number of available cores
        if available_cores < job.cores:
            heapq.heappush(waiting_queue, job)
            continue

        # Schedule the job
        job.start_time = max(start_time, job.start_time)
        scheduled_jobs.append((job.job_id, job.start_time))

        for i in range(job.cores):
            cores_in_use[core_idx+i] = job.start_time + job.actual_runtime

        for idx, usage_time in enumerate(cores_in_use):
            if usage_time <= job.start_time + job.actual_runtime:
                cores_in_use[idx] = 0
        
        for i in range(job.cores):
            cores_in_use[core_idx+i] = job.start_time + job.actual_runtime
    return scheduled_jobs """


def main():
    inst = read_instance('student_instance_1.dat')
    M = inst.m
    Num_jobs = inst.n
    jobs = inst.jobs
    cores = M
    new_joblist = []
    #for i in range(Num_jobs):
     #   new_joblist.append((jobs[i].start_time, jobs[i].runtime_req, jobs[i].actual_runtime, jobs[i].cores))
    sched = schedule(cores, jobs)
    schedule_list = sorted(sched, key=lambda x: x[1])
    
    print(Num_jobs)
    for i in range(Num_jobs):
        print((str(schedule_list[i][1]) + ' ' + str(schedule_list[i][0])))

if __name__ == "__main__":
    main()