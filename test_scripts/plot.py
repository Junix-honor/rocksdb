import datetime
import time
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.pyplot import MultipleLocator
from data_process import *
from collections import Counter

NAME = "rocksdb_result_14400s_64M_2_100B_1fg_4bg_0mutidb_1682727030_no_intra_l0"

fig, (throughput_ax, score_ax, l0_ax, compaction_needed_bytes_ax, memtable_ax, schedule_ax, compaction_throughput_ax, cpu_ax, high_cpu_ax, low_cpu_ax, pidstat_io_write_ax, pidstat_io_read_ax, pidstat_high_io_write_ax, pidstat_high_io_read_ax, pidstat_low_io_write_ax, pidstat_low_io_read_ax, io_bw_ax, io_req_size_ax, io_que_size_ax) = plt.subplots(19, 1, figsize=(
    200, 50), layout='constrained', sharex=True)
fig.suptitle(NAME, fontsize="xx-large", fontweight="medium")

#! start_time
with open('./data/'+NAME+'/exp_op_time', 'r') as f:
    number = int(f.read())
# print(number)
db_start_time_raw = time.localtime(number)
# print(db_start_time_raw)
db_start_time_str = str(db_start_time_raw[3])+":" + \
    str(db_start_time_raw[4])+":"+str(db_start_time_raw[5])
# print(db_start_time_str)
db_start_time = time.strptime(db_start_time_str, "%H:%M:%S")
# print(db_start_time)

#! op_data
op_time, interval_compaction_throughput = process_op_data(
    './data/'+NAME+'/exp_op_data')
# print(interval_compaction_throughput)
# *compaction_speed
compaction_throughput_ax.plot(op_time,
                              interval_compaction_throughput, label="compaction_throughput", alpha=0.7)
compaction_throughput_ax.set_xlabel("Time(s)")
compaction_throughput_ax.set_ylabel("Throughput(MB/s)")
# compaction_throughput_ax.set_ylim(0, 3000)
compaction_throughput_ax.grid()
compaction_throughput_ax.set_title("the throughput of the compaction", fontsize="large",
                   loc='left', fontstyle='oblique')

#! flush
flush_data = pd.read_csv('./data/'+NAME+'/exp_flush.csv', encoding='utf-8',
                         names=["start", "end"], header=0)
memtable_ax.axvspan(0, 0, alpha=0.3, color='green', label="flush")
for index, row in flush_data.iterrows():
    memtable_ax.axvspan(row["start"], row["end"], alpha=0.3, color='green')

#! stall
stall_data = pd.read_csv('./data/'+NAME+'/exp_stall.csv', encoding='utf-8',
                         names=["type", "cause", "start", "end"], header=0)
stall_memtable_num = []
stall_l0_num = []

kDelayed_kL0FileCountLimit = stall_data[(
    stall_data["type"] == "kDelayed") & (stall_data["cause"] == "kL0FileCountLimit")]
start_list = kDelayed_kL0FileCountLimit["start"].tolist()
end_list = kDelayed_kL0FileCountLimit["end"].tolist()
for i in range(len(start_list)):
    throughput_ax.axvspan(
        start_list[i], end_list[i], alpha=0.3, color='yellow', ls="--")
    # print(end_list[i]-start_list[i])
    stall_l0_num.append((start_list[i], 20))
    pidstat_io_write_ax.axvspan(
        start_list[i], end_list[i], alpha=0.3, color='yellow', ls="--")
    cpu_ax.axvspan(
        start_list[i], end_list[i], alpha=0.3, color='yellow', ls="--")
throughput_ax.axvspan(0, 0, alpha=0.3, color='yellow',
                      label="kDelayed_kL0FileCountLimit")
pidstat_io_write_ax.axvspan(0, 0, alpha=0.3, color='yellow',
                      label="kDelayed_kL0FileCountLimit")
cpu_ax.axvspan(0, 0, alpha=0.3, color='yellow',
               label="kDelayed_kL0FileCountLimit")

kDelayed_kMemtableLimit = stall_data[(
    stall_data["type"] == "kDelayed") & (stall_data["cause"] == "kMemtableLimit")]
start_list = kDelayed_kMemtableLimit["start"].tolist()
end_list = kDelayed_kMemtableLimit["end"].tolist()
for i in range(len(start_list)):
    throughput_ax.axvspan(start_list[i], end_list[i], alpha=0.3, color='gold')
    stall_memtable_num.append((start_list[i], 1))
    pidstat_io_write_ax.axvspan(start_list[i], end_list[i], alpha=0.3, color='gold')
    cpu_ax.axvspan(start_list[i], end_list[i], alpha=0.3, color='gold')

throughput_ax.axvspan(0, 0, alpha=0.3, color='gold',
                      label="kDelayed_kMemtableLimit")
pidstat_io_write_ax.axvspan(0, 0, alpha=0.3, color='gold',
                      label="kDelayed_kMemtableLimit")
cpu_ax.axvspan(0, 0, alpha=0.3, color='gold',
               label="kDelayed_kMemtableLimit")

kDelayed_kPendingCompactionBytes = stall_data[(
    stall_data["type"] == "kDelayed") & (stall_data["cause"] == "kPendingCompactionBytes")]
start_list = kDelayed_kPendingCompactionBytes["start"].tolist()
end_list = kDelayed_kPendingCompactionBytes["end"].tolist()
for i in range(len(start_list)):
    throughput_ax.axvspan(start_list[i], end_list[i], alpha=0.3, color='olive')
    # print(end_list[i]-start_list[i])
    pidstat_io_write_ax.axvspan(start_list[i], end_list[i], alpha=0.3, color='olive')
    cpu_ax.axvspan(start_list[i], end_list[i], alpha=0.3, color='olive')
