#!/bin/bash
# 流量监控脚本 - 同时显示累计和增量流量
# 用法: ./traffic_monitor.sh [刷新间隔秒数，默认5]

INTERVAL=${1:-5}
BASELINE_FILE="/tmp/traffic_baseline.txt"

# 颜色定义
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

format_bytes() {
    local bytes=$1
    if [ "$bytes" -ge 1073741824 ] 2>/dev/null; then
        printf "%.2f GB" $(echo "scale=2; $bytes/1073741824" | bc)
    elif [ "$bytes" -ge 1048576 ] 2>/dev/null; then
        printf "%.2f MB" $(echo "scale=2; $bytes/1048576" | bc)
    elif [ "$bytes" -ge 1024 ] 2>/dev/null; then
        printf "%.2f KB" $(echo "scale=2; $bytes/1024" | bc)
    else
        printf "%d B" "$bytes"
    fi
}

# 记录基准值
echo "正在记录基准值..."
START_TIME=$(date '+%Y-%m-%d %H:%M:%S')
nettop -P -L 1 -J bytes_in,bytes_out 2>/dev/null | tail -n +2 | grep -v "^$" | \
while IFS=',' read -r name bytes_in bytes_out; do
    proc_name=$(echo "$name" | sed 's/\.[0-9]*$//' | tr ' ' '_')
    echo "${proc_name},${bytes_in},${bytes_out}"
done > "$BASELINE_FILE"

echo "基准值已记录，开始监控..."
sleep 1

while true; do
    printf "\033c"

    echo -e "${CYAN}══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}                      📊 应用流量监控                              ${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════════════════${NC}"
    echo -e "起始: ${START_TIME} | 当前: $(date '+%Y-%m-%d %H:%M:%S')"
    echo -e "${CYAN}──────────────────────────────────────────────────────────────────${NC}"
    printf "${YELLOW}%-24s %14s %14s${NC}\n" "应用" "累计总量" "本次增量"
    echo -e "${CYAN}──────────────────────────────────────────────────────────────────${NC}"

    # 获取当前流量，计算增量
    > /tmp/traffic_combined.txt
    nettop -P -L 1 -J bytes_in,bytes_out 2>/dev/null | tail -n +2 | grep -v "^$" | \
    while IFS=',' read -r name bytes_in bytes_out; do
        proc_name=$(echo "$name" | sed 's/\.[0-9]*$//' | tr ' ' '_')
        total=$((bytes_in + bytes_out))

        # 查找基准值计算增量
        baseline=$(grep "^${proc_name}," "$BASELINE_FILE" 2>/dev/null | head -1)
        if [ -n "$baseline" ]; then
            base_in=$(echo "$baseline" | cut -d',' -f2)
            base_out=$(echo "$baseline" | cut -d',' -f3)
            diff_in=$((bytes_in - base_in))
            diff_out=$((bytes_out - base_out))
        else
            diff_in=$bytes_in
            diff_out=$bytes_out
        fi

        [ "$diff_in" -lt 0 ] 2>/dev/null && diff_in=$bytes_in
        [ "$diff_out" -lt 0 ] 2>/dev/null && diff_out=$bytes_out
        diff_total=$((diff_in + diff_out))

        # 保存: 累计总量,进程名,增量,累计下载,累计上传,增量下载,增量上传
        [ "$total" -ge 1024 ] && echo "${total},${proc_name},${diff_total},${bytes_in},${bytes_out},${diff_in},${diff_out}"
    done | sort -t',' -k1 -rn > /tmp/traffic_combined.txt

    # 显示前10
    head -10 /tmp/traffic_combined.txt | while IFS=',' read -r total name diff_total bytes_in bytes_out diff_in diff_out; do
        [ -z "$total" ] && continue

        total_str=$(format_bytes "$total")
        diff_str=$(format_bytes "$diff_total")

        # 根据增量大小着色
        if [ "$diff_total" -ge 104857600 ] 2>/dev/null; then
            color=$RED
        elif [ "$diff_total" -ge 10485760 ] 2>/dev/null; then
            color=$YELLOW
        else
            color=$GREEN
        fi

        display_name=$(echo "$name" | tr '_' ' ' | cut -c1-22)
        printf "${color}%-24s %14s %14s${NC}\n" "$display_name" "$total_str" "+$diff_str"
    done

    echo -e "${CYAN}──────────────────────────────────────────────────────────────────${NC}"

    # 计算总流量
    total_all=0
    diff_all=0
    while IFS=',' read -r total name diff_total rest; do
        [ -z "$total" ] && continue
        total_all=$((total_all + total))
        diff_all=$((diff_all + diff_total))
    done < /tmp/traffic_combined.txt

    printf "${CYAN}%-24s %14s %14s${NC}\n" "全部应用总计" "$(format_bytes $total_all)" "+$(format_bytes $diff_all)"

    echo -e "${CYAN}══════════════════════════════════════════════════════════════════${NC}"
    echo -e "提示: ${RED}红色${NC}>100MB增量 ${YELLOW}黄色${NC}>10MB增量 ${GREEN}绿色${NC}<10MB增量"

    sleep "$INTERVAL"
done
