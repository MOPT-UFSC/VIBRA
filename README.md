<p align="center">
   <img src="https://github.com/MOPT-UFSC/VIBRA/blob/main/pics/VIBRA.png?raw=true" alt="VIBRA logo" width="200"/>


# Vibra

## Poetry commands
```
poetry install
```

```
poetry run python -m vibra
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

If you are using Windows, the following commands will only work on `cmd`, and not on `powershell`.
To make this work propperly on powershell too, you need to run
```
conda init powershell
```
And then restart the `powershell` window.

After environment generation, we can activate and run Vibra by running the following commands:
```
conda activate VIBRA
```

Finally, enter the following command to execute the application:
```
python -m vibra
```

If some package changed since the generation, the environment can be updated using the following command: 
```
conda env update --f environment.yml --prune
```

## Generate Installer
```
poetry run pyinstaller vibra.spec --noconfirm
ISCC.exe /O"dist" /F"vibra-setup" "vibra.iss"
```
