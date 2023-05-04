import datetime
import time
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.pyplot import MultipleLocator
from data_process import *
from collections import Counter

NAME = "rocksdb_result_20000000_64M_2_100B_1fg_2bg_0mutidb_perf_1682503723"

fig, (throughput_ax) = plt.subplots(1, 1, figsize=(
    20, 5), layout='constrained', sharex=True)
fig.suptitle(NAME, fontsize="xx-large", fontweight="medium")

# start_time
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


# stall
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
    stall_l0_num.append((start_list[i], 20))
throughput_ax.axvspan(0, 0, alpha=0.3, color='yellow',
                      label="kDelayed_kL0FileCountLimit")

kDelayed_kMemtableLimit = stall_data[(
    stall_data["type"] == "kDelayed") & (stall_data["cause"] == "kMemtableLimit")]
start_list = kDelayed_kMemtableLimit["start"].tolist()
end_list = kDelayed_kMemtableLimit["end"].tolist()
for i in range(len(start_list)):
    throughput_ax.axvspan(start_list[i], end_list[i], alpha=0.3, color='gold')
    stall_memtable_num.append((start_list[i], 1))
throughput_ax.axvspan(0, 0, alpha=0.3, color='gold',
                      label="kDelayed_kMemtableLimit")

kDelayed_kPendingCompactionBytes = stall_data[(
    stall_data["type"] == "kDelayed") & (stall_data["cause"] == "kPendingCompactionBytes")]
start_list = kDelayed_kPendingCompactionBytes["start"].tolist()
end_list = kDelayed_kPendingCompactionBytes["end"].tolist()
for i in range(len(start_list)):
    throughput_ax.axvspan(start_list[i], end_list[i], alpha=0.3, color='olive')
throughput_ax.axvspan(0, 0, alpha=0.3, color='olive',
                      label="kDelayed_kPendingCompactionBytes")

kStopped_kL0FileCountLimit = stall_data[(
    stall_data["type"] == "kStopped") & (stall_data["cause"] == "kL0FileCountLimit")]
start_list = kStopped_kL0FileCountLimit["start"].tolist()
end_list = kStopped_kL0FileCountLimit["end"].tolist()
for i in range(len(start_list)):
    throughput_ax.axvspan(
        start_list[i], end_list[i], alpha=0.3, color='green', ls="--")
    stall_l0_num.append((start_list[i], 36))
throughput_ax.axvspan(0, 0, alpha=0.3, color='green',
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
throughput_ax.axvspan(0, 0, alpha=0.3, color='mediumturquoise',
                      label="kStopped_kMemtableLimit")

kStopped_kPendingCompactionBytes = stall_data[(
    stall_data["type"] == "kStopped") & (stall_data["cause"] == "kPendingCompactionBytes")]
start_list = kStopped_kPendingCompactionBytes["start"].tolist()
end_list = kStopped_kPendingCompactionBytes["end"].tolist()
for i in range(len(start_list)):
    throughput_ax.axvspan(start_list[i], end_list[i], alpha=0.3, color='cyan')
throughput_ax.axvspan(0, 0, alpha=0.3, color='cyan',
                      label="kStopped_kPendingCompactionBytes")

# IncreasingCompactionThreads_kL0FileCountLimit = stall_data[(
#     stall_data["type"] == "IncreasingCompactionThreads") & (stall_data["cause"] == "kL0FileCountLimit")]
# start_list = IncreasingCompactionThreads_kL0FileCountLimit["start"].tolist()
# end_list = IncreasingCompactionThreads_kL0FileCountLimit["end"].tolist()
# for i in range(len(start_list)):
#     low_cpu_ax.axvspan(start_list[i], end_list[i], alpha=0.3, color='yellow')
# low_cpu_ax.axvspan(0, 0, alpha=0.3, color='yellow',
#                    label="IncreasingCompactionThreads_kL0FileCountLimit")

# IncreasingCompactionThreads_kPendingCompactionBytes = stall_data[(
#     stall_data["type"] == "IncreasingCompactionThreads") & (stall_data["cause"] == "kPendingCompactionBytes")]
# start_list = IncreasingCompactionThreads_kPendingCompactionBytes["start"].tolist(
# )
# end_list = IncreasingCompactionThreads_kPendingCompactionBytes["end"].tolist()
# for i in range(len(start_list)):
#     low_cpu_ax.axvspan(start_list[i], end_list[i], alpha=0.3, color='cyan')
# low_cpu_ax.axvspan(0, 0, alpha=0.3, color='cyan',
#                    label="IncreasingCompactionThreads_kPendingCompactionBytes")

# throughput
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
        throughput_ax.text(throughput_data["now"].iloc[-1], throughput_data["average bw"].iloc[-1]+1,
                           '%.0f' % throughput_data["average bw"].iloc[-1], ha='center', va='bottom', fontsize='small', rotation=0)
        first = False


# op_time, write_throughput, write_throughput = process_op_data(
#     './data/'+NAME+'/exp_op_data')
# print(write_throughput)
# throughput_ax.plot(op_time,
#          write_throughput, label="test",color="green", alpha=0.7)


x_major_locator = MultipleLocator(10)
throughput_ax.set_xlim(xmin=0, xmax=max_time)
throughput_ax.xaxis.set_major_locator(x_major_locator)
throughput_ax.set_xlabel("Time(s)")
throughput_ax.set_ylabel("Write throughput(MB/s)")
throughput_ax.grid()
throughput_ax.set_title("foreground write throughput, stall and delay situation", fontsize="large",
                        loc='left', fontstyle='oblique')



# exp_switch_memtable
switch_memtable_data = pd.read_csv('./data/'+NAME+'/exp_switch_memtable.csv', encoding='utf-8',
                                   names=["time"], header=0)
for index, row in switch_memtable_data.iterrows():
    throughput_ax.axvline(x=row['time'], ymin=0,
                          ymax=1, color='blue', alpha=0.3)

throughput_ax.legend(loc='lower left', ncols=4)
plt.savefig('./data/'+NAME+'/'+NAME+'.jpg')
# plt.show()

