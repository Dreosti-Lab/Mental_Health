# Load required package
library(arrow)

# Specify R dataset path(s) (*.rds)
# rds_path <- "ukb27307.subset5.rds"
# rds_path <- "Round_2_Data/ukb27307.subset1.rds"
rds_path <- "Round_2_Data/ukb27307.subset7.rds"

# Generate output paths by replacing ".rds" with ".parquet" and ".feather"
parquet_path <- sub("\\.rds$", ".parquet", rds_path)
feather_path <- sub("\\.rds$", ".feather", rds_path)

# Load the RDS file
d <- readRDS(rds_path)

# Save as a Parquet file (better for large datasets)
write_parquet(d, parquet_path)

# Or save as a Feather file (fastest for Python)
write_feather(d, feather_path)

print(paste("Conversion complete:", rds_path, "->", parquet_path, "and", feather_path))
