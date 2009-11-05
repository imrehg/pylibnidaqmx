
# THIS FILE IS GENERATED FROM SETUP.PY
short_version='0.2.0'
version='0.2.0'
release=False

if not release:
    version += '.dev'
    import os
    svn_version_file = os.path.join(os.path.dirname(__file__),
                                   '__svn_version__.py')
    if os.path.isfile(svn_version_file):
        import imp
        svn = imp.load_module('nidaqmx.__svn_version__',
                              open(svn_version_file),
                              svn_version_file,
                              ('.py','U',1))
        version += svn.version
