from cx_Freeze import setup, Executable

setup(
name = "Pollution data app",
version = "0.1",
description = "",
executables = [Executable("main.py")]
)