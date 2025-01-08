from cx_Freeze import setup, Executable # type: ignore

# Dependencies are automatically detected, but you can include/exclude specific modules.
build_options = {"packages": ["pygame"], "include_files": ["dino.png", "cactus.png"]}

setup(
    name="Dino Game",
    version="1.0",
    description="A fun dino jumping game",
    options={"build_exe": build_options},
    executables=[Executable("dino.py", base="Win32GUI")]
)
