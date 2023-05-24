import json
from pathlib import Path
from textwrap import dedent
from typing import Optional

import typer

import openai

coder_env = Path.home() / ".coder_code"
if not coder_env.exists():
    coder_env.mkdir()


def load_config():
    config_file = coder_env / "config.json"
    if config_file.exists():
        with open(config_file, "r") as f:
            config = json.load(f)
    else:
        config = {"text_model": "gpt-4"}
    return config

def save_config(config):
    config_file = coder_env / "config.json"
    with open(config_file, "w") as f:
        json.dump(config, f)


CONFIG = load_config()
openai.api_key = CONFIG.get("OPENAI_API_KEY")
openai.organization = CONFIG.get("OPENAI_ORG_ID")

app = typer.Typer()


@app.callback()
def callback():
    """
    Coder Coder
    """


@app.command()
def code(user_prompt: str = typer.Argument(...),
         out_file: Optional[str] = typer.Option(None),
         in_file: Optional[str] = typer.Option(None)):
    """
    code
    """
    typer.echo(f"Coding: {user_prompt}")
    if in_file:
        with open(in_file, "r") as f:
            existing_code = f.read()
        prompt = f"""Given this existing code {existing_code}. Write code to {user_prompt}. 
        Use or rewrite the existing code in a logical way without losing any of the functionality of the existing code.
         Output code only. No description."""
    else:
        prompt = f"Write code to {user_prompt}. Output the code only. No description."
    completion = openai.ChatCompletion.create(model=CONFIG["text_model"], messages=[{"role": "user", "content": prompt}])
    text_response = completion.choices[0].message.content
    typer.echo(text_response)
    if out_file:
        with open(out_file, "w") as f:
            f.write(text_response)


@app.command()
def document(in_file: Optional[str] = typer.Argument(...)):
    typer.echo(f"Documenting: {in_file}")
    prompt = f"""Write documentation for the following code: {in_file}"""
    completion = openai.ChatCompletion.create(model=CONFIG["text_model"], messages=[{"role": "user", "content": prompt}])
    text_response = completion.choices[0].message.content
    typer.echo(text_response)


@app.command()
def plan(user_prompt: str = typer.Argument(...),
         out_file: Optional[str] = typer.Option(None)):
    typer.echo(f"Planning: {user_prompt}")
    prompt = dedent(f"""
    Develop a plan for the following goal: {user_prompt}
    """)
    completion = openai.ChatCompletion.create(model=CONFIG["text_model"], messages=[{"role": "user", "content": prompt}])
    text_response = completion.choices[0].message.content
    typer.echo(text_response)
    if out_file:
        with open(out_file, "w") as f:
            f.write(text_response)


@app.command()
def prompt(user_prompt: str = typer.Argument(...),
         out_file: Optional[str] = typer.Option(None)):
    typer.echo(f"Prompting: {user_prompt}")
    completion = openai.ChatCompletion.create(model=CONFIG["text_model"], messages=[{"role": "user", "content": user_prompt}])
    text_response = completion.choices[0].message.content
    typer.echo(text_response)
    if out_file:
        with open(out_file, "w") as f:
            f.write(text_response)


@app.command()
def set_config(key: str = typer.Argument(...),
               value: str = typer.Argument(...)):
    CONFIG[key] = value
    save_config(CONFIG)


@app.command()
def get_config(key: str = typer.Option(default=None)):
    if key is not None:
        typer.echo(CONFIG[key])
    else:
        typer.echo(CONFIG)
