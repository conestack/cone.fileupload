Changes
=======

2.0.1 (unreleased)
------------------

- Sort the imports with ruff (one per line, ``from`` imports first, no
  sections) and format the code with ``ruff format`` (90 characters per line,
  single quotes).
  [rnix]

- Add import sorting (``I`` rules) and the formatter settings to the ruff
  configuration in ``pyproject.toml``.
  [rnix]


2.0.0 (2026-10-24)
------------------

- Drop the Python 2 ``StringIO`` import fallback in tests.
  [rnix]

- Modernise the code ruff flags as outdated: ``u''`` prefixes, ``class
  X(object)``, ``.format()`` over f-strings. Behaviour unchanged.
  ``super(Class, self)`` is kept, see ``cone.app``.
  [rnix]

- Add ``qa.ruff`` domain to Makefile and pin the ruff rule selection in
  ``pyproject.toml``, ``make check`` runs ``ruff check``.
  [rnix]

- Pin ``setuptools<82.0.0`` in ``mx.ini``. ``pyramid`` 2.0.2 still imports
  ``pkg_resources``, which ``setuptools`` 82 removed.
  [rnix]

- Bootstrap 5 styles.


1.1.0 (2026-02-03)
------------------

- Refactor package layout to use ``pyproject.toml`` and implicit namespace packages.
  [rnix]

- Setup Makefile.
  [lenadax]

- Run tests with pytest.
  [lenadax]


1.0a1 (2023-05-15)
------------------

- Use ``webresource`` for resource registration.
  [rnix]

- Replace deprecated use of ``allow_non_node_children`` by ``child_constraints``.
  [rnix]


0.8 (2025-10-25)
----------------

- Pin upper versions of dependencies.
  [rnix]

- Replace deprecated use of ``allow_non_node_children`` by ``child_constraints``.
  [rnix]


0.7 (2022-01-19)
----------------

- Modernize JavaScript setup.

- Add ``i18n_messages_src``, ``upload_template_src`` and
  ``download_template_src`` attributes to ``FileUploadTile``.

- Add optional ``download_url`` to file data dict.

- Remove ``thumbnailUrl`` from file data dict.

**Breaking Changes**

- Rename ``url`` to ``view_url`` in file data dict.

- Rename ``deleteUrl`` to ``delete_url`` in file data dict.

- Rename ``deleteType`` to ``delete_type`` in file data dict.


0.6 (2021-11-21)
----------------

- Fileupload actions optionally work from contextmenu.
  [rnix]

- Move button toolbar into dedicated tile for customization.
  [rnix]

- Reduce included files and plugins of jquery fileupload to required ones.
  [rnix]

- Update jquery fileupload to version 10.32.0.
  [rnix]


0.5 (2021-11-08)
----------------

- Rename deprecated ``allow_non_node_childs`` to ``allow_non_node_children``
  in tests and documentation.
  [rnix]


0.4 (2020-05-30)
----------------

- Initial pypi release
  [rnix]


0.3
---

- Python 3 compatibility.
  [rnix]

- Convert doctests to unittests.
  [rnix]

- Use ``cone.app.main_hook`` decorator.
  [rnix]

- Move resource registration to main hook.
  [rnix]

- Upgrade to ``cone.app`` 1.0b1.
  [rnix]


0.2
---

- Code organization.
  [rnix]


0.1
---

- Make it work
  [rnix]
