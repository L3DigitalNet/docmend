# Project Tasks

<!--
Purpose:
- This document is the user-visible task list and agent-visible project queue.

Instructions for AI agents:
- Do not add tasks to the `## User tasks` section.
- Do add tasks to the `## Agent tasks` section. Include all open work from agent-managed handoff documents.
- Use `- [ ]` to indicate open work and `- [x]` for work completed during the current session.
- Remove completed standalone agent tasks after recording their outcomes in `docs/STATUS.md`.
-->

## User tasks

- [ ] Explore bounded Go utilities, including a worker-pool utility where justified. The docmend product remains Python:

````markdown
For a standalone utility that processes many files efficiently, use a **Worker Pool** pattern. Do not treat this example as a docmend product-migration design. Instead of spawning one million goroutines at once (which could overwhelm OS file descriptors or memory), spawn a fixed number of "workers" (e.g., 100) that constantly pull file paths from a queue until the queue is empty.

Here are the three core pieces that make this work:

1. **The Jobs Channel (`chan string`):** This acts as a thread-safe queue. You push file paths into it, and the workers pull paths out of it.
2. **The WaitGroup (`sync.WaitGroup`):** This acts as a counter. It tells the main program to pause and wait until every single worker has finished its job. Without this, your program would exit immediately before the workers get a chance to run.
3. **The Workers:** These are lightweight goroutines running an infinite loop. They pull a file path from the channel, process it, and go back for another one. When the channel is closed, the loop automatically breaks.

Here is a complete, runnable example of this pattern:

```go
package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

// 1. The Worker Function
// It takes the channel of file paths and the WaitGroup pointer
func fileProcessor(workerID int, jobs <-chan string, wg *sync.WaitGroup) {
	// Ensure we tell the WaitGroup we are done when this function exits
	defer wg.Done()

	// This loop pulls from the channel until the channel is closed
	for filePath := range jobs {
		fmt.Printf("Worker %d picked up: %s\n", workerID, filePath)

		// ---------------------------------------------------------
		// YOUR LOGIC GOES HERE:
		// 1. Open the file (os.Open)
		// 2. Parse it (bufio.Scanner, goquery, or goldmark)
		// 3. Write the manipulated data to a new file
		// ---------------------------------------------------------

		// Simulating the time it takes to read/write a file
		time.Sleep(time.Millisecond * time.Duration(rand.Intn(300)))

		fmt.Printf("Worker %d finished: %s\n", workerID, filePath)
	}
}

func main() {
	// A mock list of files you might get from scanning a directory using filepath.WalkDir
	filesToProcess := []string{
		"index.html", "about.html", "readme.md",
		"data1.txt", "data2.txt", "contact.html",
	}

	// Create a buffered channel to hold our file paths
	jobs := make(chan string, len(filesToProcess))
	var wg sync.WaitGroup

	// Determine how many concurrent workers to run.
	// For CPU/Disk heavy tasks, runtime.NumCPU() is a good starting point.
	numWorkers := 3

	fmt.Println("Starting workers...")

	// 2. Spin up the workers
	for w := 1; w <= numWorkers; w++ {
		wg.Add(1) // Increment the WaitGroup counter for each worker we start
		go fileProcessor(w, jobs, &wg)
	}

	// 3. Load up the queue
	// We send all the file paths into the jobs channel
	for _, file := range filesToProcess {
		jobs <- file
	}

	// Close the channel. This tells the workers "no more files are coming."
	// It does NOT destroy the channel; workers will finish pulling remaining items.
	close(jobs)

	// 4. Wait for completion
	// The main function blocks here until wg.Done() is called enough times
	// to bring the WaitGroup counter back down to zero.
	wg.Wait()

	fmt.Println("All files processed successfully!")
}

```

### Pro-Tips for your specific use case:

- **How many workers?** If you are reading/writing from an SSD, try `100` to `500` workers. If you push it too high, your OS will complain about having too many open files.
- **Handling Errors:** In a real-world scenario, you will want a second channel (e.g., `results chan error`) so workers can send back errors if a file fails to read or write. Your main function can then log those errors without stopping the rest of the pool.
- **Finding the files:** You will want to use Go's `filepath.WalkDir` in the main function to rapidly scan your directory structure and feed those found paths directly into the `jobs` channel.
````

## Agent tasks

- [ ] Support the owner's first staged real-library rollout under spec section 18.4.

  Scan read-only, review the plan and skip pile, apply a filtered subset, then widen. Expand the weird-document corpus only through the adr-0015 re-synthesis procedure so no real library bytes or paths enter this public repository.
