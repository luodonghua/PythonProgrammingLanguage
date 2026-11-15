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
    # TODO: a while True loop. Read a line (catch EOFError), split it into words,
    # then use match on the first word.
    ...


if __name__ == "__main__":
    run_menu()
