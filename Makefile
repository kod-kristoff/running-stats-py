.PHONY: test clean clean-pyc lint lint-no-fail test-w-coverage

.DEFAULT: test

PYTHON = python3
PLATFORM := ${shell uname -o}
INVENV_PATH = ${shell which invenv}

${info Platform: ${PLATFORM}}
${info invenv: ${INVENV_PATH}}

ifeq (${VIRTUAL_ENV},)
  VENV_NAME = .venv
else
  VENV_NAME = ${VIRTUAL_ENV}
endif
${info Using ${VENV_NAME}}

VENV_BIN = ${VENV_NAME}/bin

ifeq (${INVENV_PATH},)
  INVENV = export VIRTUAL_ENV="${VENV_NAME}"; export PATH="${VENV_BIN}:${PATH}"; unset PYTHON_HOME;
else
  INVENV = invenv -C ${VENV_NAME}
endif

venv: ${VENV_NAME}/made

install: venv ${VENV_NAME}/req.installed
install-test: venv install ${VENV_NAME}/req-test.installed
install-dev: venv install-test ${VENV_NAME}/req-dev.installed

${VENV_NAME}/made:
	test -d ${VENV_NAME} || ${PYTHON} -m venv ${VENV_NAME}
	${INVENV} pip install --upgrade pip
	@touch $@

${VENV_NAME}/req.installed: requirements.txt
	${INVENV} pip install -Ur $<
	@touch $@

${VENV_NAME}/req-test.installed: setup.py setup.cfg
	${INVENV} pip install -e .[test]
	@touch $@

${VENV_NAME}/req-dev.installed: setup.py setup.cfg
	${INVENV} pip install -e .[dev]
	@touch $@

test: install-test clean-pyc
	${INVENV} pytest -vv tests/

test-w-coverage: install-test clean-pyc
	${INVENV} pytest -vv --cov-config=setup.cfg --cov=running_stats --cov-report=term-missing tests

lint: install-test
	${INVENV} pylint --rcfile .pylintrc running_stats tests

lint-no-fail: install-test
	${INVENV} pylint --rcfile .pylintrc --exit-zero running_stats tests

lint-syntax-errors: install-dev
	${INVENV} flake8 karp5_sb tests setup.py run.py cli.py --count --select=E9,F63,F7,F82 --show-source --statistics ${FLAKE8_FLAGS}
		
clean: clean-pyc
clean-pyc:
	find . -name '*.pyc' -exec rm --force {} \;

