=====================
ShengBTE File Classes
=====================

Here are the classes for `ShengBTE <https://www.shengbte.org/>`_ files.

Input Files
===========

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Filename
     - Tepkit IO Class
   * - CONTROL
     - :doc:`Control </autoapi/tepkit/io/shengbte/Control>`
   * - FORCE_CONSTANTS_2ND
     - :doc:`ForceConstants </autoapi/tepkit/io/phonopy/ForceConstants>`
   * - FORCE_CONSTANTS_3RD
     - Not yet supported


Output Files
============

Root-dir Files
--------------
.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Filename
     - Tepkit IO Class
   * - BTE.cvVsT
     - :doc:`* TemperatureLengthFile </autoapi/tepkit/io/shengbte/TemperatureLengthFile>`
   * - BTE.dos
     - :doc:`* NticksLengthFile </autoapi/tepkit/io/shengbte/NticksLengthFile>`
   * - BTE.gruneisen
     - :doc:`* OmegaShapedFile </autoapi/tepkit/io/shengbte/OmegaShapedFile>`
   * - BTE.gruneisenVsT_total
     - :doc:`* TemperatureLengthFile </autoapi/tepkit/io/shengbte/TemperatureLengthFile>`
   * - BTE.KappaTensorVsT_CONV
     - :doc:`KappaTensorVsT </autoapi/tepkit/io/shengbte/KappaTensorVsT>`
   * - BTE.KappaTensorVsT_RTA
     - :doc:`KappaTensorVsT </autoapi/tepkit/io/shengbte/KappaTensorVsT>`
   * - BTE.KappaTensorVsT_sg
     - :doc:`KappaTensorVsT </autoapi/tepkit/io/shengbte/KappaTensorVsT>`
   * - BTE.omega
     - :doc:`Omega </autoapi/tepkit/io/shengbte/Omega>`
   * - BTE.P3
     - :doc:`* OmegaShapedFile </autoapi/tepkit/io/shengbte/OmegaShapedFile>`
   * - BTE.P3_minus
     - :doc:`* OmegaShapedFile </autoapi/tepkit/io/shengbte/OmegaShapedFile>`
   * - BTE.P3_minus_total
     - :doc:`* OmegaShapedFile </autoapi/tepkit/io/shengbte/OmegaShapedFile>`
   * - BTE.P3_plus
     - :doc:`* OmegaShapedFile </autoapi/tepkit/io/shengbte/OmegaShapedFile>`
   * - BTE.P3_plus_total
     - :doc:`* OmegaShapedFile </autoapi/tepkit/io/shengbte/OmegaShapedFile>`
   * - BTE.P3_total
     - :doc:`* OmegaShapedFile </autoapi/tepkit/io/shengbte/OmegaShapedFile>`
   * - BTE.pdos
     - :doc:`* NticksLengthFile </autoapi/tepkit/io/shengbte/NticksLengthFile>`
   * - BTE.qpoints
     - :doc:`* TableTextFile </autoapi/tepkit/io/TableTextFile>`
   * - BTE.qpoints_full
     - :doc:`* TableTextFile </autoapi/tepkit/io/TableTextFile>`
   * - BTE.ReciprocalLatticeVectors
     - :doc:`* TableTextFile </autoapi/tepkit/io/TableTextFile>`
   * - BTE.v
     - :doc:`V </autoapi/tepkit/io/shengbte/V>`
   * - BTE.v_full
     - :doc:`* TableTextFile </autoapi/tepkit/io/TableTextFile>`
   * - BTE.w_boundary
     - :doc:`W </autoapi/tepkit/io/shengbte/W>`
   * - BTE.w_isotopic
     - :doc:`W </autoapi/tepkit/io/shengbte/W>`

Temperature-dependent-subdir Files
----------------------------------

These files are located in the ``T*K`` subdirectories, such as ``T300K``.

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Filename
     - Tepkit IO Class
   * - BTE.cumulative_kappa_tensor
     - :doc:`CumulativeKappaTensor </autoapi/tepkit/io/shengbte/CumulativeKappaTensor>`
   * - BTE.cumulative_kappaVsOmega_tensor
     - :doc:`CumulativeKappaVsOmegaTensor </autoapi/tepkit/io/shengbte/CumulativeKappaVsOmegaTensor>`
   * - BTE.w
     - :doc:`W </autoapi/tepkit/io/shengbte/W>`
   * - BTE.w_anharmonic
     - :doc:`W </autoapi/tepkit/io/shengbte/W>`
   * - BTE.w_anharmonic_plus
     - :doc:`W </autoapi/tepkit/io/shengbte/W>`
   * - BTE.w_anharmonic_minus
     - :doc:`W </autoapi/tepkit/io/shengbte/W>`
   * - BTE.w_final
     - :doc:`W </autoapi/tepkit/io/shengbte/W>`
   * - ...
     - ...