throughput_ax.axvspan(0, 0, alpha=0.3, color='olive',
                      label="kDelayed_kPendingCompactionBytes")
pidstat_io_write_ax.axvspan(0, 0, alpha=0.3, color='olive',
                      label="kDelayed_kPendingCompactionBytes")
cpu_ax.axvspan(0, 0, alpha=0.3, color='olive',
               label="kDelayed_kPendingCompactionBytes")

kStopped_kL0FileCountLimit = stall_data[(
    stall_data["type"] == "kStopped") & (stall_data["cause"] == "kL0FileCountLimit")]
start_list = kStopped_kL0FileCountLimit["start"].tolist()
end_list = kStopped_kL0FileCountLimit["end"].tolist()
for i in range(len(start_list)):
    throughput_ax.axvspan(
        start_list[i], end_list[i], alpha=0.3, color='green', ls="--")
    stall_l0_num.append((start_list[i], 36))
    pidstat_io_write_ax.axvspan(
        start_list[i], end_list[i], alpha=0.3, color='green', ls="--")
    cpu_ax.axvspan(
        start_list[i], end_list[i], alpha=0.3, color='green', ls="--")
    
throughput_ax.axvspan(0, 0, alpha=0.3, color='green',
                      label="kStopped_kL0FileCountLimit")
pidstat_io_write_ax.axvspan(0, 0, alpha=0.3, color='green',
                      label="kStopped_kL0FileCountLimit")
cpu_ax.axvspan(0, 0, alpha=0.3, color='green',
               label="kStopped_kL0FileCountLimit")

kStopped_kMemtableLimit = stall_data[(
    stall_data["type"] == "kStopped") & (stall_data["cause"] == "kMemtableLimit")]
start_list = kStopped_kMemtableLimit["start"].tolist()
end_list = kStopped_kMemtableLimit["end"].tolist()
for i in range(len(start_list)):
    throughput_ax.axvspan(
        start_list[i], end_list[i], alpha=0.3, color='mediumturquoise')
    stall_memtable_num.append((start_list[i], 2))
    stall_memtable_num.append((end_list[i], 2))
    pidstat_io_write_ax.axvspan(
        start_list[i], end_list[i], alpha=0.3, color='mediumturquoise')
    cpu_ax.axvspan(
        start_list[i], end_list[i], alpha=0.3, color='mediumturquoise')
throughput_ax.axvspan(0, 0, alpha=0.3, color='mediumturquoise',
                      label="kStopped_kMemtableLimit")
pidstat_io_write_ax.axvspan(0, 0, alpha=0.3, color='mediumturquoise',
                      label="kStopped_kMemtableLimit")
cpu_ax.axvspan(0, 0, alpha=0.3, color='mediumturquoise',
               label="kStopped_kMemtableLimit")

kStopped_kPendingCompactionBytes = stall_data[(
    stall_data["type"] == "kStopped") & (stall_data["cause"] == "kPendingCompactionBytes")]
start_list = kStopped_kPendingCompactionBytes["start"].tolist()
end_list = kStopped_kPendingCompactionBytes["end"].tolist()
for i in range(len(start_list)):
    throughput_ax.axvspan(start_list[i], end_list[i], alpha=0.3, color='cyan')
    pidstat_io_write_ax.axvspan(start_list[i], end_list[i], alpha=0.3, color='cyan')
    cpu_ax.axvspan(start_list[i], end_list[i], alpha=0.3, color='cyan')
throughput_ax.axvspan(0, 0, alpha=0.3, color='cyan',
                      label="kStopped_kPendingCompactionBytes")
pidstat_io_write_ax.axvspan(0, 0, alpha=0.3, color='cyan',
                      label="kStopped_kPendingCompactionBytes")
cpu_ax.axvspan(0, 0, alpha=0.3, color='cyan',
               label="kStopped_kPendingCompactionBytes")


IncreasingCompactionThreads_kL0FileCountLimit = stall_data[(
    stall_data["type"] == "IncreasingCompactionThreads") & (stall_data["cause"] == "kL0FileCountLimit")]
start_list = IncreasingCompactionThreads_kL0FileCountLimit["start"].tolist()
end_list = IncreasingCompactionThreads_kL0FileCountLimit["end"].tolist()
for i in range(len(start_list)):
    low_cpu_ax.axvspan(start_list[i], end_list[i], alpha=0.3, color='yellow')
    pidstat_low_io_write_ax.axvspan(
        start_list[i], end_list[i], alpha=0.3, color='yellow')
low_cpu_ax.axvspan(0, 0, alpha=0.3, color='yellow',
                   label="IncreasingCompactionThreads_kL0FileCountLimit")
pidstat_low_io_write_ax.axvspan(0, 0, alpha=0.3, color='yellow',
                          label="IncreasingCompactionThreads_kL0FileCountLimit")

IncreasingCompactionThreads_kPendingCompactionBytes = stall_data[(
    stall_data["type"] == "IncreasingCompactionThreads") & (stall_data["cause"] == "kPendingCompactionBytes")]
start_list = IncreasingCompactionThreads_kPendingCompactionBytes["start"].tolist(
)
end_list = IncreasingCompactionThreads_kPendingCompactionBytes["end"].tolist()
for i in range(len(start_list)):
    low_cpu_ax.axvspan(start_list[i], end_list[i], alpha=0.3, color='cyan')
    pidstat_low_io_write_ax.axvspan(
        start_list[i], end_list[i], alpha=0.3, color='cyan')
