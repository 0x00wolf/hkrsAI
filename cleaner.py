# Simple script to save JSON logs into a human readable txt format
import sys
import json


if len(sys.argv) != 2:
    print('error, no file provided')
else:
    print(f'attempting to clean {sys.argv[1]}')
try:
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    output_file = f'{sys.argv[1]}.clean.txt'
    out_file = open(output_file, 'w')
    for i in range(len(data)):
        out_file.write(f"----------------\n$ {data[i]['role']}:\n\n" \
                f"{data[i]['content']}\n\n")
    out_file.close()
    print(f'saving cleaned log to: {output_file}')
except Exception as e:
    print(f'error {e}')
    sys.exit()
