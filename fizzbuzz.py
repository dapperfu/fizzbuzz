#!/usr/bin/env python3

#print("Hello World")

for i in range(0,100):
	#print(i+1)
	if i%3:
		print(f"{i}: Fizz")
	if i%5:
		print("{i}: Buzz")
	if i%15:
		print("{i}: FizzBuzz")
