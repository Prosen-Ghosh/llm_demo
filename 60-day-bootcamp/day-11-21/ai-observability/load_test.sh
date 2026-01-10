#!/bin/bash

# Advanced Load Test with Progress Bars
# Run: chmod +x load_test_advanced.sh && ./load_test_advanced.sh

API_URL="http://localhost:8000/generate"
TEST_DURATION=320
MAX_CONCURRENT=40  # Maximum concurrent requests
INITIAL_CONCURRENT=25  # Start with fewer concurrent requests
TIMEOUT_SECONDS=300  # 5 minutes per request

# Create results directory
RESULTS_DIR="load_test_results_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS_DIR"

SUMMARY_CSV="$RESULTS_DIR/summary.csv"
DETAILED_LOG="$RESULTS_DIR/detailed.log"
LATENCY_LOG="$RESULTS_DIR/latency.csv"
ERROR_LOG="$RESULTS_DIR/errors.log"

# Initialize files
echo "timestamp,request_id,prompt,status,http_code,response_time,total_time" > "$SUMMARY_CSV"
echo "request_id,latency_ms" > "$LATENCY_LOG"
echo "=== LOAD TEST STARTED ===" > "$DETAILED_LOG"
echo "=== ERROR LOG ===" > "$ERROR_LOG"

# Function to display progress bar
progress_bar() {
    local duration=$1
    local elapsed=$2
    local width=50
    local percent=$((elapsed * 100 / duration))
    local completed=$((elapsed * width / duration))
    local remaining=$((width - completed))
    
    printf "\r["
    printf "%${completed}s" | tr ' ' '='
    printf "%${remaining}s" | tr ' ' ' '
    printf "] %3d%%" "$percent"
}

# Function to run load test
run_load_test() {
    local start_time=$(date +%s)
    local end_time=$((start_time + TEST_DURATION))
    local request_id=0
    local concurrent=$INITIAL_CONCURRENT
    
    # Array of diverse prompts
    prompts=(
        "fire"
    )
    
    echo "Starting load test..."
    echo "Duration: ${TEST_DURATION}s | Max Concurrent: ${MAX_CONCURRENT}"
    echo "Results will be saved to: $RESULTS_DIR"
    echo ""
    
    # Monitor system resources (optional - requires sysstat)
    if command -v mpstat &> /dev/null; then
        echo "System monitoring enabled"
        mpstat 5 > "$RESULTS_DIR/cpu_usage.log" &
        MONITOR_PID=$!
    fi
    
    while [ $(date +%s) -lt $end_time ]; do
        local elapsed=$(( $(date +%s) - start_time ))
        
        # Display progress
        progress_bar $TEST_DURATION $elapsed
        
        # Dynamically adjust concurrency
        if [ $elapsed -gt $((TEST_DURATION / 3)) ] && [ $concurrent -lt $MAX_CONCURRENT ]; then
            concurrent=$((concurrent + 1))
        fi
        
        # Run batch of requests
        for ((i=0; i<concurrent; i++)); do
            request_id=$((request_id + 1))
            local prompt="${prompts[$RANDOM % ${#prompts[@]}]}"
            
            # URL encode the prompt
            local encoded_prompt=$(printf '%s' "$prompt" | jq -sRr @uri 2>/dev/null || echo "$prompt" | sed 's/ /%20/g')
            
            (
                local req_start=$(date +%s.%N)
                local response=$(curl -s -w "HTTP_CODE:%{http_code}\nTIME_TOTAL:%{time_total}\n" \
                    -X POST \
                    --max-time $TIMEOUT_SECONDS \
                    "$API_URL?prompt=$encoded_prompt" \
                    2>&1)
                
                local req_end=$(date +%s.%N)
                local total_time=$(echo "$req_end - $req_start" | bc)
                local http_code=$(echo "$response" | grep "HTTP_CODE:" | cut -d: -f2)
                local response_time=$(echo "$response" | grep "TIME_TOTAL:" | cut -d: -f2)
                
                local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
                
                # Log based on status
                if [[ "$http_code" == "200" ]]; then
                    echo "$timestamp,$request_id,\"$prompt\",SUCCESS,$http_code,$response_time,$total_time" >> "$SUMMARY_CSV"
                    echo "$request_id,$(echo "$response_time * 1000" | bc)" >> "$LATENCY_LOG"
                elif [[ -n "$http_code" ]]; then
                    echo "$timestamp,$request_id,\"$prompt\",FAILED,$http_code,$response_time,$total_time" >> "$SUMMARY_CSV"
                    echo "[ERROR] Request $request_id: HTTP $http_code - $prompt" >> "$ERROR_LOG"
                else
                    echo "$timestamp,$request_id,\"$prompt\",TIMEOUT,000,$total_time,$total_time" >> "$SUMMARY_CSV"
                    echo "[TIMEOUT] Request $request_id: $prompt" >> "$ERROR_LOG"
                fi
            ) &
        done
        
        # Wait for batch to complete or continue after 1 second
        sleep 1
        wait
    done
    
    printf "\n"
    
    # Stop system monitor if running
    if [ -n "$MONITOR_PID" ]; then
        kill $MONITOR_PID 2>/dev/null
    fi
}

