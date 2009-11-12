
import sys
from os.path import join, basename, dirname, splitext
from glob import glob

from numpy.distutils import log
from distutils.dep_util import newer

def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration

    package_name = 'nidaqmx'
    script_prefix = package_name

    config = Configuration(package_name,parent_package,top_path)
    config.make_svn_version_py()

    wininst = 'bdist_wininst' in sys.argv

    try:
        import multiprocessing
    except ImportError:
        multiprocessing = None

    scripts = glob(join(config.local_path, 'scripts', '*.py'))
    for script in scripts:
        if basename (script).startswith(script_prefix):
            config.add_scripts(script)
            continue

        def generate_a_script(build_dir, script=script, config=config):
            dist = config.get_distribution()
            install_lib = dist.get_command_obj('install_lib')
            if not install_lib.finalized:
                install_lib.finalize_options()

            script_replace_text = ''
            install_lib = install_lib.install_dir
            if install_lib is not None:
                script_replace_text = '''
import sys
if %(d)r not in sys.path:
    sys.path.insert(0, %(d)r)
''' % dict(d=install_lib)
            if multiprocessing is not None:
                mp_install_lib = dirname(dirname(multiprocessing.__file__))
                script_replace_text += '''
if %(d)r not in sys.path:
    sys.path.insert(0, %(d)r)
''' % dict(d=mp_install_lib)

            start_mark = '### START UPDATE SYS.PATH ###'
            end_mark = '### END UPDATE SYS.PATH ###'
            name = basename(script)
            if name.startswith (script_prefix):
                target_name = name
            elif wininst:
                target_name = script_prefix + '_' + name
            else:
                target_name = script_prefix + '.' + splitext(name)[0]
            target = join(build_dir, target_name)
            if newer(script, target) or 1:
                log.info('Creating %r', target)
                f = open (script, 'r')
                text = f.read()
                f.close()

                i = text.find(start_mark)
                if i != -1:
                    j = text.find (end_mark)
                    if j == -1:
                        log.warn ("%r missing %r line", script, start_mark)
                    new_text = text[:i+len (start_mark)] + script_replace_text + text[j:]
                else:
                    new_text = text

                f = open(target, 'w')
                f.write(new_text)
                f.close()
        config.add_scripts(generate_a_script)


    return config