low_cpu_ax.axvspan(0, 0, alpha=0.3, color='cyan',
                   label="IncreasingCompactionThreads_kPendingCompactionBytes")
pidstat_low_io_write_ax.axvspan(0, 0, alpha=0.3, color='cyan',
                          label="IncreasingCompactionThreads_kPendingCompactionBytes")

#! throughput
files = glob.glob('./data/'+NAME+'/exp_throughput_*')
max_time = 0
first = True
# print(files)
for file in files:
    throughput_data = pd.read_csv(file, encoding='utf-8',
                                  names=["now", "bw", "iops", "size", "average bw", "average iops"], header=0)
    max_time = max(max_time, throughput_data["now"].iloc[-1])
    throughput_ax.plot(throughput_data["now"],
                       throughput_data["bw"], label=file.split('/')[-1], alpha=0.7)
    throughput_ax.plot(throughput_data["now"], throughput_data["average bw"],
                       "-.", label=file.split('/')[-1]+" average", alpha=0.7)
    if first:
        throughput_ax.text(throughput_data["now"].iloc[-1], throughput_data["average bw"].iloc[-1]+0.1,
                           '%.0f' % throughput_data["average bw"].iloc[-1], ha='center', va='bottom', fontsize='small', rotation=0)
        first = False

x_major_locator = MultipleLocator(100)
throughput_ax.set_xlim(xmin=0, xmax=max_time)
throughput_ax.xaxis.set_major_locator(x_major_locator)
throughput_ax.set_xlabel("Time(s)")
throughput_ax.set_ylabel("Write throughput(MB/s)")
throughput_ax.grid()
throughput_ax.set_title("foreground write throughput, stall and delay situation", fontsize="large",
                        loc='left', fontstyle='oblique')


#! stall condition
stall_condition_data = pd.read_csv('./data/'+NAME+'/exp_stall_condition.csv', encoding='utf-8',
                                   names=["time", "num_unflushed_memtables", "num_l0_files", "num_compaction_needed_bytes"], header=0)
stall_condition_data.loc[:,
                         'num_compaction_needed_bytes'] = stall_condition_data.loc[:, 'num_compaction_needed_bytes']/1024/1024

sorted_lists = sorted(list(zip(stall_condition_data["time"],
                               stall_condition_data["num_unflushed_memtables"]))+stall_memtable_num)
sorted_time = [t[0] for t in sorted_lists]
sorted_num_unflushed_memtables = [t[1] for t in sorted_lists]

memtable_ax.step(sorted_time,
                 sorted_num_unflushed_memtables, label="num_unflushed_memtables", alpha=0.7, where='post')
memtable_ax.axhline(y=2, label="MMO_stop", linestyle=':')
memtable_ax.axhline(y=1, label="MMO_delay", linestyle=':')
memtable_ax.set_xlabel("Time(s)")
memtable_ax.set_ylabel("Number")
memtable_ax.grid()
memtable_ax.set_title("the number of unflushed memtables", fontsize="large",
                      loc='left', fontstyle='oblique')


sorted_lists = sorted(list(zip(stall_condition_data["time"],
                               stall_condition_data["num_l0_files"]))+stall_l0_num)
sorted_time = [t[0] for t in sorted_lists]
sorted_num_l0_files = [t[1] for t in sorted_lists]

l0_ax.step(sorted_time,
           sorted_num_l0_files, label="num_l0_files", alpha=0.7, where='post')
l0_ax.axhline(y=36, label="L0O_stop", linestyle=':')
l0_ax.axhline(y=20, label="L0O_delay", linestyle=':')
l0_ax.axhline(y=4, label="L0O_score", linestyle=':')
l0_ax.set_xlabel("Time(s)")
l0_ax.set_ylabel("Number")
l0_ax.grid()
l0_ax.set_title("the number of l0 files", fontsize="large",
                loc='left', fontstyle='oblique')


compaction_needed_bytes_ax.plot(stall_condition_data["time"],
                                stall_condition_data["num_compaction_needed_bytes"], label="num_compaction_needed_bytes", alpha=0.7)
compaction_needed_bytes_ax.axhline(
    y=256 * 1024, label="RDO_stop", linestyle=':')
compaction_needed_bytes_ax.axhline(
    y=64 * 1024, label="RDO_delay", linestyle=':')
compaction_needed_bytes_ax.set_xlabel("Time(s)")
compaction_needed_bytes_ax.set_ylabel("Size(MB)")
compaction_needed_bytes_ax.grid()
compaction_needed_bytes_ax.set_title("the size of compaction needed bytes", fontsize="large",
                                     loc='left', fontstyle='oblique')

#! Compaction
compaction_data = pd.read_csv('./data/'+NAME+'/exp_compaction.csv', encoding='utf-8',
                              names=["start_level", "output_level", "start", "end"], header=0)
score_ax.axvspan(0, 0, alpha=0.3, color='blue', label="L0_L0_compaction")
score_ax.axvspan(0, 0, alpha=0.3, color='red', label="L0_L1_compaction")
compaction_throughput_ax.axvspan(
    0, 0, alpha=0.3, color='red', label="L0_L1_compaction")
