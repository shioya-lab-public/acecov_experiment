include .env

export

# experiment configs
config=${PWD}/config.yaml

PYTHONPATH=${DIR}

# Download MAGMA and set version
clone:
	git clone https://github.com/HexHive/magma.git ${DIR} && \
	cd ${DIR} && \
	git checkout ${MAGMA_VERSION} && \
	echo "${PYTHON_VERSION}" > ${DIR}/.python-version

# Apply patch
patch:
	git -C ${DIR} apply ${PWD}/magma.patch

# Copy fuzzers from /fuzzers to ${DIR}/fuzzers
# Why not symbolic link? "COPY" in Dockerfile do not copy real files.
cp:
	cp -r fuzzers/* ${DIR}/fuzzers

captainrc:
	echo WORKDIR=${experiment_dir} > ${DIR}/captainrc && \
	echo WORKERS=180 >> ${DIR}/captainrc && \
	echo REPEAT=`cat ${config} | grep "EXPERIMENT_TRIAL:" -m1 | awk '{print $$2}'` >> ${DIR}/captainrc && \
	echo TIMEOUT=`cat ${config} | grep "EXPERIMENT_TIME:" -m1 | awk '{print $$2}'` >> ${DIR}/captainrc && \
	echo CACHE_ON_DISK=0 >> ${DIR}/captainrc && \
	echo TMPFS_SIZE=32g >> ${DIR}/captainrc && \
	echo POLL=30 >> ${DIR}/captainrc && \
	echo WORKER_MODE=1 >> ${DIR}/captainrc && \
	echo MAGMA=${DIR} >> ${DIR}/captainrc && \
	echo "FUZZERS=(acecov_old_n4_128kb no_acecov_old_128kb ddfuzz_128kb)" >> ${DIR}/captainrc && \
	echo "acecov_old_n4_128kb_TARGETS=(libpng libsndfile libtiff libxml2 lua openssl php sqlite3)" >> ${DIR}/captainrc
	echo "no_acecov_old_128kb_TARGETS=(libpng libsndfile libtiff libxml2 lua openssl php sqlite3)" >> ${DIR}/captainrc
	echo "ddfuzz_128kb_TARGETS=(libpng libsndfile libtiff libxml2 lua openssl php sqlite3)" >> ${DIR}/captainrc

run:
	cd ${DIR} && \
	command -v pyenv >/dev/null || export PATH="${PYENV_ROOT}/bin:${PATH}" && \
	eval "$$(pyenv init -)" && \
	bash tools/captain/run.sh /dev/shm/yoshida/magma/captainrc > /dev/shm/yoshida/magma-log 2>&1 &

# Output MAGMA log continuously
tail:
	tail -f ${CONSOLE_OUT}

install:
	cd ${DIR} && \
	command -v pyenv >/dev/null || export PATH="${PYENV_ROOT}/bin:${PATH}" && \
	eval "$$(pyenv init -)" && \
	pip install pandas==1.5.3 jinja2 lifelines seaborn scikit_posthocs

exp2json:
	cd ${DIR} && \
	command -v pyenv >/dev/null || export PATH="${PYENV_ROOT}/bin:${PATH}" && \
	eval "$$(pyenv init -)" && \
	python3 tools/benchd/exp2json.py ${experiment_dir} ${RESULT_DIR}

report:
	cd ${DIR} && \
	command -v pyenv >/dev/null || export PATH="${PYENV_ROOT}/bin:${PATH}" && \
	eval "$$(pyenv init -)" && \
	python3 json2csv.py ${RESULT_DIR} ${RESULT_DIR}.csv && \
	python3 csv2table.py ${RESULT_DIR}.csv ${RESULT_DIR}.statistic.csv

# Get local machine's status every 5 seconds
vmstat:
	vmstat 5

clean:
	rm -rf ${DIR}
