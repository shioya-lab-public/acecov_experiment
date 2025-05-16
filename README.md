# Scripts for Fuzzer Experimentation
This repository provides scripts to set up environments for evaluating fuzzing techniques (fuzzers) using the [FuzzBench](https://github.com/google/fuzzbench) and [MAGMA](https://github.com/HexHive/magma) frameworks. The repository assumes an environment capable of running Docker and Python venv. It was used for the evaluation of [AceCov](https://github.com/shioya-lab-public/AceCov).

## Running FuzzBench
To evaluate fuzzers with FuzzBench, follow these steps:
1. If you wish to evaluate a fuzzer not included in FuzzBench, add it in `fuzzbench/fuzzers/` in a format compatible with FuzzBench.
2. Edit the configuration file `fuzzbench/fuzzbench-config.yaml` to specify experiment parameters. Refer to the FuzzBench documentation for configuration details.
3. Specify the fuzzer(s) to evaluate and the experiment name in `fuzzbench/config.yaml`.
4. Define the evaluation environment in `fuzzbench/Makefile`.
5. Execute the following commands:
```bash
cd fuzzbench
make clone
make pyenv
make install-dependencies
make patch
make cp
make run
```

## Running MAGMA
To evaluate fuzzers with MAGMA, follow these steps:
1. If you wish to evaluate a fuzzer not included in MAGMA, add it in `magma/fuzzers/` in a format compatible with MAGMA.
2. Edit the configuration file `magma/config.yaml` to specify the experiment duration and number of trials.
3. Specify the experimental environment in `magma/.env`. A sample configuration is provided in `magma/.sample.env`.
4. Execute the following commands:
```bash
cd magma
make clone
make patch
make cp
make captainrc
make install
make run
```