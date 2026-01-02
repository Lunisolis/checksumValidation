
import typer
from tqdm import tqdm
from colorama import Fore, Style

app = typer.Typer()

def read_hash_file(file_path: str) -> dict:
    """Read a hash file and return a dictionary of file paths and their hashes."""
    hashes = {}
    format_error_count = 0
    try:
        with open(file_path, 'r') as f:
            with tqdm(total=sum(1 for _ in open(file_path)), desc=f"Reading {file_path}", unit="line", colour="green") as pbar:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:  # Skip empty lines
                        pbar.update(1)
                        continue

                    # Check for proper format: HASH:filepath
                    if ':' not in line:
                        format_error_count += 1
                        mismatch_during_completion()
                        typer.echo(f"{Fore.RED}Error: Invalid line format at line {line_num}: {line}")
                        mismatch_during_completion()
                        pbar.update(1)
                        continue

                    parts = line.split(':', 1)
                    if len(parts) != 2:
                        format_error_count += 1
                        mismatch_during_completion()
                        typer.echo(f"{Fore.RED}Error: Invalid line format at line {line_num}: {line}")
                        mismatch_during_completion()
                        pbar.update(1)
                        continue

                    file_hash, file_path = parts
                    if not file_hash or not file_path:
                        format_error_count += 1
                        mismatch_during_completion()
                        typer.echo(f"{Fore.RED}Error: Invalid line format at line {line_num}: {line}")
                        mismatch_during_completion()
                        pbar.update(1)
                        continue

                    # Store the hash and file path
                    if file_path not in hashes:
                        hashes[file_path] = file_hash
                    else:
                        mismatch_during_completion()
                        typer.echo(f"{Fore.YELLOW}Warning: Duplicate entry for file at line {line_num}: {file_path}")
                        mismatch_during_completion()

                    pbar.update(1)

        return hashes, format_error_count
    except FileNotFoundError:
        typer.echo(f"Error: File not found - {file_path}")
        return {}, 0
    except Exception as e:
        typer.echo(f"Error reading file {file_path}: {str(e)}")
        return {}, 0

def compare_hashes(old_file_path: str, new_file_path: str):
    """Compare hashes from two files and display appropriate ASCII art."""
    typer.echo("{Fore.CYAN}\nReading hash files...\n")
    hashes1, old_format_errors = read_hash_file(old_file_path)
    hashes2, new_format_errors = read_hash_file(new_file_path)

    if not hashes1 or not hashes2:
        return

    # Get all unique file names from both files
    all_files = set(hashes1.keys()).union(set(hashes2.keys()))

    # Initialize counters
    match_count = 0
    mismatch_count = 0
    unique_to_old_count = 0
    unique_to_new_count = 0



    # Create a progress bar for the comparison
    with tqdm(total=len(all_files), desc="Comparing files", unit="file", colour="yellow") as pbar:
        for file_path in all_files:
            if file_path in hashes1 and file_path in hashes2:
                if hashes1[file_path] == hashes2[file_path]:
                    match_count += 1
                else:
                    mismatch_count += 1
                    typer.echo(f"{Fore.RED}  Hash mismatch for file: {file_path}\n")
                    typer.echo(f"{Fore.CYAN}  Hash in older file: {hashes1[file_path]}\n")
                    typer.echo(f"{Fore.YELLOW}  Hash in newer file: {hashes2[file_path]}\n")
                    f"{Style.RESET_ALL}"
                    display_hash_mismatch_warning()
            elif file_path in hashes1:
                unique_to_old_count += 1
                typer.echo(f"{Fore.CYAN}File only recorded in older file:  \n")
                f"{Style.RESET_ALL}"
                typer.echo(f"{file_path} (hash: {hashes1[file_path]})")
                mismatch_during_completion()
            else:
                unique_to_new_count += 1
                typer.echo(f"{Fore.CYAN}File only recorded in new file:  \n")
                f"{Style.RESET_ALL}"
                typer.echo(f"{file_path} (hash: {hashes2[file_path]}) \n")
                mismatch_during_completion()
                display_name_mismatch_warning()

            pbar.update(1)

    # Display summary
    typer.echo("\nComparison Summary:")
    typer.echo(f"- Matching files: {match_count}")
    typer.echo(f"- Hash mismatches: {mismatch_count}")
    typer.echo(f"- File(s) only in older file: {unique_to_old_count}")
    typer.echo(f"- File(s) only in newer file: {unique_to_new_count}")
    if not hashes1 or not hashes2:
        typer.echo("Format errors detected in one or both files.")
        return
    # If no mismatches were found
    if mismatch_count == 0 and unique_to_old_count == 0 and unique_to_new_count == 0:
        display_successful_completion()
        typer.echo("All files match between the two sources!")
    elif mismatch_count == 0 and unique_to_new_count !=0:
        typer.echo("New file(s) present since the baseline scan was performed. See the output above to identify it/them by name.")
    elif mismatch_count == 0 and unique_to_old_count != 0:
        typer.echo("Old file(s) moved/deleted since the baseline scan was performed. See the output above to identify it/them by name.")
    elif mismatch_count == 0 and unique_to_old_count != 0 and unique_to_new_count !=0:
        typer.echo("The above file(s) has/have been added/removed since the baseline scan was performed. See the output above to identify it/them by name.")






