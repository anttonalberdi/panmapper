# PanMapper
Metagenomic pangenome mapper

## Modify config file

Specify input and output directories as well as database paths.

## Launch pipeline

### Locally
```
snakemake --use-conda --workflow-profile profile/local
```

### Slurm
```
snakemake --use-conda --workflow-profile profile/slurm
```
