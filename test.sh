#! /bin/bash

echo "pytest..."
pytest stockscore/tests
rc=$?;

if [[ $rc != 0 ]]; then
	echo "Pytest failed."
	exit $rc
fi
echo "PASSED"

echo 'All tests passed!'
