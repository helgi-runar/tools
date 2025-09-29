package main

import (
	"encoding/csv"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"
)

const (
	appData       = ".local/share/todo"
	todoFile      = "todo.csv"
	todoBackup    = "todo.csv.bak"
	timeLayout    = "2006-01-02 15:04:05"
	taskAgeYellow = 2 * 24 * time.Hour
	taskAgeRed    = 4 * 24 * time.Hour
)

// Task represents a task with description, creation and completion timestamps
type Task struct {
	Description        string
	CreationDatetime   time.Time
	CompletionDatetime time.Time
}

func main() {
	if len(os.Args) < 2 {
		listTasks(false)
		return
	}

	command := os.Args[1]
	switch command {
	case "l":
		all := len(os.Args) > 2 && os.Args[2] == "-a"
		listTasks(all)
	case "c":
		if len(os.Args) < 3 {
			fmt.Println("Usage: t c NUMBER")
			return
		}
		completeTask(os.Args[2])
		listTasks(true)
	case "r":
		if len(os.Args) < 3 {
			fmt.Println("Usage: t r NUMBER")
			return
		}
		removeTask(os.Args[2])
		listTasks(false)
	case "h":
		showHelp()
	case "a":
	default:
		if os.Args[1] == "a" && len(os.Args) < 3 {
			fmt.Println("Usage: t a DESCRIPTION")
			return
		} else if os.Args[1] == "a" && len(os.Args) > 2 {
			addTask(strings.Join(os.Args[2:], " "))
		} else {
			addTask(strings.Join(os.Args[1:], " "))
		}
		listTasks(false)
	}
}

func showHelp() {
	fmt.Println(`Task Manager Usage:

t a DESCRIPTION
	Add a new task with the specified DESCRIPTION.

t l [-a]
	List all tasks. Use the -a flag to include completed tasks.

t c NUMBER
	Mark the task with the specified NUMBER as completed.

t r NUMBER
	Remove the task with the specified NUMBER.

t h
	Show this help message.
`)
}

func getTodoPath() string {
	home, err := os.UserHomeDir()
	if err != nil {
		fmt.Println("Error: Unable to determine home directory.")
		os.Exit(1)
	}
	return filepath.Join(home, appData, todoFile)
}

func backupTodoFile() {
	src := getTodoPath()
	dst := getTodoPath() + ".bak"
	input, err := os.ReadFile(src)
	if err != nil {
		return
	}
	os.WriteFile(dst, input, 0644)
}

func readTasks() ([]Task, error) {
	filePath := getTodoPath()
	file, err := os.Open(filePath)
	if err != nil {
		if errors.Is(err, os.ErrNotExist) {
			return []Task{}, nil
		}
		return nil, err
	}
	defer file.Close()

	reader := csv.NewReader(file)
	rows, err := reader.ReadAll()
	if err != nil {
		return nil, err
	}

	tasks := []Task{}
	for _, row := range rows {
		creationTime, _ := time.Parse(timeLayout, row[1])
		completionTime, _ := time.Parse(timeLayout, row[2])
		tasks = append(tasks, Task{Description: row[0], CreationDatetime: creationTime, CompletionDatetime: completionTime})
	}
	return tasks, nil
}

func writeTasks(tasks []Task) error {
	filePath := getTodoPath()
	file, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	for _, task := range tasks {
		row := []string{task.Description, task.CreationDatetime.Format(timeLayout), task.CompletionDatetime.Format(timeLayout)}
		writer.Write(row)
	}
	return nil
}

func addTask(description string) {
	description = strings.TrimSpace(description)
	tasks, err := readTasks()
	if err != nil {
		fmt.Println("Error reading tasks:", err)
		return
	}

	tasks = append(tasks, Task{Description: description, CreationDatetime: time.Now(), CompletionDatetime: time.Date(1, time.January, 1, 0, 0, 0, 0, time.Now().Local().Location())})
	backupTodoFile()
	if err := writeTasks(tasks); err != nil {
		fmt.Println("Error writing tasks:", err)
	}
}

func listTasks(showAll bool) {
	tasks, err := readTasks()
	if err != nil {
		fmt.Println("Error reading tasks:", err)
		return
	}

	fmt.Println("\nTasks:")
	for i, task := range tasks {
		age := time.Since(task.CreationDatetime)
		color := ""
		if task.CompletionDatetime.Year() == 1 {
			if age > taskAgeRed {
				color = "\033[31m" // Red
			} else if age > taskAgeYellow {
				color = "\033[33m" // Yellow
			}
		} else if !showAll {
			continue
		}

		status := ""
		if task.CompletionDatetime.Year() != 1 {
			status = " (completed)"
			color = "\033[9m" // Strike-through
		}
		fmt.Printf("%s%d. %s%s%s\033[0m\n", color, i+1, task.Description, status, color)
	}
	fmt.Print("\n\n")
}

func completeTask(number string) {
	tasks, err := readTasks()
	if err != nil {
		fmt.Println("Error reading tasks:", err)
		return
	}

	n, err := strconv.Atoi(number)
	if err != nil || n < 1 || n > len(tasks) {
		fmt.Println("Invalid task number.")
		return
	}

	tasks[n-1] = Task{tasks[n-1].Description, tasks[n-1].CreationDatetime, time.Now()}
	backupTodoFile()
	if err := writeTasks(tasks); err != nil {
		fmt.Println("Error writing tasks:", err)
	}
}

func removeTask(number string) {
	tasks, err := readTasks()
	if err != nil {
		fmt.Println("Error reading tasks:", err)
		return
	}

	n, err := strconv.Atoi(number)
	if err != nil || n < 1 || n > len(tasks) {
		fmt.Println("Invalid task number.")
		return
	}

	tasks = append(tasks[:n-1], tasks[n:]...)
	backupTodoFile()
	if err := writeTasks(tasks); err != nil {
		fmt.Println("Error writing tasks:", err)
	}
}
