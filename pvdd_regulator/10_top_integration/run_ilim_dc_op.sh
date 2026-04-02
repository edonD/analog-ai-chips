#!/bin/bash
# Run .OP-based current limit DC characterization
# More reliable than transient approach — finds true DC equilibrium

cd /home/ubuntu/analog-ai-chips/pvdd_regulator/10_top_integration

echo "# iload_ma pvdd_v" > ilim_dc_data.txt

# Use resistance values to sweep from light load to short circuit
# R = V/I: at 5V, 5000=1mA, 500=10mA, 250=20mA, 100=50mA, etc.
for rload in 100000 5000 1000 500 333 250 200 166 143 125 111 100 91 83 77 71 62.5 55 50 45 40 35 30 25 20 15 10 7 5 3 2 1 0.5 0.1; do
  sed "s/RLOAD_PLACEHOLDER/${rload}/g" tb_ilim_dc_op.spice > tb_ilim_point_op.spice
  result=$(ngspice -b tb_ilim_point_op.spice 2>&1 | grep -E "pvdd_v|iload_ma")
  pvdd=$(echo "$result" | grep pvdd_v | awk '{print $NF}')
  ima=$(echo "$result" | grep iload_ma | awk '{print $NF}')

  # Handle empty results
  if [ -z "$pvdd" ] || [ -z "$ima" ]; then
    echo "SKIP Rload=${rload} (convergence fail)"
    continue
  fi

  echo "${ima} ${pvdd}" >> ilim_dc_data.txt
  echo "Rload=${rload}ohm -> PVDD=${pvdd}V, Iload=${ima}mA"
done

echo "=== DONE ==="
