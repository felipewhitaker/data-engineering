# Makefile
.ONESHELL:

# default when `make` is called
all: venv install run

# clean and run `all`
clearrun: clean all

# create `venv`
venv:
	: # Create venv if it doesn't exist
	: # test -d .venv || virtualenv -p python3 --no-site-packages venv
	test -d .venv || python3 -m venv .venv

# activate and install requirements in `venv`
install: venv
	: # Activate .venv and install something inside
	source .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	: # Other commands here

# run `scripts`
run:
	: # Run your app here, e.g
	: # determine if we are in venv,
	: # see https://stackoverflow.com/q/1871549
	. .venv/bin/activate && pip -V

# : # Or see @wizurd's answer to exec multiple commands
# . .venv/bin/activate && (\
# 	python3 -c 'import sys; print(sys.prefix)'; \
# 	pip3 -V \
# )

# delete `venv`
clean:
	rm -rf .venv