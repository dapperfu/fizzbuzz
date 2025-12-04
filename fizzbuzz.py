#!/usr/bin/env python3

#print("Hello World")

for i in range(1,101):
	print(i+1)
	if i%3==0:
		print(f"{i}: Fizz i/3={i/3}")
	if i%5==0:
		print(f"{i}: Buzz i/5={i/5}")
	if i%15==0:
		print(f"{i}: FizzBuzz i=15/{i/15}")
