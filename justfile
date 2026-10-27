# list recipes
default:
    just --list

# install and run
run:
    uv run

# install dependencies
install:
    uv sync --frozen

# upgrade dependencies
update:
    uv lock --upgrade

# check code with ruff
check:
    ruff check

# format with ruff
format:
    ruff format

# build package
build: check format
	rm -rf dist/; \
	uv build

# test package can be installed and imported
package-test:
    uv run --with "skyra_data_wrapper" --no-project -- python -c "import skyra_data_wrapper"

