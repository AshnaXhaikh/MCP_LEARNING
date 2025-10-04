from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two number and return the result."""
    return a * b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers and return the result."""
    return a - b

@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide two numbers and return the result."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

@mcp.tool()
def power(a: int, b: int) -> float:

    """Raise a to the power of b and return the result."""
    return a ** b

@mcp.tool()
def sqrt(a: int) -> float:
    """Return the square root of a number."""
    if a < 0:
        raise ValueError("Cannot take the square root of a negative number.")
    return a ** 0.5

@mcp.tool()
def log(a: float, base: float = 10) -> float:
    """Return the logarithm of a number with the specified base."""
    if a <= 0 or base <= 1:
        raise ValueError("Logarithm undefined for these values.")
    import math
    return math.log(a, base)

if __name__ == "__main__":
    # Change back to stdio. The client will handle launching the process 
    # and creating a streamable-http proxy to it automatically.
    mcp.run(transport="stdio") 

# if __name__ == "__main__":
#     # IMPORTANT: Do NOT specify host/port here. 
#     # The client will pass the necessary info when it launches the server.
#     mcp.run(transport="streamable-http") 