# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Add required packages from GitHub (UserName/RepositoryName) to this vector
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
GitHub_packages <- NULL

main <- function(GitHub_packages = NULL,
                 CRAN_repo = "http://cran.wustl.edu/",
                 dependency = TRUE, quiet = TRUE, upgrade = FALSE) {

    # If there are packages installed from Github, first make sure "devtools" is installed 
    if (!is.null(GitHub_packages)) {
        install_CRAN("devtools", repo = CRAN_repo, dependency = dependency,
                     quiet = quiet, upgrade = upgrade)
    }

    # Install packages from GitHub
    if (!is.null(GitHub_packages)) {
        library(devtools)
        lapply(GitHub_packages, function(pkg) install_github(pkg))
    }
}

install_CRAN <- function(pkg, repo, dependency, quiet, upgrade = FALSE) {
    if (upgrade) {
        install.packages(pkg, repos = repo, dependencies = dependency, quiet = quiet)
    } else {
        if (system.file(package = pkg) == "") {
            install.packages(pkg, repos = repo, dependencies = dependency, quiet = quiet)
        }
    }
}

# upgrade = TRUE will update all packages to the most current version
# upgrade = FALSE will skip packages that are already installed
main(GitHub_packages, upgrade = FALSE)
