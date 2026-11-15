"""Assignment 4: A to-do list menu loop.

The loop reads commands with input_fn and writes answers with output_fn, so a
test can feed scripted commands and collect the output.
"""


def run_menu(input_fn=input, output_fn=print) -> list[str]:
    """Run the menu until "quit". Return the tasks that are left.

    Show the prompt "> " for every command: input_fn("> "). Commands (the
    first word is not case sensitive, extra spaces are ignored):

    add <text>   add a task and output "Added: <text>"
                 without text, output "Usage: add <text>"
    list         output "No tasks." if empty, otherwise one output per task,
                 numbered from 1: "1. buy milk"
    done <n>     remove task number n (counting from 1) and output "Done: <text>"
                 for a missing, non-numeric or out-of-range n, output "No such task."
    quit         output "Bye!" and stop
    anything else (not empty) output "Unknown command: <first word as typed>"
    empty line   do nothing

    If input_fn raises EOFError (no more input), act as if the user typed quit.
    """
    tasks: list[str] = []
    while True:
        try:
            line = input_fn("> ")
        except EOFError:
            line = "quit"
        words = line.split()
        if not words:
            continue
        command, rest = words[0].lower(), words[1:]
        match command:
            case "add":
                if rest:
                    text = " ".join(rest)
                    tasks.append(text)
                    output_fn(f"Added: {text}")
                else:
                    output_fn("Usage: add <text>")
            case "list":
                if not tasks:
                    output_fn("No tasks.")
                for number, task in enumerate(tasks, start=1):
                    output_fn(f"{number}. {task}")
            case "done":
                if len(rest) == 1 and rest[0].isdigit() and 1 <= int(rest[0]) <= len(tasks):
                    output_fn(f"Done: {tasks.pop(int(rest[0]) - 1)}")
                else:
                    output_fn("No such task.")
            case "quit":
                output_fn("Bye!")
                return tasks
            case _:
                output_fn(f"Unknown command: {words[0]}")


if __name__ == "__main__":
    run_menu()
