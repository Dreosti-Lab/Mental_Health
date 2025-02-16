# Analysis of UK BioBank data

## Requirements

- Create and activate a new virtual environment

```bash
mkdir _tmp
cd _tmp
python -m venv UKBB
source UKBB/bin/activate
```

- Install R dataset reader for Python (pyarrow), which requires conversion from RDS format

```bash
pip install numpy pandas pyarrow
```

## Converting RDS to Parquet/Feather
Loading RDS files in Python can be extremely slow. Use then following R script to convert them to a more Python-friendly format. *Note*: You may need to run this script with "sudo"

```R
# Install required package (arrow) - can take a long time!
install.packages("arrow", repos='http://cran.us.r-project.org')  # Install if not already installed
```

```R
library(arrow)

# Load the RDS file
d <- readRDS("ukb27307.subset5.rds")

# Save as a Parquet file (better for large datasets)
write_parquet(d, "ukb27307.subset5.parquet")

# Or save as a Feather file (fastest for Python)
write_feather(d, "ukb27307.subset5.feather")

print("Conversion complete: RDS -> Parquet & Feather")
```