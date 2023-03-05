
.. _usage:

Quickstart Guide
##################

This project aims to provide a user friendly environment for adding and running cocotb tests for *Caravel user projects*. 

Please setup your project through ``ChipCraft`` as this project is setuped and run through ``ChipCraft``.

.. todo::

      Add chipcraft docs link or info 


.. todo::

      Add link for examples 

.. _create_test:

Creating a Test
***************

A typical test for *Caravel* consists of 2 parts: ``Python/cocotb`` code and ``C`` code. 

* ``Python/cocotb`` code is for communicating with *Caravel* hardware interface inputs, outputs, clock, reset, and power ports/bins. ``cocotb`` here replaces the ``verilog`` code.

* ``C`` code provides firmware code that would be loaded into the *Caravel* CPU.

Tests files has to located under ``<caravel_user_project>/verilog/dv/cocotb/`` 

.. code-block::

      | dv
      | ├── cocotb
      | │   ├── <new_test>
      | │   │   └── <new_test.py>
      | │   │   └── <new_test.c>
      | │   └── cocotb_tests.py
      | 


.. note:: 

   The name of ``C`` file must match the name of ``cocotb`` test function 

Python Template
-----------------------------------------------------------------------------------------------

The template for ``python`` test:

.. code-block:: python3

   from cocotb_includes import * # import python APIs 
   import cocotb

   @cocotb.test() # cocotb test marker
   @repot_test # wrapper for configure test reporting files
   async def <test_name>(dut):
      caravelEnv = await test_configure(dut) #configure, start up and reset caravel

      ######################## add test sequence ###################### 


Commonly used APIs to monitor or drive the hardware can be found in :doc:`python_api`

.. warning:: 

   New test python function should be imported into cocotb_tests.py 

   .. code-block:: python3

      from <new_test>.<new_test> import <new_test>


C Template
----------------------

The template for Code test:

.. code-block:: C++

   #include <common.h> // include required APIs 
   void main(){
      //////////////////////add test here////////////////////// 
      return;
   }


Commonly used APIs for firmware can be found in :doc:`C_api`


.. _run_test:

Running a Test
***************

Run with ChipCraft 
--------------------------------

``chipcraft verify <testname> --design <design name>``


.. todo::

      Add how to run test using chipcraft


Run without ChipCraft 
-------------------------

Check prerequisites
^^^^^^^^^^^^^^^^^^^^
* Docker: `Linux <https://hub.docker.com/search?q=&type=edition&offering=community&operating_system=linux&utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header>`__ || `Windows <https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header>`__ || `Mac with Intel Chip <https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header>`__ || `Mac with M1 Chip <https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker&utm_medium=webreferral&utm_campaign=dd-smartbutton&utm_location=header>`__

.. include:: ../../README.md
   :start-after: <!-- start configure the repo include0 -->
   :end-before: <!-- end configure the repo include0 -->

Configure the repo
^^^^^^^^^^^^^^^^^^^^
.. note:: 

      This step is only when first clone the repo.

.. include:: ../../README.md
   :start-after: <!-- start configure the repo include1 -->
   :end-before: <!-- end configure the repo include1 -->

.. literalinclude:: ../../README.md
   :start-after: <!-- start configure the repo include2 -->
   :end-before: <!-- end configure the repo include2 -->

Run test/tests
^^^^^^^^^^^^^^^^^^^^

.. include:: ../../README.md
   :start-after: <!-- start run a test include1 -->
   :end-before: <!-- end run a test include1 -->


.. literalinclude:: ../../README.md
   :start-after: <!-- start run a test include2 -->
   :end-before: <!-- end run a test include2 -->

Example
"""""""""""

.. include:: ../../README.md
   :start-after: <!-- start run a test include3 -->
   :end-before: <!-- end run a test include3 -->

.. _create_testlist:

Creating a Testlist
*********************

Testlist is a file that contain a collection of test names to run together. 

The syntax is simple as ``YAML`` is used to write the testlist  

.. code-block:: yaml

   # Testlist Can has only 2 elements Tests or includes 

   # Test element has list of dictionaries of tests to include 
   Tests: 
      - {name: <test1>, sim: RTL} 
      - {name: <test1>, sim: GL} 
      - {name: <test2>, sim: RTL} 

   # include has paths  for other testlist to include in this test list 
   # paths are relative to the location of this yaml file
   includes: 
      - <test4>/<testlist>.yaml
      - <testlist>.yaml
      - ../<test5>/<testlist>.yaml


.. todo::

      Add support for more elements for the test like clock, seed 



Checking Results
*********************

.. include:: ../../README.md
   :start-after: <!-- start result include1 -->
   :end-before: <!-- end result include1 -->

.. literalinclude:: ../../README.md
   :start-after: <!-- start result include2 -->
   :end-before: <!-- end result include2 -->


.. todo::

      Add description of sim directiory 