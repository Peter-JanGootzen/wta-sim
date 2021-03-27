#!/usr/bin/env python3.7
import itertools
import os
import subprocess

trace_dir = "C:/Users/L/Documents/vu/wta-sim/traces/"
output_location = "C:/Users/L/Documents/vu/wta-sim/experiment_output/"
slack_location = "C:/Users/L/Documents/vu/wta-sim/slack/"

machine_resources = [128, 12]
machine_tdps = [280, 95]
machine_base_clocks = [2.9, 4.1]
machine_fractions = [0.5, 0.5]

# Variations to try:
target_utilizations = [0.3]
task_selection_policies = ["fcfs"]
task_placement_policies = ["best_fit", "look_ahead"]
dvfs_enabled = [True, False]

subprocess.run("mvn package", shell=True)

for folder in next(os.walk(trace_dir))[1]:
    if folder == "alibaba_from_flat":
        continue  # Do not load the entire alibaba trace, too much.

    if "google" in str(folder).lower(): continue
    if "lanl" in str(folder).lower(): continue
    if "two_sigma" in str(folder).lower(): continue

    for tu, tsp, tpp, dvfs in itertools.product(target_utilizations, task_selection_policies,
                                                task_placement_policies, dvfs_enabled):
        output_dir = os.path.join(output_location, f"{folder}_tu_{tu}_tsp_{tsp}_tpp_{tpp}_dvfs_{dvfs}")
        if os.path.exists(output_dir):
            continue

        print(f"Running {output_dir}")
        command = f"""sbatch --job-name={output_dir}
               --output={output_dir}.out
               --error={output_dir}.err
               --time=24:00:00 """
        command += "java -Xmx60g -cp target/wta-sim-0.1.jar science.atlarge.wta.simulator.WTASim -f wta"
        command += " -c " + " ".join([str(x) for x in machine_resources])
        command += " -t " + " ".join([str(x) for x in machine_tdps])
        command += " -bc " + " ".join([str(x) for x in machine_base_clocks])
        command += " -mf " + " ".join([str(x) for x in machine_fractions])
        command += " -sd " + slack_location
        command += " -e " + " ".join([str(x) for x in [dvfs] * len(machine_resources)])
        command += " -i " + os.path.join(trace_dir, folder)
        command += " -o " + output_dir
        command += " --target-utilization " + str(tu)
        command += " --task-order-policy " + tsp
        command += " --task-placement-policy " + tpp

        subprocess.run(command, shell=True)