pidstat_io_write_ax.axvspan(0, 0, alpha=0.3, color='red', label="L0_L1_compaction")
cpu_ax.axvspan(0, 0, alpha=0.3, color='red', label="L0_L1_compaction")
throughput_ax.axvspan(0, 0, alpha=0.3, color='red', label="L0_L1_compaction")
l0_ax.axvspan(0, 0, alpha=0.3, color='red', label="L0_L1_compaction")
score_ax.axvspan(0, 0, alpha=0.3, color='green',
                 label="deeper_level_compaction")
for index, row in compaction_data.iterrows():
    if row['start_level'] == 0 and row['output_level'] == 0:
        score_ax.axvspan(xmin=row['start'], xmax=row['end'],
                         ymin=0, ymax=0.1, alpha=0.3, color='blue')
    elif row['start_level'] == 0 and row['output_level'] == 1:
        score_ax.axvspan(xmin=row['start'], xmax=row['end'],
                         ymin=0.1, ymax=0.2, alpha=0.3, color='red')
        compaction_throughput_ax.axvspan(xmin=row['start'], xmax=row['end'],
                                         ymin=0.1, ymax=0.2, alpha=0.3, color='red')
        pidstat_io_write_ax.axvspan(xmin=row['start'], xmax=row['end'],
                              ymin=0.9, ymax=1.0, alpha=0.3, color='red')
        cpu_ax.axvspan(xmin=row['start'], xmax=row['end'],
                       ymin=0.9, ymax=1.0, alpha=0.3, color='red')
        throughput_ax.axvspan(xmin=row['start'], xmax=row['end'],
                              ymin=0.9, ymax=1.0, alpha=0.3, color='red')
        l0_ax.axvspan(xmin=row['start'], xmax=row['end'],
                      ymin=0 , ymax=1.0, alpha=0.3, color='red')
    elif row['start_level'] == 1 and row['output_level'] == 2:
        score_ax.axvspan(xmin=row['start'], xmax=row['end'],
                         ymin=0.2, ymax=0.3, alpha=0.3, color='green')
    elif row['start_level'] == 2 and row['output_level'] == 3:
        score_ax.axvspan(xmin=row['start'], xmax=row['end'],
                         ymin=0.3, ymax=0.4, alpha=0.3, color='green')
    elif row['start_level'] == 3 and row['output_level'] == 4:
        score_ax.axvspan(xmin=row['start'], xmax=row['end'],
                         ymin=0.4, ymax=0.5, alpha=0.3, color='green')
    elif row['start_level'] == 4 and row['output_level'] == 5:
        score_ax.axvspan(xmin=row['start'], xmax=row['end'],
                         ymin=0.5, ymax=0.6, alpha=0.3, color='green')
    elif row['start_level'] == 5 and row['output_level'] == 6:
        score_ax.axvspan(xmin=row['start'], xmax=row['end'],
                         ymin=0.6, ymax=0.7, alpha=0.3, color='green')
    else:
        score_ax.axvspan(xmin=row['start'], xmax=row['end'],
                         ymin=0.7, ymax=0.8, alpha=0.3, color='green')

#! Compaction_score
# score_data_1 = pd.read_csv('./data/'+NAME+'/exp_compaction_score.csv', encoding='utf-8',
#                            names=["time", "level", "score"], header=0)

score_data = pd.read_csv('./data/'+NAME+'/exp_compaction_score', encoding='utf-8',
                         delim_whitespace=True, names=["level", "score"], header=0)
# print(score_data_2['level'])

# l0_score_data_1 = score_data_1[(score_data_1["level"] == 0)]
# l0_score_raw_data_2 = score_data_2[(
#     score_data_2["level"] == "L0")]["score"].tolist()
# l0_padding_zero = len(stall_condition_data["time"]) - len(l0_score_raw_data_2)
# l0_score_data_2 = [0] * l0_padding_zero + l0_score_raw_data_2

# l0_total_time = l0_score_data_1["time"].tolist(
# )+stall_condition_data["time"].tolist()
# l0_score_data_total = l0_score_data_1["score"].tolist()+l0_score_data_2

# score_ax.scatter(l0_total_time, l0_score_data_total,
#                  label="l0_score", alpha=0.7)

for i in [0]:
    # level_score_data_1 = score_data_1[(score_data_1["level"] == 0)]
    level_score_raw_data = score_data[(
        score_data["level"] == "L"+str(i))]["score"].tolist()
    level_padding_zero = len(
        stall_condition_data["time"]) - len(level_score_raw_data)
    level_score_data = [0] * level_padding_zero + level_score_raw_data

    # level_total_time =stall_condition_data["time"].tolist()
    # level_score_data_total = level_score_data_2

    # sorted_lists = sorted(zip(level_total_time, level_score_data_total))
    # sorted_time = [t[0] for t in sorted_lists]
    # sorted_score = [t[1] for t in sorted_lists]

    score_ax.step(stall_condition_data["time"], level_score_data,
                  label="l"+str(i)+"_score", alpha=0.5, where='post')

score_ax.axhline(y=1, label="compaction_score", linestyle=':')
score_ax.set_xlabel("Time(s)")
score_ax.set_ylabel("Score")
score_ax.grid()
score_ax.set_title("the score of LSM-tree level", fontsize="large",
                   loc='left', fontstyle='oblique')

#! top
top_time_data = pd.read_csv('./data/'+NAME+'/exp_top_time.txt', encoding='utf-8',
                            delim_whitespace=True, names=["TIME"])
time_list = top_time_data["TIME"].tolist()
relative_time_list = []
# time_start = time.strptime(time_list[0],"%H:%M:%S")
for i in range(0, len(time_list)):
    time_now = time.strptime(time_list[i], "%H:%M:%S")
    relative_time = int(time.mktime(time_now))-int(time.mktime(db_start_time))
    if relative_time<0:
        relative_time+=86400
    relative_time_list.append(relative_time)

