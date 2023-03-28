#!/bin/bash

op_num=80000000
user_thread_num=1
backgroud_thread_num=2
num_multi_db=0
value_size=100
db_dir="/mnt/shunzi/hjx"
wal_dir="/mnt/ssd/hjx"

# for user_thread_num in 1 2 4 8
# do

rm -rf ${db_dir}/*
rm  ${wal_dir}/*.log
sudo -S fstrim ${db_dir}
sudo -S fstrim ${wal_dir}
sudo -S bash -c 'echo 1 > /proc/sys/vm/drop_caches'

top -H -b d 1 | grep -e 'db_bench' -e 'kv_bench' -e 'rocksdb:' > top.txt &
top_pid=$!
iostat -mtx 1 > iostat.txt &
iostat_pid=$!

../release/db_bench \
--db=${db_dir}/rocksdb  --wal_dir=${wal_dir} \
--num=${op_num} --num_multi_db=${num_multi_db} \
--threads=${user_thread_num} --max_background_jobs=${backgroud_thread_num} \
--value_size=${value_size} --benchmarks=fillrandom,stats  --histogram=true \
--compression_ratio=1 --compression_type=none | tee result.log


kill ${top_pid}
kill ${iostat_pid}

result_dir=result_rocksdb_${user_thread_num}user_${backgroud_thread_num}bg_${num_multi_db}mutidb

mkdir ${result_dir}

mv ./top.txt ${result_dir}
mv ./iostat.txt ${result_dir}
mv ./result.log ${result_dir}
mv ./OP_DATA ${result_dir}
mv ./OP_TIME.csv ${result_dir}
mv ./LOG ${result_dir}
# done