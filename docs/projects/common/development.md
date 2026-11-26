# Shared-library development

The distribution is `rpt-common`, imported as `rpt_common`, with Python 3.13+,
SQLAlchemy, and Alembic. The `postgres` extra adds Psycopg. There is no PyPI release
or runtime image. Use the library README for setup and test commands.

Central Auth declares this library from Git main and uses an editable sibling
checkout during development. Its image copies only shared package build inputs
from the named context `pycommon`. Its CI resolves common/protobuf revisions once
per run. The package is available on the public `main` branch; consumer builds use
the revision resolved at the start of each workflow run.

Change model definitions and migrations together. Verify fresh/repeated upgrades,
explicit node IDs, disabled defaults, validation, and packaged migration resources.
The central-service integration suite also validates real PostgreSQL, SELECT-only
accounts, encrypted connections, and read-only execution.
