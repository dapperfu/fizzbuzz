#!/usr/bin/env python3

#print("Hello World")

for i in range(1,101):
	print(i+1)
	if i%3==0:
		print(f"{i}: Fizz")
	if i%5==0:
		print(f"{i}: Buzz")
	if i%15==0:
		print(f"{i}: FizzBuzz")
