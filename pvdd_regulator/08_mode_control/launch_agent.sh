#!/bin/bash
cd /home/ubuntu/analog-ai-chips/pvdd_regulator/08_mode_control
exec claude -p --dangerously-skip-permissions --verbose --output-format stream-json \
  "Read run_design.md in the current directory completely. It contains your full autonomous task for designing Block 08 Mode Control. Execute all 5 phases: design the circuit in design.cir, write all testbenches, run the experiment loop iterating until all 16 specs pass, create plots and README, and create the xschem schematic and PNG. Start now and NEVER STOP until done. After each working improvement commit with git add pvdd_regulator/08_mode_control/ and git commit. Build incrementally - start with one comparator." \
  > /home/ubuntu/analog-ai-chips/pvdd_regulator/08_mode_control/agent.log 2>&1