# print(relative_time_list)

top_data = pd.read_csv('./data/'+NAME+'/exp_top.txt', encoding='utf-8',
                       delim_whitespace=True, names=["PID", "USER", "PR", "NI", "VIRT", "RES", "SHR", "S", "CPU", "MEM", "TIME", "COMMAND"])
high_cpu_lists = []
low_cpu_lists = []
top_min_len = len(relative_time_list)
top_data_grouped = top_data.groupby(["PID"])


def process_top_data_group(group):
    cpu_list = group["CPU"].tolist()
    cpu_list_len = len(cpu_list)
    global top_min_len
    top_min_len = min(top_min_len, cpu_list_len)
    thread_name = group["COMMAND"].tolist()[0]
    if "bench" in thread_name:
        cpu_ax.plot(relative_time_list[:cpu_list_len], cpu_list,
                    label=thread_name+"_"+str(group.name), alpha=0.7)
    elif "high" in thread_name:
        high_cpu_ax.plot(relative_time_list[:cpu_list_len], cpu_list,
                         label=thread_name+"_"+str(group.name), alpha=0.7)
        high_cpu_lists.append(cpu_list)
    elif "low" in thread_name:
        low_cpu_ax.plot(relative_time_list[:cpu_list_len], cpu_list,
                        label=thread_name+"_"+str(group.name), alpha=0.7)
        low_cpu_lists.append(cpu_list)


top_data_grouped.apply(process_top_data_group)

high_cpu_list = []
low_cpu_list = []
for i in range(top_min_len):
    total = 0
    for list in high_cpu_lists:
        total += list[i]
    if len(high_cpu_lists) != 0:
        high_cpu_list.append(total/len(high_cpu_lists))
    else:
        high_cpu_list.append(0)
for i in range(top_min_len):
    total = 0
    for list in low_cpu_lists:
        total += list[i]
    if len(low_cpu_lists) != 0:
        low_cpu_list.append(total/len(low_cpu_lists))
    else:
        low_cpu_list.append(0)
cpu_ax.plot(relative_time_list[:top_min_len], high_cpu_list,
            label="high_thread_pool_avg", alpha=0.7)
cpu_ax.plot(relative_time_list[:top_min_len], low_cpu_list,
            label="low_thread_pool_avg", alpha=0.7)

avg_high_cpu_list = []
avg_low_cpu_list = []
for i in range(0, top_min_len):
    avg_high_cpu_list.append(np.mean(high_cpu_list[:i+1]))
for i in range(0, top_min_len):
    avg_low_cpu_list.append(np.mean(low_cpu_list[:i+1]))
cpu_ax.plot(relative_time_list[:top_min_len], avg_high_cpu_list, "-.",
            label="high_thread_pool_avg_avg", alpha=0.7)
cpu_ax.text(relative_time_list[top_min_len-1], avg_high_cpu_list[-1]+0.1,
            '%.0f' % avg_high_cpu_list[-1], ha='center', va='bottom', fontsize='small', rotation=0)
cpu_ax.plot(relative_time_list[:top_min_len], avg_low_cpu_list, "-.",
            label="low_thread_pool_avg_avg", alpha=0.7)
cpu_ax.text(relative_time_list[top_min_len-1], avg_low_cpu_list[-1]+0.1,
            '%.0f' % avg_low_cpu_list[-1], ha='center', va='bottom', fontsize='small', rotation=0)

cpu_ax.set_xlabel("Time(s)")
cpu_ax.set_ylabel("CPU Utilization(%)")
cpu_ax.grid()
cpu_ax.set_title("foreground db_bench CPU utilization, background high and low thread pool average CPU utilization", fontsize="large",
                 loc='left', fontstyle='oblique')

high_cpu_ax.set_xlabel("Time(s)")
high_cpu_ax.set_ylabel("CPU Utilization(%)")
high_cpu_ax.grid()
high_cpu_ax.set_title("background high thread pool CPU utilization", fontsize="large",
                      loc='left', fontstyle='oblique')

low_cpu_ax.set_xlabel("Time(s)")
low_cpu_ax.set_ylabel("CPU Utilization(%)")
low_cpu_ax.grid()
low_cpu_ax.set_title("background low thread pool CPU utilization", fontsize="large",
                     loc='left', fontstyle='oblique')


#! io_stat
io_time_data = pd.read_csv('./data/'+NAME+'/exp_iostat_time.txt', encoding='utf-8',
                           delim_whitespace=True, names=["TIME"])
time_list = io_time_data["TIME"].tolist()
relative_time_list = []
# time_start = time.strptime(time_list[0], "%H:%M:%S")
for i in range(0, len(time_list)):
    time_now = time.strptime(time_list[i], "%H:%M:%S")
    relative_time = int(time.mktime(time_now))-int(time.mktime(db_start_time))
    if relative_time < 0:
        relative_time += 86400
    relative_time_list.append(relative_time)

io_data = pd.read_csv('./data/'+NAME+'/exp_iostat.txt', encoding='utf-8',
                      delim_whitespace=True, names=["Device", "r/s", "rMB/s", "rrqm/s", "%rrqm", "r_await", "rareq-sz", "w/s", "wMB/s", "wrqm/s", "%wrqm", "w_await", "wareq-sz", "d/s", "dMB/s", "drqm/s", "%drqm", "d_await", "dareq-sz", "f/s", "f_await", "aqu-sz", "%util"])

