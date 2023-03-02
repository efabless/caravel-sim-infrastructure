
.. _usage:

****************
Quickstart Guide
****************

This project aims to provide a user friendly environment for adding and running cocotb tests for *Caravel user projects*. 

Please setup your project through ``ChipCraft`` as this project is setuped and run through ``ChipCraft``.

.. todo::

      Add chipcraft docs link or info 


.. todo::

      Add link for examples 

.. _create_test:

Creating a Test
===============

A typical test for *Caravel* consists of 2 parts: ``Python/cocotb`` code and ``C`` code. 

* ``Python/cocotb`` code is for communicating with *Caravel* hardware interface inputs, outputs, clock, reset, and power ports/bins. ``cocotb`` here replaces the ``verilog`` code.

* ``C`` code provides software code that would be loaded into the *Caravel* CPU.

Tests files has to located under ``<caravel_user_project>/verilog/dv/cocotb/`` 


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
++++++++++++++++

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
++++++++++++++++

The template for Code test:

.. code-block:: C++

   #include <common.h> // include required APIs 
   void main(){
      //////////////////////add test here////////////////////// 
      return;
   }


Commonly used APIs for software can be found in :doc:`C_api`


.. _run_test:

Running a Test
===============

``chipcraft verify <testname> --design <design name>``


.. todo::

      Add how to run test using chipcraft


.. _create_testlist:

Creating a Testlist
=======================

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

Running a Testlist
=====================

.. todo::

      Add how to run testlist using chipcraft


Checking Results
=====================

.. todo::

      Add description of sim directiory 