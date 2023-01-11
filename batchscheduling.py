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
    inst = read_instance('student_instance_2.dat')
    M = inst.m
    Num_jobs = inst.n
    jobs = inst.jobs
    currently_free = M
    current_time = 0
    schedule = {}
    running = []
    backfill = []
    for i in range(Num_jobs):
        if i in backfill:
            continue
        if current_time < jobs[i].release_time:
            current_time = jobs[i].release_time
        running = sorted(running, key = itemgetter(1))
        ready_to_delte = 0
        for r in running:
            if r[1] < current_time:
                currently_free += jobs[r[0]].machines
                ready_to_delte += 1
            else:
                break
        for j in range(ready_to_delte):
            running.pop(0)

        if currently_free >= jobs[i].machines:
            schedule[i] = [jobs[i].id, current_time]
            currently_free -= jobs[i].machines
            running.append((jobs[i].id-1, current_time + jobs[i].runtime_act, current_time+jobs[i].runtime_req))
        else:
            
            shadow_time_temp =  sorted(running, key = itemgetter(2), reverse=True)
            free_temp = M
            shadow_time = shadow_time_temp[0][2]

            for cores in shadow_time_temp:
                if jobs[i].machines >= (free_temp - jobs[cores[0]].machines):
                    break
                else:
                    free_temp = free_temp - jobs[cores[0]].machines
                    shadow_time = cores[2]

            #print(shadow_time)
            extra_nodes = free_temp - jobs[i].machines

            for j in range(i+1, Num_jobs):
                run_time = current_time + jobs[j].runtime_req
                if jobs[j].machines <= currently_free:
                    if (run_time < shadow_time) or jobs[j].machines <= extra_nodes:
                        current_time = max(current_time, jobs[j].release_time)
                        schedule[j] = [jobs[j].id, current_time]
                        currently_free -= jobs[j].machines
                        running.append((jobs[j].id-1, current_time + jobs[j].runtime_act, current_time+jobs[j].runtime_req))
                        backfill.append(jobs[j].id-1)
                
                running = sorted(running, key = itemgetter(1))
                while True:
                    if len(running) == 0:
                        break
                    if current_time <= running[0][1]:
                        break
                    else:
                        currently_free += jobs[running[0][0]].machines
                        running.pop(0)

                while(currently_free < jobs[i].machines):
                    temp = running[0]
                    current_time = temp[1]
                    currently_free += jobs[temp[0]].machines
                    running.pop(0)
                if currently_free >= jobs[i].machines:
                    schedule[i] = [jobs[i].id, current_time]
                    currently_free -= jobs[i].machines
                    running.append((jobs[i].id-1, current_time + jobs[i].runtime_act, current_time+jobs[i].runtime_req))
                    break

            if i == Num_jobs-1:
                while(currently_free < jobs[i].machines):
                    temp = running[0]
                    current_time = temp[1]
                    currently_free += jobs[temp[0]].machines
                    running.pop(0)
                schedule[i] = [jobs[i].id, current_time]
                currently_free -= jobs[i].machines
                running.append((jobs[i].id-1, current_time + jobs[i].runtime_act, current_time+jobs[i].runtime_req))

            while(currently_free < jobs[i].machines):
                temp = running[0]
                current_time = temp[1]
                currently_free += jobs[temp[0]].machines
                running.pop(0)

    """ schedule[i] = [jobs[i].id, current_time]
            currently_free -= jobs[i].machines
            running.append((jobs[i].id-1, current_time + jobs[i].runtime_act, current_time+jobs[i].runtime_req))
            """
        #print('Free: '+ str(currently_free))
        #if currently_free < 0:
            #print('RAISE')

    print(Num_jobs)
    for i in range(Num_jobs):
        print(str(schedule[i][0]) + ' ' + str(schedule[i][1]))

if __name__ == "__main__":
    main()