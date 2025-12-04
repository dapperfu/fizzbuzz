

.PHONY: dev
dev:
	nano fizzbuzz.py && ./fizzbuzz.py && git add fizzbuzz.py && read -p "Press Enter to continue..." && git commit -a
