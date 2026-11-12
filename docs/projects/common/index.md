# Shared Python utilities

[pyCommon](https://github.com/Hamlink-Canada/pyCommon) owns Python code shared across
projects, including the SQLAlchemy node-credential model and its migrations. Central
Auth reads the model; an operator-managed process writes credentials. There
is no shared-library service endpoint or standalone runtime image.

Database models live in `rpt_common.models`; migrations remain in
`rpt_common.migrations`. Other shared Python modules can be added alongside these
packages.

Start with [the model](model.md), [migrations](migrations.md), and
[development](development.md). Operator command and Job examples are maintained in
the [library README](https://github.com/Hamlink-Canada/pyCommon#readme) and Central Auth
README. The package is available from Git `main`; follow the library README for
installation and dependency pinning.
