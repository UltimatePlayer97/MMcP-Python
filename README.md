# MMcP - Make Minecraft Portable
A fork of https://github.com/NickGenghar/make_minecraft_portable, but made in Python!

Having trouble making your Minecraft installation more portable? This tool will help you achieve that and more! Make Minecraft Portable, MMcP for short, is a simple program to manage Minecraft in a friendlier, more portable method, allowing for advance features such as custom installations (called `instance`s), custom locations and others. Originally, this project was made in Windows Batch script (sadly lost the original) as a pet project. With this rewrite, it is now aimed to become friendlier towards the larger masses.

## Features
Currently, the following features are available:
- [Complete]: Launch the (official) Minecraft Launcher (logins are managed by the Minecraft Launcher, not MMcP).
- [Complete]: Create, modify and remove `instances`.
- [Planned]: Download and install community-created contents (resource packs, mods, shaders, etc.) via providers (Modrinth, CurseForge, etc.).
- [Planned]: Auto-launch Minecraft via MMcP.
- [Partial]: Export `instances` into a compressed archive to be imported into other third-party launchers ([Prism Launcher](https://prismlauncher.org/), [Modrinth App](https://modrinth.com/app), [CurseForge App](https://www.curseforge.com/download/app), etc.).
- And many more! (Send ideas by creating a feature request, pull/merge request, etc.).

## How To Build the Project
Prerequesteries:
 - Python 3, if you do not have it installed you may download it [here](https://www.python.org/downloads/)
 - Git (Optional, but very helpful if you want to contribute code.)

---
Use the green `Code` button around the middle top-right, choose your appropriate download method.

Alternatively, with `git`, `clone` the project to a working directory, then move into it.
```
git clone https://github.com/UltimatePlayer97/MMcP-Python.git

cd MMcP-Python
```
in the `MMcP-Python` folder, open up a command prompt directing to this folder and run `pip install -r requirements.txt`, this will ensure all the modules needed for this project are installed.

Once you have entered the project folder, go into the `src` folder and run the `main.py` file.

---
## Usage
For now, the program does not receives command-line input. Instead, it provides what's known as a _Terminal User Interface_, TUI for short. Using this TUI, the user then select
