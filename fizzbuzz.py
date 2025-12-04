#!/usr/bin/env python3

for i in range(1,101):
	print(i+1)
	if i%3==0:
		print(f"{i}: Fizz i/3={i/3:.5f}")
	if i%5==0:
		print(f"{i}: Buzz i/5={i/5:.5f}")
	if i%15==0:
		print(f"{i}: FizzBuzz i=15/{i/15:5f}")
