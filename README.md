# Design and Professional Skills
A repository of teaching material for the UCL ENGF0002 Computer Science course.

## Structure

The structure of the material is as follows:
- The `Docs' directory contains meta-information such as the course sylabus.
- The `Topics' folder contains the lecture notes, and example code for all topics covered in the course.
- Each topic contains a folder `src' containing the source code of a number of examples and tests for those examples.
- Coursework will appear in the 'Assignments' folder when it has been set.

## Building the lecture notes

Since we are computer scientists we have integrated the production of
lecture notes into a proper build system and a sophisticated tool
chain to avoid errors in code fragments. In order to compile the
lecture notes you will need: latex (with the beamer class, tikz and
the UCL beamer templates); python3; the [doit](http://pydoit.org/),
[pytest](https://docs.pytest.org/en/latest/) and Pygments packages.

You will need git, and to clone this repository locally. When all the dependencies are installed you may simply type `doit' in each topic folder to build the slides into a pdf. Under the hood this runs all unit tests and doctests, produces figures from running code, and finally compiles the latex into a pdf file.

Alternatively, if you are a student at UCL we will be posting the lecture notes on UCL Moodle as well.

## How to report typos and errors, or propose enhancements

Github comes with a handy bug tracker, which we invite students and other users of the material to use to report bugs. You can open an issue here: https://github.com/mhandley/ENGF0002-2019/issues . Pull requests earn you an honorable mention as a contributor.