def display_cascading_gradient_red_blue():
    """Display the cascading gradient of red and blue ASCII art."""
    art = r"""
               ____   ____        .__   .__     .___         __                ____   ____     ____
______   ______\   \ /   /_____   |  |  |__|  __| _/_____  _/  |_  ____ _______\   \ /   /    /_   |
\____ \ /  ___/ \   Y   / \__  \  |  |  |  | / __ | \__  \ \   __\/  _ \\_  __ \\   Y   /______|   |
|  |_> >\___ \   \     /   / __ \_|  |__|  |/ /_/ |  / __ \_|  | (  <_> )|  | \/ \     //_____/|   |
|   __//____  >   \___/   (____  /|____/|__|\____ | (____  /|__|  \____/ |__|     \___/        |___|
|__|        \/                 \/                \/      \/                                          

    """
    # Create a cascading gradient effect by coloring different parts of the art
    colored_art = (
        f"{Fore.RED}               ___   ____         .__   .__     .___         __                 ___   ____     ____\n"
        f"{Fore.RED} _____    _____\\  \\ /   / _____   |  |  |__|  __| _/_____ __/  |_   ____ _______\\   \\/   /    /_   |\n"
        f"{Fore.YELLOW} \\ __  \\ /  ___/\\  Y   / \\ __  \\  |  |  |  | / __ |\\ __  \\\\_    _\\ /  _ \\\\_  __ \\\\  Y   /______|   |\n"
        f"{Fore.BLUE} |  |_> >\\___ \\  \\    /    / __ \\ |  |__|  |/ /_/ |  / __ \\ |  |  (  <_> )|  | \\/ \\    //_____/|   |\n"
        f"{Fore.CYAN} |   __/ /____  > \\ _/    (____  /|____/|__|\\____ | (____  /|__|   \\____/ |__|     \\__/        |___|\n"
        f"{Fore.MAGENTA} |__|         \\/               \\/                \\/      \\/                                           \n"
        f"{Style.RESET_ALL}"
    )
    typer.echo(colored_art)

