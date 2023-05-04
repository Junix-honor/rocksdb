#!/bin/bash
set -x
export LC_ALL=C

# mkdir /sys/fs/cgroup/memory/kv64
# echo 64G > /sys/fs/cgroup/memory/kv64/memory.limit_in_bytes
# echo 0 > /sys/fs/cgroup/memory/kv64/memory.swappiness

# sudo -S bash -c 'echo 800000 > /proc/sys/fs/file-max'
# ulimit -n 800000

op_num=20000000
duration=0
user_thread_num=1
backgroud_thread_num=2 
num_multi_db=0
value_size=100
write_buffer_size=16
max_write_buffer_number=2
monitor_interval=1
db_dir="/mnt/shunzi/hjx"
wal_dir="/mnt/ssd/hjx"
db_disk="nvme1n1"
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
    rm -rf ${wal_dir}/*
    sudo -S fstrim ${db_dir}
    sudo -S fstrim ${wal_dir}
    sudo -S bash -c 'echo 1 > /proc/sys/vm/drop_caches'

    # cgexec -g memory:kv64
    perf record -F 9999 -g -o exp_perf.data -- \
    ../release/db_bench \
        --db=${db_dir}/rocksdb --wal_dir=${wal_dir} \
        --num=$((${op_num} / ${user_thread_num})) --num_multi_db=${num_multi_db} \
        --duration=${duration} \
        --threads=${user_thread_num} \
        --max_background_jobs=${backgroud_thread_num} \
        --value_size=${value_size} \
        --write_buffer_size=$((${write_buffer_size} << 20)) \
        --max_write_buffer_number=${max_write_buffer_number} \
        --benchmarks=fillrandom,stats --histogram=true \
        --use_direct_io_for_flush_and_compaction=${direct} \
        --use_direct_reads=${direct_read} \
        --enable_pipelined_write=false \
        --allow_concurrent_memtable_write=true \
        --disable_wal=${disable_wal} \
        --wal_bytes_per_sync=${wal_bytes_per_sync} \
        --memtablerep=${memtablerep} \
        --batch_size=${batch_size} \
        --compression_ratio=1 --compression_type=none >exp_result.log 

    cur_sec=$(date '+%s')
    result_dir=rocksdb_result_${op_num}_${write_buffer_size}M_${max_write_buffer_number}_${value_size}B_${user_thread_num}fg_${backgroud_thread_num}bg_${num_multi_db}mutidb_perf_${cur_sec}

    rm -rf ./data/${result_dir}

    mkdir ./data/${result_dir}

    perf script -i exp_perf.data > exp_out.perf
    ../FlameGraph/stackcollapse-perf.pl exp_out.perf > exp_out.folded
    ../FlameGraph/flamegraph.pl exp_out.folded > exp_${result_dir}_flame.svg
    
    rm ./exp_perf.data
    rm ./exp_out.perf
    # rm ./exp_out.folded

    mv ./exp* ./data/${result_dir}
}

# batch_size=20
# user_thread_num=1
# db_bench
# user_thread_num=2
# db_bench 
# user_thread_num=4
# db_bench  
# user_thread_num=8
# db_bench 
# user_thread_num=16
# db_bench 

user_thread_num=8
# disable_wal=true 
# user_thread_num=1
# num_multi_db=0
db_bench 

# user_thread_num=32
# num_multi_db=8
# db_bench

# user_thread_num=32
# num_multi_db=16
# db_bench

# user_thread_num=8
# db_bench 

# user_thread_num=16
# num_multi_db=4
# db_bench 

# user_thread_num=16
# num_multi_db=8
# db_bench 

# user_thread_num=16
# num_multi_db=16
# db_bench 

# user_thread_num=16
# num_multi_db=0
# db_bench 

# user_thread_num=16
# num_multi_db=4
# db_bench 



# batch_size=1
# user_thread_num=40
# db_bench 
# backgroud_thread_num=1
# disable_wal=true 

# batch_size=1
# user_thread_num=8
# db_bench