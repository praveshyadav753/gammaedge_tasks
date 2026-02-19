import asyncio
import time

async def say_after(delay, what):
    """A coroutine that waits a specified delay and then prints a message."""
    await asyncio.sleep(delay)  # Yields control to the event loop
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    # Create tasks and run them concurrently using asyncio.gather()
    await asyncio.gather(
        say_after(5, 'hello'),
        say_after(5, 'world')
    )

    print(f"finished at {time.strftime('%X')}")

# The entry point to run the asynchronous program
if __name__ == "__main__":
    asyncio.run(main())