def display_name_mismatch_warning():
    """Display the name mismatch warning ASCII art in light orange/light yellow."""
    art = r"""
                                          .__                       __         .__      
  ____ _____    _____   ____        _____ |__| ______ _____ _____ _/  |_  ____ |  |__   
 /    \\__  \  /     \_/ __ \      /     \|  |/  ___//     \\__  \\   __\/ ___\|  |  \  
|   |  \/ __ \|  Y Y  \  ___/     |  Y Y  \  |\___ \|  Y Y  \/ __ \|  | \  \___|   Y  \ 
|___|  (____  /__|_|  /\___  >____|__|_|  /__/____  >__|_|  (____  /__|  \___  >___|  / 
     \/     \/      \/     \/_____/     \/        \/      \/     \/          \/     \/  
                                                                                        
    """
    # Light orange/light yellow color
    colored_art = (
        f"{Fore.LIGHTYELLOW_EX}                                             .__                          __         .__\n"
        f"{Fore.LIGHTYELLOW_EX}   ____ ____     ____    ___          _____  |__|  _____   _____ _____  _/  |_  ____ |  |__\n"
        f"{Fore.LIGHTYELLOW_EX}  /    \\\\__ \\   /    \\ _/ __\\        /     \\ |  | /  ___/ /     \\\\__  \\\\    __\\/ ___\\|  |  \\\n"
        f"{Fore.LIGHTYELLOW_EX} |   |  \\/ __\\_|  Y Y \\\\ ___/        |  Y Y \\|  | \\___  \\ |  Y Y \\/ __ \\|  |   \\  \\__|   Y  \\\n"
        f"{Fore.LIGHTYELLOW_EX} |___|  (____  /__|_|  /\\___  >______|__|_| /|__|/____  > |__|_|  (____  /__|   \\__  >___|  /\n"
        f"{Fore.LIGHTYELLOW_EX}      \\/     \\/      \\/     \\//_____/     \\/          \\/        \\/     \\/          \\/     \\/\n"
        f"{Style.RESET_ALL}"
    )
    typer.echo(colored_art)


def display_hash_mismatch_warning():
    """Display the hash mismatch warning ASCII art in dark orange/red."""
    art = r"""
.__                  .__                   .__                       __         .__      
|  |__ _____    _____| o |__          _____ |__| ______ _____ _____ _/  |_  ____ |  |__   
|  |  \\__  \  /  ___/  |  \        /     \|  |/  ___//     \\__  \\   __\/ ___\|  |  \  
|   Y  \/ __ \_\___ \|   Y  \      |  Y Y  \  |\___ \|  Y Y  \/ __ \|  | \  \___|   Y  \ 
|___|  (____  /____  >___|  /______|__|_|  /__/____  >__|_|  (____  /__|  \___  >___|  / 
     \/     \/     \/     \//_____/     \/        \/      \/     \/          \/      \/  
                                                                                       
    """
    # Dark orange/red color
    colored_art = (
        f"{Fore.LIGHTRED_EX}.__                   .__                    __                           __          .__ \n"
        f"{Fore.LIGHTRED_EX}|  |__ _____    ______|  |__         _____  |__|  ______  _____ ______  _/  |_  ____  |  |__\n"
        f"{Fore.LIGHTRED_EX}|  |  \\\\_   \\  /  ___/|  |  \\       /     \\ |  | /  ___/ /     \\\\__   \\\\    __\\/ ___\\ |  |  \\\n"
        f"{Fore.LIGHTRED_EX}|   Y  \\/ __ \\ \\___  \\|   Y  \\      |  Y Y \\|  | \\__   \\ |  Y Y  \\/ __ \\|  |   \\  \\___|   Y  \\\n"
        f"{Fore.LIGHTRED_EX}|___|  /(____  //____  >___|  /_____|__|_| /|__|/____  > |__|_|  (____  / __|   \\___  >___|  /\n"
        f"{Fore.LIGHTRED_EX}     \\/      \\/      \\/     \\//_____/    \\/          \\/        \\/     \\/            \\/     \\/\n"
        f"{Style.RESET_ALL}"
    )
    typer.echo(colored_art)

