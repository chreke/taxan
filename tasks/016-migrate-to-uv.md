# Migrate to uv

We need a way to:

- separate dependencies from transitive dependencies
- ensure that a dependency list gets updated automatically when a package is installed

pip doesn't satisfy these requirements, so we need to switch to something else.
