init:
	pip3 install -r requirements.txt

test:
	pytest tests

slow-test:
	pytest tests --runslow

clean: # clean the repository
	find . -name "__pycache__" | xargs  rm -rf
	find . -name "*pytest_cache" | xargs rm -rf
	find . -name "*.pyc" | xargs rm -rf
	find . -name ".eggs" | xargs rm -rf
	find . -name "build" | xargs rm -rf
	find . -name "dist" | xargs rm -rf
	find . -name "stockscore.egg-info" | xargs rm -rf

.PHONY: test init clean
