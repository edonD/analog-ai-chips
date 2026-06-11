# Re-fetch the .asc test corpus (see SOURCES.md). Files stay local.
$tmp = "$env:TEMP\asc_corpus"
Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force $tmp | Out-Null
git clone --depth 1 https://github.com/mick001/Circuits-LTSpice $tmp\mick
git clone --depth 1 https://github.com/jmfermun/XTR111-LTspice-Model $tmp\xtr
git clone --depth 1 https://github.com/nunobrum/PyLTSpice $tmp\pylt

$dest = Join-Path $PSScriptRoot "asc"
New-Item -ItemType Directory -Force $dest | Out-Null
$picks = @('Common-emitter-amplifier-design.asc', 'Instrumentation-amplifier.asc',
           'Full-bridge-rectifier.asc', 'Differences-amplifier.asc',
           'Push-pull-amplifier.asc')
foreach ($p in $picks) {
    Get-ChildItem $tmp\mick -Recurse -Filter $p |
        Select-Object -First 1 | Copy-Item -Destination $dest
}
Copy-Item $tmp\xtr\*.asc, $tmp\xtr\*.asy $dest -ErrorAction SilentlyContinue
Get-ChildItem $tmp\pylt -Recurse -Filter *.asc |
    Select-Object -First 3 | Copy-Item -Destination $dest
Write-Host "corpus ready: $((Get-ChildItem $dest -Filter *.asc).Count) sheets in $dest"
Write-Host "smoke test:  python -m glass render `"$dest\Common-emitter-amplifier-design.asc`" --png"
