#! /bin/bash

python3 -m coverage run --source="../api,../utils" -m unittest discover .
pid=$!

# kill -0 -> doesn't send a signal, but returns exit status 0 if process exists else non-zero
while kill -0 $pid >/dev/null 2>&1; do
  echo "Process $pid is still running..."
  sleep 5
done

# output results
if [ ! -d "coverage_files" ]; then
  echo "coverage_files/ does not exist, creating directory ... "
  mkdir coverage_files
fi
resport_results=$(coverage report)
echo "$resport_results" > "coverage_files/$(date +%Y%m%d%H%M%S)--report.txt"
coverage annotate -d "coverage_files/"
echo ""
echo ""
echo "REPORT RESULTS"
echo "----------------"
echo ""
echo "${resport_results}"