
.PHONY: dev
dev:
	nano fizzbuzz.py && ./fizzbuzz.py > output.txt && cat output.txt && git add . && read -p "Press Enter to continue..." dummy && git commit -a
