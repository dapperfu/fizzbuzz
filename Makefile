
.PHONY: dev
dev:
	nano fizzbuzz.py && ./fizzbuzz.py && git add fizzbuzz.py && echo "10 seconds to analyze output" && sleep 5 && git commit -a
