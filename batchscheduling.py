from operator import itemgetter
import sys

class Job:
    def __init__(self, arrival_time: float, job_id: int, requested_time: float, runtime: float, num_cpus: int):
        self.release_time = arrival_time
        self.id = job_id
        self.runtime_req = requested_time
        self.runtime_act = runtime
        self.machines = num_cpus
    
    def __repr__(self):
        return f"Job({self.id}, {self.release_time}, {self.runtime_req}, {self.runtime_act}, {self.machines})"

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


def main():
    inst = read_instance()
    M = inst.m
    Num_jobs = inst.n
    jobs = inst.jobs
    currently_free = M
    current_time = 0
    schedule = {}
    running = []
    for i in range(Num_jobs):
        if current_time < jobs[i].release_time:
            current_time = jobs[i].release_time
        running = sorted(running, key = itemgetter(1))
        ready_to_delte = 0
        for r in running:
            if r[1] < current_time:
                currently_free += jobs[r[0]].machines
                ready_to_delte += 1
                #running.remove(r)
            else:
                break
        for j in range(ready_to_delte):
            running.pop(0)

        if currently_free >= jobs[i].machines:
            schedule[i] = [jobs[i].id, current_time]
            currently_free -= jobs[i].machines
            current_time += 1
            running.append((jobs[i].id-1, jobs[i].release_time + jobs[i].runtime_act + 1))
        else:
            while(currently_free < jobs[i].machines):
                temp = running[0]
                current_time = jobs[temp[0]].release_time + jobs[temp[0]].runtime_act
                currently_free += jobs[temp[0]].machines
                running.pop(0)
            schedule[i] = [jobs[i].id, current_time]
            currently_free -= jobs[i].machines
            current_time += 1
            running.append((jobs[i].id-1, jobs[i].release_time + jobs[i].runtime_act + 1))

        #print('Free: '+ str(currently_free))
        #if currently_free < 0:
         #   print('RAISE')

    print(Num_jobs)
    for i in range(Num_jobs):
        print(str(schedule[i][0]) + ' ' + str(schedule[i][1]))

if __name__ == "__main__":
    main()