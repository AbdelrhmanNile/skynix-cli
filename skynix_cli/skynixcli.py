import typer
import os
import json
import shutil

cli = typer.Typer()

@cli.command()
def pull():
    typer.echo("Pulling from github")
    path = f"/home/{os.getlogin()}"
    repo = "https://github.com/AbdelrhmanNile/skynix.git"
    config = None
    
    if os.path.exists(f"{path}/skynix"):
        config = json.load(open(f"{path}/skynix/config.json"))
        shutil.rmtree(f"{path}/skynix")
    
    os.system(f"cd {path} && git clone {repo}")
    typer.echo("Done pulling")
    typer.echo("Installing requirements")
    os.system(f"cd {path}/skynix && pip3 install pipenv && pipenv install")
    os.system(f"cd {path}/skynix && pipenv --venv > {path}/skynix/venv.txt")
    with open(f"{path}/skynix/venv.txt", "r") as f:
        venv = f.read()
    
    if config != None:
        config["python"] = f"{venv.strip()}/bin/python"
    else:
        config = {"python": f"{venv.strip()}/bin/python",
                  "poe_token": "",
                  "openweathermap_token": ""}
        
    with open(f"{path}/skynix/config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
        
    typer.echo("Done installing requirements")
    typer.echo("#############################################")
    typer.echo("Please install xfce4-terminal and vlc if you don't have them on your system")
    

@cli.command()
def run():
    user = os.getlogin()
    config = json.load(open(f"/home/{user}/skynix/config.json"))
    python = config["python"]
    os.system(f"xfce4-terminal --drop-down -e '{python} -u '/home/{user}/skynix/main.py''")

@cli.command()
def config():
    os.system(f"nano /home/{os.getlogin()}/skynix/config.json")

if __name__ == "__main__":
    cli()
