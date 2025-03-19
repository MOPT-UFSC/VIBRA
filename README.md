<p align="center">
   <img src="https://github.com/MOPT-UFSC/VIBRA/blob/main/pics/VIBRA.png?raw=true" alt="VIBRA logo" width="200"/>


# Vibra

## Poetry commands
```
poetry install
```

```
poetry run python vibra
```

```
poetry run pytest
```

```
poetry run black
```
## Conda environment
To enable MUMPS solver in Vibra we need to use conda instead of poetry.
To generate the conda environment, just run:
```
conda env create -f environment.yml
```

## Generate Installer
```
poetry run pyinstaller vibra.spec --noconfirm
ISCC.exe /O"dist" /F"vibra-setup" "vibra.iss"
```