# Generate report
generate_report() {
    echo ""
    echo "=== LOAD TEST REPORT ==="
    echo ""
    
    # Read CSV and calculate statistics
    total=$(tail -n +2 "$SUMMARY_CSV" | wc -l)
    success=$(grep -c "SUCCESS" "$SUMMARY_CSV")
    failed=$(grep -c "FAILED" "$SUMMARY_CSV")
    timeout=$(grep -c "TIMEOUT" "$SUMMARY_CSV")
    
    echo "Total Requests: $total"
    echo "Successful: $success ($(echo "scale=2; $success * 100 / $total" | bc)%)"
    echo "Failed: $failed ($(echo "scale=2; $failed * 100 / $total" | bc)%)"
    echo "Timeout: $timeout ($(echo "scale=2; $timeout * 100 / $total" | bc)%)"
    echo ""
    
    # Calculate average response time
    if [ $success -gt 0 ]; then
        avg_time=$(awk -F, '/SUCCESS/ {sum+=$6; count++} END {print sum/count}' "$SUMMARY_CSV")
        echo "Average Response Time: $(echo "scale=2; $avg_time" | bc)s"
        
        # Find min/max response times
        min_time=$(awk -F, '/SUCCESS/ {if(min==""){min=$6}; if($6<min) min=$6} END {print min}' "$SUMMARY_CSV")
        max_time=$(awk -F, '/SUCCESS/ {if($6>max) max=$6} END {print max}' "$SUMMARY_CSV")
        echo "Min Response Time: ${min_time}s"
        echo "Max Response Time: ${max_time}s"
    fi
    
    # Calculate requests per second
    rpm=$((total * 60 / TEST_DURATION))
    echo ""
    echo "Requests per Minute: $rpm"
    
    # Generate latency percentiles if latency file exists
    if [ -f "$LATENCY_LOG" ] && [ $(wc -l < "$LATENCY_LOG") -gt 1 ]; then
        echo ""
        echo "=== LATENCY PERCENTILES (ms) ==="
        # Skip header and sort latency values
        tail -n +2 "$LATENCY_LOG" | cut -d, -f2 | sort -n > "$RESULTS_DIR/latency_sorted.txt"
        
        total_latencies=$(wc -l < "$RESULTS_DIR/latency_sorted.txt")
        
        # Calculate percentiles
        p50_line=$((total_latencies * 50 / 100))
        p90_line=$((total_latencies * 90 / 100))
        p95_line=$((total_latencies * 95 / 100))
        p99_line=$((total_latencies * 99 / 100))
        
        p50=$(sed "${p50_line}q;d" "$RESULTS_DIR/latency_sorted.txt")
        p90=$(sed "${p90_line}q;d" "$RESULTS_DIR/latency_sorted.txt")
        p95=$(sed "${p95_line}q;d" "$RESULTS_DIR/latency_sorted.txt")
        p99=$(sed "${p99_line}q;d" "$RESULTS_DIR/latency_sorted.txt")
        
        echo "p50 (median): ${p50}ms"
        echo "p90: ${p90}ms"
        echo "p95: ${p95}ms"
        echo "p99: ${p99}ms"
    fi
    
    # Show errors if any
    if [ $failed -gt 0 ] || [ $timeout -gt 0 ]; then
        echo ""
        echo "=== ERRORS DETECTED ==="
        tail -20 "$ERROR_LOG"
    fi
    
    echo ""
    echo "Full results available in: $RESULTS_DIR"
}

# Main execution
echo "API Load Test Tool"
echo "=================="
run_load_test
generate_report