io_data.loc[:, 'wareq-sz'] = io_data.loc[:, 'wareq-sz']*512/1024
io_data_grouped = io_data.groupby(["Device"])


def process_io_data_group(group):
    # write_bandwith = group["wMB/s"].tolist()
    # read_bandwith = group["rMB/s"].tolist()
    io_bw_ax.plot(relative_time_list, group["wMB/s"],
                  label="write_"+group["Device"].tolist()[0], alpha=0.7)
    io_bw_ax.text(relative_time_list[-1], group["wMB/s"].mean()+10,
                  '%.2f' % group["wMB/s"].mean(), ha='center', va='bottom', fontsize='small', rotation=0)
    io_bw_ax.plot(relative_time_list, group["rMB/s"],
                  label="read_"+group["Device"].tolist()[0], alpha=0.7)
    io_bw_ax.text(relative_time_list[-1], group["rMB/s"].mean()-10,
                  '%.2f' % group["rMB/s"].mean(), ha='center', va='bottom', fontsize='small', rotation=0)
    sum_bw = group["wMB/s"]+group["rMB/s"]
    io_bw_ax.plot(relative_time_list, sum_bw,
                  label=group["Device"].tolist()[0]+"_total_bandwith", alpha=0.7)
    io_bw_ax.text(relative_time_list[-1]-40, sum_bw.mean()-1,
                  '%.2f' % sum_bw.mean(), ha='center', va='bottom', fontsize='small', rotation=0)
    # avg_write_bandwith = []
    # for i in range(0, len(write_bandwith)):
    #     avg_write_bandwith.append(np.mean(write_bandwith[:i+1]))
    # io_bw_ax.plot(relative_time_list, avg_write_bandwith, "-.",
    #               label=group["Device"].tolist()[0]+"_avg", alpha=0.7)
    # io_bw_ax.text(relative_time_list[-1], avg_write_bandwith[-1]+0.1,
    #               '%.2f' % avg_write_bandwith[-1], ha='center', va='bottom', fontsize='small', rotation=0)
    io_req_size_ax.plot(relative_time_list, group["wareq-sz"],
                        label="write_"+group["Device"].tolist()[0], alpha=0.7)
    io_req_size_ax.text(relative_time_list[-1], group["wareq-sz"].mean()+20,
                        '%.2f' % group["wareq-sz"].mean(), ha='center', va='bottom', fontsize='small', rotation=0)
    
    io_req_size_ax.plot(relative_time_list, group["rareq-sz"],
                        label="read_"+group["Device"].tolist()[0], alpha=0.7)
    io_req_size_ax.text(relative_time_list[-1], group["rareq-sz"].mean()-20,
                        '%.2f' % group["rareq-sz"].mean(), ha='center', va='bottom', fontsize='small', rotation=0)
    
    io_que_size_ax.plot(relative_time_list, group["aqu-sz"],
                        label=group["Device"].tolist()[0], alpha=0.7)
    io_que_size_ax.text(relative_time_list[-1]-1, group["aqu-sz"].mean()+0.1,
                        '%.2f' % group["aqu-sz"].mean(), ha='center', va='bottom', fontsize='small', rotation=0)
    # aqu_sz = group["aqu-sz"].mean()
    # print(group["Device"].tolist()[0])
    # print(aqu_sz)


io_data_grouped.apply(process_io_data_group)

io_bw_ax.set_xlabel("Time(s)")
io_bw_ax.set_ylabel("IO Bandwith(MB/s)")
io_bw_ax.grid()
io_bw_ax.set_title("device IO bandwith", fontsize="large",
                   loc='left', fontstyle='oblique')

io_req_size_ax.set_xlabel("Time(s)")
io_req_size_ax.set_ylabel("Write Avg Req Size(MB)")
io_req_size_ax.grid()
io_req_size_ax.set_title("write average request size", fontsize="large",
                         loc='left', fontstyle='oblique')

io_que_size_ax.set_xlabel("Time(s)")
io_que_size_ax.set_ylabel("Number")
io_que_size_ax.grid()
io_que_size_ax.set_title("averge queue size", fontsize="large",
                   loc='left', fontstyle='oblique')

#! pidstat
pidstat_data = pd.read_csv('./data/'+NAME+'/exp_pidstat.txt', encoding='utf-8',
                           delim_whitespace=True, names=["TIME", "UID", "TGID", "TID", "kB_rd/s", "kB_wr/s", "kB_ccwr/s", "iodelay", "COMMAND"])
pidstat_data.loc[:, 'kB_wr/s'] = pidstat_data.loc[:, 'kB_wr/s']/1024.0
pidstat_data.loc[:, 'kB_rd/s'] = pidstat_data.loc[:, 'kB_rd/s']/1024.0

# counter = Counter(pidstat_data['TIME'].tolist())
# for element, count in counter.items():
#     # print(count)
#     if count!=5:
#         print(f"{element}重复了{count}次")

time_list = pidstat_data['TIME'].drop_duplicates().tolist()
relative_time_list = []
for i in range(0, len(time_list)):
    time_now = time.strptime(time_list[i], "%H:%M:%S")
    relative_time = int(time.mktime(time_now)) - \
        int(time.mktime(db_start_time))
    if relative_time < 0:
        relative_time += 86400
    relative_time_list.append(relative_time)
pidstat_min_len = len(relative_time_list)
high_io_write_lists = []
low_io_write_lists = []
high_io_read_lists = []
low_io_read_lists = []

pidstat_data_grouped = pidstat_data.groupby(["TID"])


