# VCF_MongoDB
 
## Overview
This Python application is designed to streamline the process of importing variant data from VCF (Variant Call Format) files into a MongoDB database, making genomic data analysis more efficient and accessible. The structure of the import is based on the 1000 Genome Project format which I found was quite a clever way of including multiple samples with the drawback of losing quality information about each mutation. 

From my experiences, that quality information per mutation lends itself well compression techniques present in the existing VCF format with software like FM3VCF and HTSlib etc. However in the absence of that information, a generalistic approach geared towards datascience becomes open. By storing the large VCF files using MongoDB, we can make use of sharding to distribute the burden of storage across a network. This also presents a clear interface for non-biologists to approach the 1000 Genome Project Data.

## Features
- Index data by `Sample ID` (As per the format of 1000 Genome Project)

- Support for all chromosomes, including mitochondrial dna

- Support for sharding across a network (PLANNED)

## Installation

```ps
pip install -r requirements.txt
```