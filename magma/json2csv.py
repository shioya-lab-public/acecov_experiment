import argparse
import sys
import json

def main(args=None):
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('-o',
						'--out',
						required=False,
						type=str,
						default="out.json"
						)
	parser.add_argument('file', type=str)

	args = parser.parse_args(args)

	f = open(args.file, "r")
	j = json.load(f)
	result: dict = j["results"]

	with open(args.out, "w") as output:
		output.write("fuzzer,benchmark,program,trial,type,bug,time\n")
		fuzzers = list(result.keys())
		for f in fuzzers:
			bench = list(result[f].keys())
			for b in bench:
				prog = list(result[f][b])
				for p in prog:
					tr = list(result[f][b][p])
					for t in tr:
						reached: dict = result[f][b][p][t]["reached"]
						triggered: dict = result[f][b][p][t]["triggered"]
						for t in triggered:
							output.write(f"{f},{b},{p},{t},reached,{t},{triggered[t]}\n")

if __name__ == '__main__':
	sys.exit(main())
