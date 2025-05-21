<p align="center">
   <img src="https://github.com/MOPT-UFSC/VIBRA/blob/main/pics/Vibra_Logo.png?raw=true" alt="VIBRA logo" width="500"/>


# Vibra: Vibroacoustic Analysis using FEM

*V0.0.1 May 20th 2025*

Vibra is an open-source software developed in Python for modeling vibroacoustic problems using the Finite Element Method (FEM). In its current version, the software has been validated for performing modal analysis, complex modal analysis, and time-harmonic analysis of linear acoustic problems using linear tetrahedral finite elements (which do not suffer from locking in acoustic applications). Built-in support for Gmsh functions enables the generation of high-quality meshes, ensuring continuity between regions and allowing for local refinements. Typical acoustic boundary conditions—Dirichlet, Neumann, and Robin—are implemented, as well as transfer impedance conditions between media, which can be used, for example, to model perforated panels. Porous material models are also available, including Delany-Bazley, Delany-Bazley-Miki, JCA, and JCAL. The software is integrated with the REPROP library, which is essential for determining the properties of working fluid mixtures.

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
## Generate Installer
```
poetry run pyinstaller vibra.spec --noconfirm
ISCC.exe /O"dist" /F"vibra-setup" "vibra.iss"
```

## Authors

The authors are members of [MOPT - Multidisciplinary Modeling and Optimization](https://mopt.paginas.ufsc.br/), from Federal University of Santa Catarina (Florianópolis, SC, Brazil).

   - [Andre F. Fernandes](https://www.linkedin.com/in/andrefpf/) - Computer Scientist; 
   - [Olavo M. Silva](https://www.linkedin.com/in/olavo-m-silva-5822a5151/) - Engineer;
   - [Jacson G. Vargas](https://www.linkedin.com/in/jacson-gil-vargas-a54b0768/) - Engineer;
   - [Rodrigo Schwartz](https://www.linkedin.com/in/rodrigo-schwartz-249308244/) - Computer Scientist;
   - [Vinícius H. Ribeiro](http://linkedin.com/in/vin%C3%ADcius-henrique-ribeiro-385b67218) - Computer Scientist;
   - [Gustavo Martins](https://www.linkedin.com/in/gustavo-martins/) - Engineer and Data Scientist;
   - [Vitor Slongo](https://www.linkedin.com/in/vitor-slongo-45298a270/) - Mesh and Geometry Specialist;
   - [Gildean Almeida](https://www.linkedin.com/in/gildean-almeida-708862298/) - Validation;
   - [Leornardo R. Galibern](https://www.linkedin.com/in/leonardo-rosa-galibern-04a1b2304/) - Plate Elements.


<p align="center">
   <img src="https://github.com/MOPT-UFSC/VIBRA/blob/main/pics/MOPT4.PNG?raw=true" alt="MOPT logo" width="1100"/>

