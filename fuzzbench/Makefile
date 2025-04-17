export

# need to use "source" command
SHELL=/bin/bash

DIR=/dev/shm/user/fuzzbench
PYTHON_VERSION=3.10.15
FUZZBENCH_VERSION=4a47f4b

PYENV_ROOT="${HOME}/.pyenv"
PYTHONPATH=${DIR}

# experiment configs
config=fuzzbench-config.yaml
experiment_filestore=`cat ${config} | grep "experiment_filestore:" -m1 | awk '{print $$2}'`
report_filestore=`cat ${config} | grep "report_filestore:" -m1 | awk '{print $$2}'`
docker_registry=`cat ${config} | grep "docker_registry:" -m1 | awk '{print $$2}'`

experiment_fuzzers=`cat config.yaml | grep "fuzzers:" -m1 | awk '{print $$2}'`

# path to log output
CONSOLE_OUT=/dev/shm/user/log

# Download FuzzBench and set version
clone:
	git clone https://github.com/google/fuzzbench.git ${DIR} && \
	cd ${DIR} && \
	git checkout ${FUZZBENCH_VERSION} && \
	echo "${PYTHON_VERSION}" > ${DIR}/.python-version

pyenv:
	command -v pyenv >/dev/null || export PATH="${PYENV_ROOT}/bin:${PATH}"

# Install the packages used by fuzzbench into pyenv
install-dependencies:
	cd ${DIR} && \
	command -v pyenv >/dev/null || export PATH="${PYENV_ROOT}/bin:${PATH}" && \
	eval "$$(pyenv init -)" && \
	python3.10 --version && \
	make install-dependencies

# Apply patch
patch:
	git -C ${DIR} apply ${PWD}/fuzzbench.patch

# Copy fuzzers from /fuzzers to ${DIR}/fuzzers
cp:
	cp -r fuzzers/* ${DIR}/fuzzers

run:
	source ${DIR}/.venv/bin/activate && \
	mkdir -p ${experiment_filestore} && \
	mkdir -p ${report_filestore} && \
	python3.10 ${DIR}/experiment/run_experiment.py \
		--experiment-config ${config} \
		--experiment-name old-ddfuzz-1cpu-150parallel \
        --allow-uncommitted-changes \
		--runners-cpus 130 \
		--measurers-cpus 5 \
		--benchmarks curl_curl_fuzzer_http freetype2_ftfuzzer harfbuzz_hb-shape-fuzzer libjpeg-turbo_libjpeg_turbo_fuzzer libpcap_fuzz_both libpng_libpng_read_fuzzer libxml2_xml libxslt_xpath openssl_x509 re2_fuzzer stb_stbi_read_fuzzer vorbis_decode_fuzzer woff2_convert_woff2ttf_fuzzer \
		--fuzzers acecov_old_n4_ddfuzz no_acecov_old_ddfuzz ddfuzz128kb \
		> ${CONSOLE_OUT} 2>&1 &

report:
	source ${DIR}/.venv/bin/activate && \
	python3.10 parse.py -o ${report_filestore}/old-ddfuzz-1cpu-150parallel

# Output fuzzbench log continuously
tail:
	tail -f ${CONSOLE_OUT}

# Get local machine's status every 5 seconds
vmstat:
	vmstat 5

# Stop fuzzbench containers
stop:
	docker container stop `docker container ls | grep "${docker_registry}" | awk '{print $$1}'`

# Remove fuzzbench images
rmi:
	docker rmi --force `docker images -a | grep "${docker_registry}" | awk '{print $$3}'` && \
	docker rmi --force `docker images -a | grep "<none>" | awk '{print $$3}'`

clean:
	rm -rf ${DIR}
