Tepkit Documentation
====================



.. raw:: html

   <p align="center">
     <img src="_static/logo.png" style="height:250px;">
   </p>
   <p align="center">
     <a href="https://pypi.org/project/tepkit/">
       <img src="https://img.shields.io/pypi/pyversions/tepkit.svg" alt="Python"></a>
     <a href="https://pypi.org/project/tepkit/">
       <img src="https://img.shields.io/pypi/v/tepkit.svg" alt="PyPI"></a>
   </p>

**Welcome to Tepkit Documentation!**

| GitHub Repository: https://github.com/TepLabCode/tepkit
| PyPI: https://pypi.org/project/tepkit/

.. note::
   The documentation is in the early stages and will be improved over time.

.. toctree::
   :hidden:

   Home <self>

.. toctree::
   :maxdepth: 1
   :caption: Introduction

   Overview <tutorials/overview>

.. toctree::
   :maxdepth: 1
   :caption: Tutorials

   Installation                  <tutorials/installation>
   Getting Started               <tutorials/getting_started>
   Work with thirdorder          <tutorials/work_with_thirdorder>
   Plotting Figures              <tutorials/plotting>
   How to Add Custom Functions   <tutorials/custom_functions>
   Adjust cutoff radius          <tutorials/adjust_cutoff_radius>
   Deformation Potential Theory  <autoapi/tepkit/formulas/dp/index>

.. toctree::
   :maxdepth: 1
   :caption: File API

   Overview                 <file/_overview>
   VASP File Classes        <file/vasp_file_classes>
   BoltzTraP2 File Classes  <file/boltztrap2_file_classes>
   Phonopy File Classes     <file/phonopy_file_classes>
   ShengBTE File Classes    <file/shengbte_file_classes>

.. toctree::
   :maxdepth: 1
   :caption: API Reference

   Overview                 <others/api_reference_overview>
   autoapi/tepkit/core/index
   autoapi/tepkit/io/index
   autoapi/tepkit/utils/index
   autoapi/tepkit/formulas/index
