def add(a, b):
	"""Return the sum of a and b."""
	return a + b


def is_even(n):
	"""Return True if n is even, False otherwise."""
	return n % 2 == 0


def factorial(n):
	"""Return n! for n >= 0. Raises ValueError for negative n."""
	if n < 0:
		raise ValueError("n must be >= 0")
	result = 1
	for i in range(2, n + 1):
		result *= i
	return result
