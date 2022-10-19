from rich import print
from rich.prompt import Prompt


def run_CLI():
    from hangman_CLI.hangman import run

    run()



def run_GUI():
    from hangman_GUI import main


def select_app(retry=0):
    if retry < 3:
        app_type = Prompt.ask("Which of the hangman apps do you want to run?\n[1] CLI\n[2] GUI\n")
        if app_type == "1":
            print("CLI")
            run_CLI()
        elif app_type == "2":
            print("GUI")
            run_GUI()
        else:
            retry += 1
            return select_app(retry)
    else:
        print("[bold red]You have either entered an invalid response three times or an unexpected error has occurred.[/bold red] This program will now exit.")
        exit()

if __name__ == "__main__":
    select_app()
    
    