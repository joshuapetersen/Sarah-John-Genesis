CMAKE_<LANG>_SIMULATE_ID
------------------------

Identification string of the "executed" compiler.

Some compilers execute other compilers to serve as drop-in
replacements.  When CMake detects such a compiler it sets this
variable to what would have been the :variable:`CMAKE_<LANG>_COMPILER_ID` for
the executed compiler.

.. note::
  In other words, this variable describes the ABI compatibility
  of the generated code.
