from parse_batch_instance import read_instance, Instance, Job
from operator import itemgetter

def main():
    inst = read_instance('instances/student_instance_1.dat')
    M = inst.m
    Num_jobs = inst.n
    jobs = inst.jobs
    currently_free = M
    current_time = 0
    schedule = {}
    running = []
    for i in range(Num_jobs):
        running = sorted(running, key = itemgetter(1))
        for r in running:
            if r[1] <= current_time:
                currently_free += jobs[r[0]].machines
                running.remove(r)
            else:
                break
        if currently_free >= jobs[i].machines:
            schedule[i] = [jobs[i].id, jobs[i].release_time]
            currently_free -= jobs[i].machines
            current_time = jobs[i].release_time
            running.append((jobs[i].id-1, jobs[i].release_time + jobs[i].runtime_act))
        else:
            while(currently_free < jobs[i].machines):
                temp = running[0]
                current_time = jobs[temp[0]].release_time + jobs[temp[0]].runtime_act
                currently_free += jobs[temp[0]].machines
                running.pop(0)
            schedule[i] = [jobs[i].id, jobs[i].release_time]
            currently_free -= jobs[i].machines
            current_time = jobs[i].release_time
            running.append((jobs[i].id-1, jobs[i].release_time + jobs[i].runtime_act))

    print(Num_jobs)
    for i in range(Num_jobs):
        print(str(schedule[i][0]) + ' ' + str(schedule[i][1]))

if __name__ == "__main__":
    main()