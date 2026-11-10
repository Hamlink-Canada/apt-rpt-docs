# Share schemas through a Git-pinned Python dependency

Keep the four repositories independently releasable and make each service depend on `rpt_protobuf` at a full Git commit SHA, with generated bindings committed in the library and reproducibility checked in CI. We will publish service Docker images rather than Python packages to PyPI; this retains a single schema owner and works while repositories are private, at the cost of authenticated source access during builds and explicit dependency updates across repositories.
