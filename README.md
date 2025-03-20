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

Download and install the conda-forge ([conda-forge](https://conda-forge.org/download/)).
It is recommended to check the option *Add Miniforge3 to my PATH environment variable* in the program installation setup.
Once conda-forge was installed, it is possible to enable the MUMPS solver in Vibra. To enable this solver we need to use conda instead of poetry.
To generate the conda environment, just run:
```
conda env create -f environment.yml
```

After environment generation, we can activate and run Vibra by running the following commands:
```
conda activate VIBRA
```

Finally, enter the following command to execute the application:
```
conda run vibra
```

## Generate Installer
```
poetry run pyinstaller vibra.spec --noconfirm
ISCC.exe /O"dist" /F"vibra-setup" "vibra.iss"
```
