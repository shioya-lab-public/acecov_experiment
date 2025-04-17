import pandas
import argparse
import sys

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

	df = pandas.read_csv(args.file)
	df = df[['fuzzer', 'benchmark', 'trial_id', 'time', 'edges_covered']]

	end = 86400
	df = df[df['time'] == end]

	with open(args.out, 'w') as f:
		f.write('fuzzer,benchmark,mean,median\n')

		for bench in df['benchmark'].unique():
			bdf = df[df['benchmark'] == bench]
			for fuzzer in bdf['fuzzer'].unique():
				fdf = bdf[bdf['fuzzer'] == fuzzer]
				f.write(f'{fuzzer},{bench},{fdf["edges_covered"].mean()},{fdf["edges_covered"].median()}\n')

if __name__ == '__main__':
	sys.exit(main())
