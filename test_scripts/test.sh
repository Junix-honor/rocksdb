#!/bin/bash
set -x
export LC_ALL=C

# mkdir /sys/fs/cgroup/memory/kv64
# echo 64G > /sys/fs/cgroup/memory/kv64/memory.limit_in_bytes
# echo 0 > /sys/fs/cgroup/memory/kv64/memory.swappiness

sudo -S bash -c 'echo 800000 > /proc/sys/fs/file-max'
ulimit -n 800000

op_num=100000000
user_thread_num=1
backgroud_thread_num=2
num_multi_db=0
value_size=100
write_buffer_size=64
monitor_interval=1
db_dir="/mnt/shunzi/hjx"
wal_dir="/mnt/ssd/hjx"
db_disk="nvme1n1"
wal_disk="sdd"

# for user_thread_num in 1 2 4 8
# do

rm -rf ${db_dir}/*
rm  ${wal_dir}/*.log
sudo -S fstrim ${db_dir}
sudo -S fstrim ${wal_dir}
sudo -S bash -c 'echo 1 > /proc/sys/vm/drop_caches'

cgexec -g memory:kv64 ../release/db_bench \
--db=${db_dir}/rocksdb  --wal_dir=${wal_dir} \
--num=${op_num} --num_multi_db=${num_multi_db} \
--threads=${user_thread_num} --max_background_jobs=${backgroud_thread_num} \
--value_size=${value_size} --write_buffer_size=$((${write_buffer_size}<<20)) \
--benchmarks=fillrandom,stats  --histogram=true \
--compression_ratio=1 --compression_type=none > exp_result.log &

db_bench_pid=$!

top -H -b d ${monitor_interval} -p ${db_bench_pid} > exp_top_raw.txt &
# top -H -b d ${monitor_interval} | grep -e 'db_bench' -e 'kv_bench' -e 'rocksdb:' > exp_top.txt &
top_pid=$!
iostat -mtx ${monitor_interval} > exp_iostat_raw.txt &
# iostat -mtx ${monitor_interval} | grep -e ${db_disk} -e ${wal_disk} > exp_iostat.txt &
iostat_pid=$!

pidstat -p ${db_bench_pid} -d -t 1 > exp_pidstat_raw.txt&
# pidstat -p ${db_bench_pid} -dRsuvr -H -t 1 > exp_pidstat.txt&
pidstat_pid=$!

# fg $(jobs | grep "db_bench" | awk '{print $1}')
wait ${db_bench_pid}

sync
kill ${top_pid}
kill ${iostat_pid}
kill ${pidstat_pid}

grep -e 'db_bench' -e 'kv_bench' -e 'rocksdb:' exp_top_raw.txt > exp_top.txt
grep -E '^top' exp_top_raw.txt | awk '{print $3}' >exp_top_time.txt
grep -e ${db_disk} -e ${wal_disk} exp_iostat_raw.txt > exp_iostat.txt 
grep '^[0-9][0-9]/[0-9][0-9]/[0-9][0-9]' exp_iostat_raw.txt | cut -d ' ' -f 2 >exp_iostat_time.txt
grep -e '|__' exp_pidstat_raw.txt > exp_pidstat.txt



result_dir=rocksdb_result_${op_num}_${write_buffer_size}M_${user_thread_num}user_${backgroud_thread_num}bg_${num_multi_db}mutidb

mkdir ${result_dir}

mv ./exp* ${result_dir}
# done