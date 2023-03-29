//
//
//

#pragma once

#include <string>
#include <stdarg.h>
#define STATISTIC_OPEN

#define LZW_INFO
#ifdef LZW_INFO
#define RECORD_INFO(file_num,format,...)   LZW_LOG(file_num,format,##__VA_ARGS__)

#else
#define RECORD_INFO(file_num,format,...)
#endif

#define PRI_DEBUG
#ifdef PRI_DEBUG
#define DBG_PRINT(format, a...) printf(" DEBUG:%4d %-20s : " format, __LINE__, __FUNCTION__,  ##a)
#else
#define DBG_PRINT(format, a...)
#endif

#define LZW_DEBUG

#ifdef LZW_DEBUG
#define RECORD_LOG(format,...)   LZW_LOG(0,format,##__VA_ARGS__)

#else
#define RECORD_LOG(format,...)
#endif

const std::string log_file0("./exp_log");
const std::string log_file1("./exp_op_time.csv");
const std::string log_file2("./exp_op_data");
const std::string log_file3("./exp_stall.csv");
// const std::string log_file4("./exp_foreground_stall.csv");
// const std::string log_file5("PerSecondLatency.csv");


extern void init_log_file();

extern void LZW_LOG(int file_num,const char* format, ...);
extern uint64_t bench_start_time;