# Call these commands with:
# $ doit

import doit
import glob


def task_build():
    """build cmd """
    return {
        'actions': ['pdflatex -shell-escape 00_About_Slides ;pdflatex -shell-escape 00_About_Slides ; bibtex 00_About_Slides ; pdflatex -shell-escape 00_About_Slides',],
        'file_dep': ["00_About_Slides.tex"],
        'targets': ["00_About_Slides.pdf"],
        'verbosity': 2,
        }
