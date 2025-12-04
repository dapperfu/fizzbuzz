#!/usr/bin/env python3

#print("Hello World")

for i in range(1,101):
	#print(i+1)
	if i%3:
		print(f"{i}: Fizz")
	if i%5:
		print(f"{i}: Buzz")
	if i%15:
		print(f"{i}: FizzBuzz")
