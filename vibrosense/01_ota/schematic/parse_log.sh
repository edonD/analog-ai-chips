#!/bin/bash
# Live monitor: tail -f agent.log | bash parse_log.sh
# Or one-shot: bash parse_log.sh < agent.log

python3 -c "
import sys, json

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    if line.startswith('==='):
        print(line, flush=True)
        continue
    try:
        obj = json.loads(line)
        t = obj.get('type','')
        if t == 'assistant':
            msg = obj.get('message',{})
            for c in msg.get('content',[]):
                if c.get('type') == 'text' and c.get('text','').strip():
                    print(f'\033[1;36m[AGENT]\033[0m {c[\"text\"].strip()}', flush=True)
                elif c.get('type') == 'tool_use':
                    name = c.get('name','')
                    inp = c.get('input',{})
                    if name == 'Bash':
                        cmd = inp.get('command','')[:200]
                        print(f'\033[1;33m[CMD]\033[0m {cmd}', flush=True)
                    elif name == 'Write':
                        fp = inp.get('file_path','')
                        print(f'\033[1;32m[WRITE]\033[0m {fp}', flush=True)
                    elif name == 'Edit':
                        fp = inp.get('file_path','')
                        print(f'\033[1;32m[EDIT]\033[0m {fp}', flush=True)
                    elif name == 'Read':
                        fp = inp.get('file_path','')
                        print(f'\033[34m[READ]\033[0m {fp}', flush=True)
                    elif name == 'Glob':
                        print(f'\033[34m[GLOB]\033[0m {inp.get(\"pattern\",\"\")}', flush=True)
                    elif name == 'Grep':
                        print(f'\033[34m[GREP]\033[0m {inp.get(\"pattern\",\"\")}', flush=True)
                    else:
                        print(f'\033[35m[TOOL:{name}]\033[0m', flush=True)
        elif t == 'tool_result':
            content = obj.get('content','')
            # Show errors and key results briefly
            if isinstance(content, str) and ('error' in content.lower() or 'Error' in content):
                lines = content.strip().split('\n')
                for l in lines[:5]:
                    if 'error' in l.lower() or 'Error' in l:
                        print(f'\033[1;31m[ERROR]\033[0m {l.strip()[:200]}', flush=True)
    except json.JSONDecodeError:
        pass
" 2>/dev/null
