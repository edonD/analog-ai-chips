#!/bin/bash
# Run discrete steady-state current limit measurements
# Each point: start from IC, let regulator settle 20ms, apply load, measure at 25ms

cd /home/ubuntu/analog-ai-chips/pvdd_regulator/10_top_integration

echo "# iload_ma pvdd_v" > ilim_dc_data.txt

for iload in 0 0.001 0.005 0.01 0.015 0.02 0.025 0.03 0.035 0.04 0.042 0.044 0.046 0.048 0.049 0.05 0.051 0.052 0.053 0.054 0.055 0.056 0.058 0.06 0.065 0.07 0.08 0.1; do
  iload_ma=$(echo "$iload * 1000" | bc)

  # Generate testbench from template
  sed "s/ILOAD_PLACEHOLDER/${iload}/g" tb_plot7_ilim_dc.spice > tb_ilim_point.spice

  # Run ngspice
  result=$(ngspice -b tb_ilim_point.spice 2>&1 | grep "pvdd_final" | tail -1 | awk '{print $NF}')

  # Handle empty result
  if [ -z "$result" ]; then
    result="NaN"
  fi

  echo "${iload_ma} ${result}" >> ilim_dc_data.txt
  echo "Iload=${iload_ma}mA -> PVDD=${result}V"
done

echo "=== DONE ==="
echo "Data saved to ilim_dc_data.txt"
