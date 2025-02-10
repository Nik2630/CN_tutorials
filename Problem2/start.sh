if [ "$#" -ne 2 ]; then
  echo "Usage: bash start.sh <client_program_file> <number_of_clients>"
  exit 1
fi

CLIENT_PROGRAM=$1
NUM_CLIENTS=$2

if ! [ -f "$CLIENT_PROGRAM" ]; then
  echo "Error: Client program file '$CLIENT_PROGRAM' not found."
  exit 1
fi

# wait 3 seconds before starting the clients
sleep 3

START_TIME=$(date +%s.%N)

# Run clients in parallel using background processes
for i in $(seq 1 $NUM_CLIENTS); do
  python3 "$CLIENT_PROGRAM" "test_string_$i" &
done

wait # Wait for all background processes to complete

END_TIME=$(date +%s.%N)
ELAPSED_TIME=$(echo "$END_TIME - $START_TIME" | bc -l) # Calculate elapsed time using bc

echo "Total execution time: ${ELAPSED_TIME} seconds"