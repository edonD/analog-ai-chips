#!/usr/bin/env bash
# Watch for the first Claude agent to finish, then launch the finisher agent.

echo "Watching for optimization agent (PID of claude on pts/1) to finish..."

# Wait for the second claude process to exit (the one on pts/1, PID 4238)
while kill -0 4238 2>/dev/null; do
    sleep 10
done

echo "Optimization agent finished at $(date). Launching finisher agent..."
sleep 2

bash /home/ubuntu/analog-ai-chips/pvdd_regulator/00_error_amp/run_finish.sh
