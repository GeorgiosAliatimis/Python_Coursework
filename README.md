# Python_Coursework
This repository consists code for the [Introductory Python Course](http://www.mathsbox.com/introductory-python/STOR-601-stable-marriage-assessment.html),
which is part of STOR-i assessment. <br> 
Most of this project focuses on the Stable Matching/Marriage Problem, as described in the book 
[Stable Marriage and Its Relation to Other Combinatorial Problems](https://ebookcentral.proquest.com/lib/lancaster/detail.action?docID=4908424).<br>

## Installation
<b> Prerequisites: </b> Linux OS, conda<br>
1. First, create a new environment with the name stable_matching_env by running
      ```
      conda env create -f environment.yml
      ```
2. You need to add stable_matching_env to the jupyter kernel
      ```
      conda activate stable_matching_env
      python -m ipykernel install --user --name=stable_matching_env
      conda deactivate
      ```
3. If you do not have jupyter installed, run
      ```
      conda install -c anaconda jupyter 
      ```
4. Run 
      ```
      jupyter notebook
      ```
5. Change the kernel (from the top panel Kernel > Change Kernel > stable_matching_env).

If you use different OS or do not have conda set up, try pip installing the packages in requirements.txt and use python 3.10. 
