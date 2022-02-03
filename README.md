# enron-data-literacy

This repository contains the experiments, source code and documentation that we created for the Data Literacy 21/22 project at the University of Tuebingen.

## Abstract
The Enron mail corpus provides real world corporate mail communication data.
The corpus contains mails by Enron personell during the phase in which Enron de-
clared bankruptcy. We extract the core working hours of the Enron personell from
this dataset. The dataset indicates that Enron performed a migration of their mail
systems shortly before the scandal became public, which introduces an interesting
shift in the mails’ time information. However, we show that there is no significant
change in core working hours over time.

## Structure of the repository
The raw data is in `data`, the `doc` folder contains the Latex documentation. `exp` has the experiment data and `src` contains the python source code to parse the e-mails and to generate the plots used in the documentation.

## Running the experiments
To run the experiments, you need the Enron Mail Corpus. It is available for download [here](https://www.cs.cmu.edu/~enron/). After downloading it, make sure it is present in the data folder of this repository (e.g. via a symlink or by extracting it there). The final structure should look like this:

```shell
├── data
│   └── maildir
│       ├── allen-p
│       ├ ...
├── doc
├── exp
└── src
```
Also, make sure you have installed python3, Jupyter Notebook and the modules `pandas`, `matplotlib`, `numpy` and `tueplots`. The experiments are 

