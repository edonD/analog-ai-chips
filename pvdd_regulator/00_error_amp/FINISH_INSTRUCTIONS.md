# Finish Instructions — READ AND EXECUTE AFTER OPTIMIZATION LOOP

When you are done optimizing the error amplifier, you MUST complete ALL of the following steps before exiting:

## 1. Final Commit
- `git add` all modified and new files in this block directory
- Commit with a descriptive message summarizing final performance

## 2. Update README.md
- Create/update `README.md` with full documentation:
  - Topology description and schematic
  - Device table (all transistors with W/L/m)
  - Operating point summary
  - All spec results in a table
  - All plots embedded inline

## 3. Generate Xschem Schematic
- Create an xschem `.sch` file for the error amplifier
- The schematic MUST be very well organized with clear signal flow
- All nodes must be properly connected with net labels
- Title block must be visible with block name, author, date
- Use generous margins and spacing — no cramped layout
- Group: input pair together, mirrors together, output stage together
- Signal flow: inputs on left, output on right, supplies top/bottom
- Export to PNG using xschem --export

## 4. Push to GitHub
```bash
git add pvdd_regulator/00_error_amp/
git commit -m "feat(pvdd/00): final error amp — schematic, README, all plots"
git push origin autoresearch/error-amp-mar27
```
