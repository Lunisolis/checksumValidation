import os
import hashlib
import typer
from pathlib import Path
from tqdm import tqdm
from colorama import Fore, Style
from datetime import datetime
import time

app = typer.Typer()

def generate_hashes(folder_path: str) -> dict:
    """Generate SHA512 hashes for all files in the specified folder."""
    hashes = {}
    # Use Path for more efficient path handling
    folder_path = Path(folder_path)

    # Check if it's a file or directory
    if folder_path.is_file():
        files = [folder_path]
    else:
        # Collect all files in the folder and subfolders
        files = list(folder_path.rglob('*'))
        files = [f for f in files if f.is_file()]

    # Generate hashes for each file
    for file_path in tqdm(files, desc="Generating hashes", unit="file", colour="green"):
        try:
            # Read file in chunks to handle large files efficiently
            hash_sha512 = hashlib.sha512()
            with open(file_path, 'rb') as f:
                # Read file in 64KB chunks
                for chunk in iter(lambda: f.read(65536), b''):
                    hash_sha512.update(chunk)
            hashes[str(file_path)] = hash_sha512.hexdigest()
        except IOError as e:
            typer.echo(f"{Fore.YELLOW}Warning: Could not read file {file_path}: {str(e)}{Style.RESET_ALL}")
    return hashes

def save_hashes_to_file(hashes: dict, output_file: str) -> None:
    """Save the generated hashes to a file with format HASH:filename."""
    try:
        with open(output_file, 'w') as f:
            for file_path, file_hash in sorted(hashes.items()):
                f.write(f"{file_hash}:{file_path}\n")
    except IOError as e:
        typer.echo(f"{Fore.RED}Error: Could not write to file {output_file}: {str(e)}{Style.RESET_ALL}")
        raise typer.TyperExit(code=1)


def display_cascading_gradient_red_blue():
    """Display the cascading gradient of red and blue ASCII art."""
    art = r"""
                 _________                                              ____   ____     ____  
______   ______ /   _____/  ____  _____     ____    ____    ____ _______\   \ /   /    /_   | 
\____ \ /  ___/ \_____  \ _/ ___\ \__  \   /    \  /    \ _/ __ \\_  __ \\   Y   /______|   | 
|  |_> >\___ \  /        \\  \___  / __ \_|   |  \|   |  \\  ___/ |  | \/ \     //_____/|   | 
|   __//____  >/_______  / \___  >(____  /|___|  /|___|  / \___  >|__|     \___/        |___| 
|__|        \/         \/      \/      \/      \/      \/      \/                             

    """
    # Create a cascading gradient effect by coloring different parts of the art
    # Create a cascading gradient effect by coloring different parts of the art
    colored_art = (
        f"{Fore.RED}                  _________                                               ____   ____     ____  \n"
        f"{Fore.RED} ______   ______ /   _____/  ____  _____     ____    ____    ____ ________\\   \\ /   /    /_   | \n"
        f"{Fore.YELLOW} \\____ \\ /  ___/ \\_____  \\ _/ ___\\ \\__  \\   /    \\  /    \\ _/ __ \\\\_   __ \\\\   Y   /______|   | \n"
        f"{Fore.BLUE} |  |_> >\\___ \\  /        \\\\  \\___  / __ \\_|   |  \\|   |  \\   ___/  |  | \\/ \\     //_____/|   | \n"
        f"{Fore.CYAN} |   __//____  >/_______  / \\___  >(____  /|___|  /|___|  / \\___  > |__|     \\___/        |___| \n"
        f"{Fore.MAGENTA} |__|        \\/         \\/      \\/      \\/      \\/      \\/      \\/                             \n"
        f"{Style.RESET_ALL}"
    )
    typer.echo(colored_art)

@app.command()
def generate_and_save_hashes(
    input_path: str = typer.Option(..., "-i", "--input", help="Input directory or file path"),
    output_file: str = typer.Option(..., "-o", "--output", help="Output file path to save hashes"),
) -> None:
    """Generate SHA512 hashes for files in the specified path and save to a file."""
    typer.echo(f"{Fore.CYAN}Generating hashes for files in {input_path}{Style.RESET_ALL}")

    # Check if input exists
    if not os.path.exists(input_path):
        typer.echo(f"{Fore.RED}Error: Path {input_path} does not exist{Style.RESET_ALL}")
        raise typer.TyperExit(code=1)

    # Generate timestamp for output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Append timestamp to the given output filename
    output_file = f"{output_file}_{timestamp}.txt"

    # Generate hashes
    start_time = time.time()
    hashes = generate_hashes(input_path)
    elapsed_time = time.time() - start_time

    typer.echo(f"{Fore.CYAN}Saving hashes to {output_file}{Style.RESET_ALL}")
    save_hashes_to_file(hashes, output_file)

    typer.echo(f"{Fore.GREEN}Hashes generated and saved to {output_file}{Style.RESET_ALL}")
    typer.echo(f"{Fore.BLUE}Processed {len(hashes)} files in {elapsed_time:.2f} seconds{Style.RESET_ALL}")

if __name__ == "__main__":
    display_cascading_gradient_red_blue()
    app()
