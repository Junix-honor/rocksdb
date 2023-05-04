#!/bin/bash
set -x
export LC_ALL=C

# mkdir /sys/fs/cgroup/memory/kv64
# echo 64G > /sys/fs/cgroup/memory/kv64/memory.limit_in_bytes
# echo 0 > /sys/fs/cgroup/memory/kv64/memory.swappiness

sudo -S bash -c 'echo 800000 > /proc/sys/fs/file-max'
ulimit -n 800000

op_num=8000000000
duration=1800
user_thread_num=1
backgroud_thread_num=2
num_multi_db=0
value_size=100
write_buffer_size=64
target_file_size_base=64
max_write_buffer_number=2
monitor_interval=1
# db_dir="/mnt/shunzi/hjx"
db_dir="/mnt/hjx/hjx"
wal_dir="/mnt/ssd/hjx"
# db_disk="nvme1n1"
db_disk="nvme0n1"
wal_disk="sdd"

direct=true
direct_read=false

disable_wal=false
wal_bytes_per_sync=$[1 * 1048576]  #1m

memtablerep="skip_list"
# memtablerep="prefix_hash"
# memtablerep="vector"
# memtablerep="hash_linkedlist"

batch_size=1


function db_bench() {
    rm ./exp_*
    rm -rf ${db_dir}/*
    rm ${wal_dir}/*.log
    sudo -S fstrim ${db_dir}
    sudo -S fstrim ${wal_dir}
    # sync;sudo -S bash -c 'echo 3 > /proc/sys/vm/drop_caches'
    sync; echo 3 > /proc/sys/vm/drop_caches

    # cgexec -g memory:kv64
    # perf record -F 9999 -g -o exp_perf.data -- \
    ../release/db_bench \
        --db=${db_dir}/rocksdb --wal_dir=${wal_dir} \
        --num=$((${op_num} / ${user_thread_num})) --num_multi_db=${num_multi_db} \
        --duration=${duration} \
        --threads=${user_thread_num} \
        --max_background_jobs=${backgroud_thread_num} \
        --value_size=${value_size} \
        --write_buffer_size=$((${write_buffer_size} << 20)) \
        --target_file_size_base=$((${target_file_size_base} << 20)) \
        --max_write_buffer_number=${max_write_buffer_number} \
        --benchmarks=fillrandom,stats --histogram=true \
        --use_direct_io_for_flush_and_compaction=${direct} \
        --use_direct_reads=${direct_read} \
        --enable_pipelined_write=false \
        --allow_concurrent_memtable_write=false \
        --disable_wal=${disable_wal} \
        --wal_bytes_per_sync=${wal_bytes_per_sync} \
        --memtablerep=${memtablerep} \
        --batch_size=${batch_size} \
        --compression_ratio=1 --compression_type=none > exp_result.log &

    db_bench_pid=$!

    top -H -b d ${monitor_interval} -p ${db_bench_pid} >exp_top_raw.txt &
    # top -H -b d ${monitor_interval} | grep -e 'db_bench' -e 'kv_bench' -e 'rocksdb:' > exp_top.txt &
    top_pid=$!
    iostat -mtx ${monitor_interval} >exp_iostat_raw.txt &
    # iostat -mtx ${monitor_interval} | grep -e ${db_disk} -e ${wal_disk} > exp_iostat.txt &
    iostat_pid=$!

    pidstat -p ${db_bench_pid} -d -t ${monitor_interval} >exp_pidstat_raw.txt &
    # pidstat -p ${db_bench_pid} -dRsuvr -H -t 1 > exp_pidstat.txt&
    pidstat_pid=$!

    pidstat -p ${db_bench_pid} -u -t ${monitor_interval} >exp_pidstat_cpu_raw.txt &
    pidstat_cpu_pid=$!

    # fg $(jobs | grep "db_bench" | awk '{print $1}')
    wait ${db_bench_pid}

    sync
    kill ${top_pid}
    kill ${iostat_pid}
    kill ${pidstat_pid}
    kill ${pidstat_cpu_pid}

    grep -e 'db_bench' -e 'kv_bench' -e 'rocksdb:' exp_top_raw.txt >exp_top.txt
    grep -E '^top' exp_top_raw.txt | awk '{print $3}' >exp_top_time.txt
    grep -e ${db_disk} -e ${wal_disk} exp_iostat_raw.txt >exp_iostat.txt
    grep '^[0-9][0-9]/[0-9][0-9]/[0-9][0-9]' exp_iostat_raw.txt | cut -d ' ' -f 2 >exp_iostat_time.txt
    grep -e '|__' exp_pidstat_raw.txt >exp_pidstat.txt
    grep '^\ \ L[0-9].*' exp_op_data | awk '{print $1,$5}' >exp_compaction_score

    cur_sec=$(date '+%s')
    result_dir=rocksdb_result_${op_num}_${write_buffer_size}M_${max_write_buffer_number}_${value_size}B_${user_thread_num}fg_${backgroud_thread_num}bg_${num_multi_db}mutidb_${cur_sec}

    rm -rf ./data/${result_dir}

    mkdir ./data/${result_dir}

    # perf script -i exp_perf.data > exp_out.perf
    # ../FlameGraph/stackcollapse-perf.pl exp_out.perf > exp_out.folded
    # ../FlameGraph/flamegraph.pl exp_out.folded > exp_perf.svg

    mv ./exp* ./data/${result_dir}
}

disable_wal=true
# db_bench

# value_size=1000
# user_thread_num=1
# backgroud_thread_num=4
# db_bench

user_thread_num=1
backgroud_thread_num=2
db_bench

# user_thread_num=1
# backgroud_thread_num=2
# db_bench
# user_thread_num=1
# backgroud_thread_num=4
# db_bench

# user_thread_num=1
# backgroud_thread_num=4
# db_bench

# user_thread_num=1
# backgroud_thread_num=8
# db_bench

# user_thread_num=1
# backgroud_thread_num=16
# db_bench

# user_thread_num=1
# backgroud_thread_num=32
# db_bench

# user_thread_num=1
# backgroud_thread_num=64
# db_bench

# op_num=4000000000
# value_size=100
# user_thread_num=1
# backgroud_thread_num=4
# db_bench
