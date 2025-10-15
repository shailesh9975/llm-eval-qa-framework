#!/bin/bash

# Function to check if the API is ready
wait_for_api() {
    echo "Waiting for API to be ready..."
    for i in {1..10}; do
        RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/evaluate -X POST -H "Content-Type: application/json" -d '{"prompt":"ping"}')
        if [ "$RESPONSE" == "200" ]; then
            echo "API is ready!"
            return 0
        fi
        sleep 1
    done
    echo "API did not become ready in time."
    return 1
}

# Step 1: Start Node.js API in background
echo "Starting Node.js mock API..."
cd api
nohup node server.js > api.log 2>&1 &
API_PID=$!
cd ..
echo "Node.js API PID: $API_PID"

# Step 2: Wait for API readiness
if ! wait_for_api; then
    echo "Exiting due to API startup failure."
    kill $API_PID
    exit 1
fi

# Step 3: Run Python evaluator
echo "Running Python evaluator..."
python3 -m evaluate.evaluator

# Step 4: Stop Node.js API
echo "Stopping Node.js API..."
kill $API_PID
echo "Done. Results saved to evaluate/reports/latest_metrics.json"

