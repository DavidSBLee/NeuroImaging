# ANTsR (Advacned Normalization Tool ported into R using Rcpp)
# Spatial Normalization
# I used this commands on terminal to install
# Only need to do these once

### From Terminal and from Git ###
git clone https://github.com/ANTsX/ANTsRCore.git
git clone https://github.com/ANTsX/ANTsR.git
git clone https://github.com/ANTsX/ITKR.git

# Or Use these
git clone https://github.com/stnava/ANTsRCore.git
git clone https://github.com/stnava/ANTsR.git
git clone https://github.com/stnava/ITKR.git

R CMD INSTALL ITKR
R CMD INSTALL ANTsRCore
R CMD INSTALL ANTsR

### From Terminal and from R (NOT from R studio or R gui) ###
devtools::install_github("stnava/cmaker")
devtools::install_github("stnava/ITKR")
devtools::install_github("stnava/ANTsR")
Install Xquarts!!!: https://dl.bintray.com/xquartz/downloads/XQuartz-2.7.11.dmg
devtools::install_github("muschellij2/extrantsr")

# If thiings need to be upgraded
devtools::install_github("stnava/ANTsRCore", upgrade_dependencies = FALSE)
devtools::install_github("stnava/ANTsR", upgrade_dependencies = FALSE)
devtools::install_github("muschellij2/extrantsr", upgrade_dependencies = FALSE)

#Refer to These Pages for more detailed information
http://johnmuschelli.com/neuroc/installing_ANTsR/index.html
http://johnmuschelli.com/imaging_in_r/installing_everything_locally/
https://github.com/muschellij2/Neurohacking/blob/master/Installation.Rmd