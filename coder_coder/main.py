import json
import math
import os
import time
from pathlib import Path
from typing import Optional

import typer

import openai
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / "env" /".env")
openai.api_key = os.environ["OPENAI_API_KEY"]  # supply your API key however you choose
openai.organization = os.environ["OPENAI_ORG_ID"]  # supply your organization key however you choose


app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome Portal Gun
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
    completion = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
    text_response = completion.choices[0].message.content
    typer.echo(text_response)
    if out_file:
        with open(out_file, "w") as f:
            f.write(text_response)


@app.command()
def plan(user_prompt: str = typer.Argument(...),
         out_file: Optional[str] = typer.Option(None)):
    prompt = f"""
Develop a plan for the following goal: {user_prompt}
"""
    completion = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
    text_response = completion.choices[0].message.content
    typer.echo(text_response)
    if out_file:
        with open(out_file, "w") as f:
            f.write(text_response)


@app.command()
def prompt(user_prompt: str = typer.Argument(...),
         out_file: Optional[str] = typer.Option(None)):
    completion = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": user_prompt}])
    text_response = completion.choices[0].message.content
    typer.echo(text_response)
    if out_file:
        with open(out_file, "w") as f:
            f.write(text_response)