def display_successful_completion():
    """Display the successful completion ASCII art with no changes detected."""
    art = r"""
  _____ .__ .__                                         __           .__
_/ ____\|__||  |    ____    ______      _____  _____  _/  |_   ____  |  |__
\   __\ |  ||  |  _/ __ \  /  ___/     /     \ \__  \ \   __\_/ ___\ |  |  \
 |  |   |  ||  |__\  ___/  \___ \     |  Y Y  \ / __ \_|  |  \  \____|   Y  \
 |__|   |__||____/ \___  >/____  >    |__|_|  /(____  /|__|   \____   >__|  /
                       \/      \/           \/      \/             \/     \/

    """
    # Default color green(green coloring for success messages)
    colored_art = (
        f"{Fore.GREEN}  _____  .__ .__                                       __         .__\n"
        f"{Fore.GREEN}_/ ____\\ |__||  |    ____   ______     _____  _____  _/  |_  ____ |  |__\n"
        f"{Fore.GREEN}\\  __\\   |  ||  |  _/ __ \\ /  ___/    /     \\\\__   \\\\    __\\/ ___\\|  |  \\\n"
        f"{Fore.GREEN} |  |    |  ||  |__\\  ___/ \\__  \\     |  Y Y \\ / __ \\|  |   \\ \\___|   Y  \\\n"
        f"{Fore.GREEN} |__|    |__||____/ \\__  >/____  >    |__|_|  (____  / __|   \\____  >_|  /\n"
        f"{Fore.GREEN}                       \\/      \\/           \\/     \\/             \\/   \\/\n"
        f"{Style.RESET_ALL}"
    )
    typer.echo(colored_art)

def mismatch_during_completion():
    """Display the successful completion ASCII art with no changes detected."""

    art = r"""
____  ___               ____  ___               ____  ___               ____  ___               ____  ___ 
\   \/  /               \   \/  /               \   \/  /               \   \/  /               \   \/  / 
 \     /      ______     \     /      ______     \     /      ______     \     /      ______     \     /  
 /     \     /_____/     /     \     /_____/     /     \     /_____/     /     \     /_____/     /     \  
/___/\  \               /___/\  \               /___/\  \               /___/\  \               /___/\  \ 
      \_/                     \_/                     \_/                     \_/                     \_/ 
                                                                                                          
                                                                                             
                                                                                                          
	"""
                                                                                                          
    # Default color green(green coloring for success messages)
    colored_art = (
        f"{Fore.RED}____  ___               ____  ___               ____  ___               ____  ___               ____  ___ \n"
        f"{Fore.RED}\\   \\/  /               \\   \\/  /               \\   \\/  /               \\   \\/  /               \\   \\/  / \n"
        f"{Fore.RED} \\     /      ______     \\     /      ______     \\     /      ______     \\     /      ______     \\     /  \n"
        f"{Fore.RED} /     \\     /_____/     /     \\     /_____/     /     \\     /_____/     /     \\     /_____/     /     \\  \n"
        f"{Fore.RED}/___/\\  \\               /___/\\  \\               /___/\\  \\               /___/\\  \\               /___/\\  \\  \n"
        f"{Fore.RED}      \\_/                     \\_/                     \\_/                     \\_/                     \\_/ \n"
        f"{Style.RESET_ALL}"
    )
    typer.echo(colored_art)                                                                                                         
                                                                                                          
                                                                                                          

@app.command()
def main(
    old_file_path: str = typer.Option(..., "-o", "--old-file", help="Path to the old hash file"),
    new_file_path: str = typer.Option(..., "-n", "--new-file", help="Path to the new hash file")
):
    """Compare hashes from two files and display appropriate ASCII art."""
    typer.echo(f"Comparing hashes from {old_file_path} and {new_file_path}...\n")
    compare_hashes(old_file_path, new_file_path)

if __name__ == "__main__":
    display_cascading_gradient_red_blue()
    typer.echo("Use the -o flag to specify a baseline hash file, and the -n flag to specify the current hash file to compare them.")
    typer.echo("Keep libraries updated using pip update within your Venv")
    app()