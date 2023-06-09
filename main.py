import typer
from typing import Optional
from pathlib import Path

app = typer.Typer()

@app.command('run')
def main(extension: str,
         directory: Optional[str] = typer.Argument(None, help="Directory where to look for"),
         delete: Optional[bool] = typer.Option(False, help="Delete founded files")):
    """
    Display founded files in the given extension
    """

    if directory:
        directory = Path(directory)
    else:
        directory = Path.cwd()

    if not directory.exists():
        typer.secho(f"Directory {directory} does not exist", fg=typer.colors.RED)
        raise typer.Exit()

    files = directory.rglob(f"*.{extension}")
    if delete:
        typer.confirm("Are you sure you want to delete ?", abort=True)
        for file in files:
            file.unlink()
            typer.secho(f"File {file} deleted.", fg=typer.colors.RED)
    else:
        typer.secho(f"Founded files with extension {extension}", bg=typer.colors.BLUE)
        for file in files:
            typer.echo(file)        

@app.command()
def search(extension: str):
    """
    Search for file with a given extension
    """
    main(extension=extension, directory=None, delete=False)


@app.command()
def delete(extension: str):
    """
    Delete file with a given extension
    """
    main(extension=extension, directory=None, delete=True)

if __name__ == "__main__":
    app()