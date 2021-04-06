.PHONY: deploy_pkg
deploy_pkg:
	./venv_deploy/bin/python setup.py clean --all bdist_wheel clean --all