def process_pidstat_data_group(group):
    wr_len = len(group["kB_wr/s"])
    global pidstat_min_len
    pidstat_min_len = min(pidstat_min_len, wr_len)
    thread_name = group["COMMAND"].tolist()[0][3:]
    if "bench" in thread_name:
        pidstat_io_write_ax.plot(relative_time_list[:wr_len], group["kB_wr/s"], label=thread_name +
                           "_"+str(group.name), alpha=0.7)
        pidstat_io_read_ax.plot(relative_time_list[:wr_len], group["kB_rd/s"], label=thread_name +
                                 "_"+str(group.name), alpha=0.7)
        # bench_lists.append(wr)
    elif "high" in thread_name:
        pidstat_high_io_write_ax.plot(relative_time_list[:wr_len], group["kB_wr/s"], label=thread_name +
                                "_"+str(group.name), alpha=0.7)
        high_io_write_lists.append(group["kB_wr/s"].tolist())
        pidstat_high_io_read_ax.plot(relative_time_list[:wr_len], group["kB_rd/s"], label=thread_name +
                                      "_"+str(group.name), alpha=0.7)
        high_io_read_lists.append(group["kB_rd/s"].tolist())
    elif "low" in thread_name:
        pidstat_low_io_write_ax.plot(relative_time_list[:wr_len], group["kB_wr/s"], label=thread_name +
                               "_"+str(group.name), alpha=0.7)
        low_io_write_lists.append(group["kB_wr/s"].tolist())
        pidstat_low_io_read_ax.plot(relative_time_list[:wr_len], group["kB_rd/s"], label=thread_name +
                                     "_"+str(group.name), alpha=0.7)
        low_io_read_lists.append(group["kB_rd/s"].tolist())


pidstat_data_grouped.apply(process_pidstat_data_group)

high_io_write_list = []
low_io_write_list = []
for i in range(pidstat_min_len):
    total = 0
    for list in high_io_write_lists:
        total += list[i]
    high_io_write_list.append(total)
for i in range(pidstat_min_len):
    total = 0
    for list in low_io_write_lists:
        total += list[i]
    low_io_write_list.append(total)
pidstat_io_write_ax.plot(relative_time_list[:pidstat_min_len],
                   high_io_write_list, label="high_thread_pool_total", alpha=0.7)
pidstat_io_write_ax.plot(relative_time_list[:pidstat_min_len],
                   low_io_write_list, label="low_thread_pool_total", alpha=0.7)


high_io_read_list = []
low_io_read_list = []
for i in range(pidstat_min_len):
    total = 0
    for list in high_io_read_lists:
        total += list[i]
    high_io_read_list.append(total)
for i in range(pidstat_min_len):
    total = 0
    for list in low_io_read_lists:
        total += list[i]
    low_io_read_list.append(total)
pidstat_io_read_ax.plot(relative_time_list[:pidstat_min_len],
                         high_io_read_list, label="high_thread_pool_total", alpha=0.7)
pidstat_io_read_ax.plot(relative_time_list[:pidstat_min_len],
                         low_io_read_list, label="low_thread_pool_total", alpha=0.7)


avg_high_io_write_list = []
avg_low_io_write_list = []
for i in range(0, pidstat_min_len):
    avg_high_io_write_list.append(np.mean(high_io_write_list[:i+1]))
for i in range(0, pidstat_min_len):
    avg_low_io_write_list.append(np.mean(low_io_write_list[:i+1]))
pidstat_io_write_ax.plot(relative_time_list[:pidstat_min_len], avg_high_io_write_list, "-.",
                   label="high_thread_pool_total_avg", alpha=0.7)
pidstat_io_write_ax.text(relative_time_list[pidstat_min_len-1], avg_high_io_write_list[-1]+0.1,
                   '%.0f' % avg_high_io_write_list[-1], ha='center', va='bottom', fontsize='small', rotation=0)
pidstat_io_write_ax.plot(relative_time_list[:pidstat_min_len], avg_low_io_write_list, "-.",
                   label="low_thread_pool_total_avg", alpha=0.7)
pidstat_io_write_ax.text(relative_time_list[pidstat_min_len-1], avg_low_io_write_list[-1]+0.1,
                   '%.0f' % avg_low_io_write_list[-1], ha='center', va='bottom', fontsize='small', rotation=0)

avg_high_io_read_list = []
avg_low_io_read_list = []
for i in range(0, pidstat_min_len):
    avg_high_io_read_list.append(np.mean(high_io_read_list[:i+1]))
for i in range(0, pidstat_min_len):
    avg_low_io_read_list.append(np.mean(low_io_read_list[:i+1]))
pidstat_io_read_ax.plot(relative_time_list[:pidstat_min_len], avg_high_io_read_list, "-.",
                         label="high_thread_pool_total_avg", alpha=0.7)
pidstat_io_read_ax.text(relative_time_list[pidstat_min_len-1], avg_high_io_read_list[-1]+0.1,
                         '%.0f' % avg_high_io_read_list[-1], ha='center', va='bottom', fontsize='small', rotation=0)
pidstat_io_read_ax.plot(relative_time_list[:pidstat_min_len], avg_low_io_read_list, "-.",
                         label="low_thread_pool_total_avg", alpha=0.7)
pidstat_io_read_ax.text(relative_time_list[pidstat_min_len-1], avg_low_io_read_list[-1]+0.1,
                         '%.0f' % avg_low_io_read_list[-1], ha='center', va='bottom', fontsize='small', rotation=0)

