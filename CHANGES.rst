Changes
=======

1.0a1 (2023-05-15)
------------------

- Use ``webresource`` for resource registration.
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
