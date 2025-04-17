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

	sum_df = df.groupby(['benchmark', 'program', 'fuzzer']).size().reset_index(name='sum')

	types_df = df.groupby(['benchmark', 'program', 'fuzzer', 'bug']).size().reset_index().groupby(['benchmark', 'program', 'fuzzer']).size().reset_index(name='types')

	df = pandas.merge(sum_df, types_df, on=['benchmark', 'program', 'fuzzer'])
	print(df.groupby(['fuzzer'], as_index=False)[['sum', 'types']].sum())
	df = pandas.concat([df, df.groupby(['benchmark', 'program', 'fuzzer'], as_index=False)[['sum', 'types']].sum()], ignore_index=False)
	df = df.pivot(index=['benchmark', 'program'], columns='fuzzer', values=['sum', 'types']).reset_index()
	df.to_csv(args.out, index=False)

if __name__ == '__main__':
	sys.exit(main())
