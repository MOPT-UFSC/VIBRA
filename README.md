<p align="center">
   <img src="https://media.githubusercontent.com/media/MOPT-UFSC/molde/main/data/vibra/png/vibra_colored_other_background.png" alt="VIBRA logo" width="500"/>

<a href="https://doi.org/10.5281/zenodo.20936528"><img src="https://zenodo.org/badge/662679851.svg" alt="DOI"></a>

# Vibra: Vibroacoustic Analysis using FEM
*v0.6.1 Aug 2026*

Vibra is an open-source software developed in Python for modeling vibroacoustic problems using the Finite Element Method (FEM). In its current version, the software has been validated for performing modal analysis, complex modal analysis, and time-harmonic analysis of linear acoustic problems. Built-in support for Gmsh functions enables the generation of high-quality meshes, ensuring continuity between regions and allowing for local refinements. Typical acoustic boundary conditions—Dirichlet, Neumann, and Robin—are implemented, as well as transfer impedance conditions between media, which can be used, for example, to model perforated panels. Porous material models are also available, including Delany-Bazley, Delany-Bazley-Miki, JCA, and JCAL. The software is integrated with the NIST REPROP library, which can be adopted for determining the properties of working fluid mixtures (if you use this feature, you need a license from NIST). The acoustic analyses are validated through comparisons with commercial softwares. VIBRA already includes structural elements (solid and DKT plate), but the structural analysis is still under validation. In our upcoming versions, we will have the structural analysis validated and also include fluid–structure interaction analyses.

<p align="center">
   <img src="https://github.com/MOPT-UFSC/VIBRA/blob/main/pics/275Hz.gif?raw=true" alt="FILTRO gif" width="900"/>

*What's new?*

- Optimized solvers for harmonic and modal analysis.
- Complete set of boundary conditions for 3D acoustic analysis.
- Acoustic transfer admittance model for representing complex devices as equivalent models.
- Perforate plate transfer admittance model.
- Viscothermal loss models.
- Porous materials models (rigid porous materials, equivalent properties).
- New interface and visualization tools (enhanced symbols for boundary condition, excitation, etc).
- Project file management improvements: structural and acoustic results can now be saved and retrieved.
- Enhanced animation of results (real and imaginary parts, phase monitoring, etc).

## Instalation

To install the latest stable version of VIBRA, go to the Releases page on GitHub:

https://github.com/MOPT-UFSC/VIBRA/releases

Then:

- Select the most recent release.

- Download the executable file for your operating system.

- Extract the files (if needed) and run the installation setup (.exe).

That’s it! VIBRA is now ready to use.

## Documentation

- The theoretical background for the acoustic formulation implemented in Vibra is based on classic and new FE books. Example: [Finite Element and Boundary Methods in Structural Acoustics and Vibration, by Noureddine Atalla and Franck Sgard](https://www.taylorfrancis.com/books/mono/10.1201/b18366/finite-element-boundary-methods-structural-acoustics-vibration-noureddine-atalla-franck-sgard).
- The structural elemements are implemented based on the books: [The Finite Element Method: Linear Static and Dynamic Finite Element Analysis, by Thomas Hughes](https://books.google.com.br/books?id=cHH2n_qBK0IC), [The Finite Element Method: Its Basis and Fundamentals, by O.C. Zienkiewicz, R.L. Taylor and J.Z. Zhu](https://www.sciencedirect.com/book/9781856176330/the-finite-element-method-its-basis-and-fundamentals), and [Structural Analysis with the Finite Element Method. Linear Statics.
Volume 2: Beams, Plates and Shells, by Eugenio Oñate](https://link.springer.com/book/10.1007/978-1-4020-8743-1).
 
- Examples of application: [MOPT YouTube Playlist](https://www.youtube.com/playlist?list=PLg6O6BGMOmkfDxR0atlMMUncDrxqOLwbT).
  
## Questions
If you have any questions you can open a new issue with the tag 'question'.

## Authors

The authors are members of [MOPT - Multidisciplinary Modeling and Optimization](https://mopt.paginas.ufsc.br/), from Federal University of Santa Catarina (Florianópolis, SC, Brazil).

   - [Andre F. Fernandes](https://www.linkedin.com/in/andrefpf/) - Computer Scientist; 
   - [Olavo M. Silva](https://www.linkedin.com/in/olavo-m-silva-5822a5151/) - Engineer;
   - [Jacson G. Vargas](https://www.linkedin.com/in/jacson-gil-vargas-a54b0768/) - Engineer;
   - [Vitor Slongo](https://www.linkedin.com/in/vitor-slongo-45298a270/) - Mesh and Geometry Specialist;
   - [Rodrigo Schwartz](https://www.linkedin.com/in/rodrigo-schwartz-249308244/) - Computer Scientist;
   - [Vinícius H. Ribeiro](http://linkedin.com/in/vin%C3%ADcius-henrique-ribeiro-385b67218) - Computer Scientist;
   - [Guilherme Pierri](https://www.linkedin.com/in/guilherme-pierri-4487a4271/) - Computer Scientist;
   - [Gustavo Martins](https://www.linkedin.com/in/gustavo-martins/) - Engineer and Data Scientist;   
   - [Gildean Almeida](https://www.linkedin.com/in/gildean-almeida-708862298/) - Validation;
   - [Leonardo R. Galibern](https://www.linkedin.com/in/leonardo-rosa-galibern-04a1b2304/) - Plate Elements;
   - [Taiana Barbosa Farias](https://www.linkedin.com/in/taiana-barbosa-farias-82740339a/) - Front-end.

## Citation

```bibtex
@software{vibra_software,
  title         = {MOPT-UFSC/VIBRA: 0.5.3},
  author        = {Jacson Gil Vargas and Olavo M. Silva and Andr\'{e} Fernandes and Vitor Voigt Slongo and Rodrigo Schwartz and Vinicius Henrique Ribeiro and Guilherme Pierri and Gildean Almeida and Taiana Barbosa Farias and Danilo Espindola and Gustavo Martins},
  year          = 2026,
  month         = jun,
  publisher     = {Zenodo},
  doi           = {10.5281/zenodo.20936529},
  url           = {https://doi.org/10.5281/zenodo.20936529},
  version       = {v0.5.3}
}
```

<p align="center">
   <img src="https://github.com/MOPT-UFSC/VIBRA/blob/main/pics/MOPT4.PNG?raw=true" alt="MOPT logo" width="1100"/>