# pidstat_data_grouped_time = pidstat_data.groupby(
#     ["TIME"]).agg({'kB_wr/s': 'sum'})
# io_bw_ax.plot(relative_time_list, pidstat_data_grouped_time["kB_wr/s"].tolist(),
#               label="sum", alpha=0.5)

pidstat_io_write_ax.set_xlabel("Time(s)")
pidstat_io_write_ax.set_ylabel("IO Bandwith(MB/s)")
pidstat_io_write_ax.grid()
pidstat_io_write_ax.set_title("foreground db_bench IO bandwith, background high and low thread pool total IO write bandwith", fontsize="large",
                        loc='left', fontstyle='oblique')

pidstat_high_io_write_ax.set_xlabel("Time(s)")
pidstat_high_io_write_ax.set_ylabel("IO Bandwith(MB/s)")
pidstat_high_io_write_ax.grid()
pidstat_high_io_write_ax.set_title("background high thread pool IO write bandwith", fontsize="large",
                             loc='left', fontstyle='oblique')

pidstat_low_io_write_ax.set_xlabel("Time(s)")
pidstat_low_io_write_ax.set_ylabel("IO Bandwith(MB/s)")
pidstat_low_io_write_ax.grid()
pidstat_low_io_write_ax.set_title("background low thread pool IO write bandwith", fontsize="large",
                            loc='left', fontstyle='oblique')

pidstat_io_read_ax.set_xlabel("Time(s)")
pidstat_io_read_ax.set_ylabel("IO Bandwith(MB/s)")
pidstat_io_read_ax.grid()
pidstat_io_read_ax.set_title("foreground db_bench IO bandwith, background high and low thread pool total IO read bandwith", fontsize="large",
                              loc='left', fontstyle='oblique')

pidstat_high_io_read_ax.set_xlabel("Time(s)")
pidstat_high_io_read_ax.set_ylabel("IO Bandwith(MB/s)")
pidstat_high_io_read_ax.grid()
pidstat_high_io_read_ax.set_title("background high thread pool IO read bandwith", fontsize="large",
                                   loc='left', fontstyle='oblique')

pidstat_low_io_read_ax.set_xlabel("Time(s)")
pidstat_low_io_read_ax.set_ylabel("IO Bandwith(MB/s)")
pidstat_low_io_read_ax.grid()
pidstat_low_io_read_ax.set_title("background low thread pool IO read bandwith", fontsize="large",
                                  loc='left', fontstyle='oblique')


#! background_schedule
schedule_data = pd.read_csv('./data/'+NAME+'/exp_background_schedule.csv', encoding='utf-8',
                            names=["time", "type", "num"], header=0)

unscheduled_compactions = schedule_data[(
    schedule_data["type"] == "unscheduled_compactions")]
bg_compaction_scheduled = schedule_data[(
    schedule_data["type"] == "bg_compaction_scheduled")]

schedule_ax.step(
    bg_compaction_scheduled["time"], bg_compaction_scheduled["num"], '-', label="compaction scheduled", alpha=0.5, color="green", where='post')
# schedule_ax.step(
#     unscheduled_compactions["time"], unscheduled_compactions["num"], ':', label="unscheduled compactions", alpha=0.5, color="red", where='post')

schedule_ax.set_xlabel("Time(s)")
schedule_ax.set_ylabel("Number")
schedule_ax.grid()
schedule_ax.set_title("background schedule condition", fontsize="large",
                      loc='left', fontstyle='oblique')

#! exp_compaction_noting_to_do
ompaction_noting_to_do_data = pd.read_csv('./data/'+NAME+'/exp_compaction_noting_to_do.csv', encoding='utf-8',
                                          names=["time"], header=0)
for index, row in ompaction_noting_to_do_data.iterrows():
    schedule_ax.axvline(x=row['time'], ymin=0.4,
                        ymax=0.6, color='blue', alpha=0.7)

# #! exp_switch_memtable
# switch_memtable_data = pd.read_csv('./data/'+NAME+'/exp_switch_memtable.csv', encoding='utf-8',
#                                    names=["time"], header=0)
# for index, row in switch_memtable_data.iterrows():
#     throughput_ax.axvline(x=row['time'], ymin=0,
#                           ymax=1, color='blue', alpha=0.3)

throughput_ax.legend(loc='lower left', ncols=4)
cpu_ax.legend(loc='upper left', ncols=4)
high_cpu_ax.legend(loc='upper left', ncols=4)
low_cpu_ax.legend(loc='upper left', ncols=4)
io_bw_ax.legend(loc='lower left', ncols=5)
io_req_size_ax.legend(loc='upper left', ncols=4)
pidstat_io_write_ax.legend(loc='upper left', ncols=4)
pidstat_high_io_write_ax.legend(loc='upper left', ncols=4)
pidstat_low_io_write_ax.legend(loc='upper left', ncols=4)
pidstat_io_read_ax.legend(loc='upper left', ncols=4)
pidstat_high_io_read_ax.legend(loc='upper left', ncols=4)
pidstat_low_io_read_ax.legend(loc='upper left', ncols=4)
memtable_ax.legend(loc='upper left', ncols=4)
l0_ax.legend(loc='upper left', ncols=4)
compaction_needed_bytes_ax.legend(loc='upper left', ncols=4)
score_ax.legend(loc='upper left', ncols=4)
schedule_ax.legend(loc='upper left', ncols=4)
compaction_throughput_ax.legend(loc='upper left', ncols=4)
plt.savefig('./data/'+NAME+'/'+NAME+'.jpg')
# plt.show()
