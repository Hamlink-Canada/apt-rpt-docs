# Shared-library development

The distribution is `rpt-common`, imported as `rpt_common`, with Python 3.13+,
SQLAlchemy, and Alembic. The `postgres` extra adds Psycopg. There is no PyPI release
or runtime image. Use the library README for setup and test commands.

Central Auth declares this library from Git main and uses an editable sibling
checkout during development. Its image copies only shared package build inputs
from the named context `pycommon`. Its CI resolves common/protobuf revisions once
per run. Merge the initial shared-library implementation before expecting public
main-based consumer builds to work.

Change model definitions and migrations together. Verify fresh/repeated upgrades,
explicit node IDs, disabled defaults, validation, and packaged migration resources.
The central-service integration suite also validates real PostgreSQL, SELECT-only
accounts, encrypted connections, and read-only execution.
