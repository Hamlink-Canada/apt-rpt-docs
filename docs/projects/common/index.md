# Shared Python utilities

[pyCommon](https://github.com/Hamlink-Canada/pyCommon) owns Python code shared across
projects, initially the SQLAlchemy node-credential model and its migrations. Central
Auth reads the model; a separate provisioning project will write credentials. There
is no shared-library service endpoint or standalone runtime image.

Database models live in `rpt_common.models`; migrations remain in
`rpt_common.migrations`. Other shared Python modules can be added alongside these
packages.

Start with [the model](model.md), [migrations](migrations.md), and
[development](development.md). Operator command and Job examples are maintained in
the [library README](https://github.com/Hamlink-Canada/pyCommon#readme) and Central Auth
README. The implementation is prepared locally; publication/merge status must be
checked before consuming the initial package from Git main.
