project('wwplot',
  version: '0.0.3',
  meson_version: '>= 0.40.0'
)

py3_mod = import('python3')
i18n_mod = import('i18n')

message('Checking dependencies')
py3 = py3_mod.find_python()

gtk3 = dependency('gtk+-3.0', version: '>= 3.18')

pygobj = dependency('pygobject-3.0')
pycairo = dependency('py3cairo')

prefix = get_option('prefix')
bindir = join_paths(prefix, get_option('bindir'))
datadir = join_paths(prefix, get_option('datadir'))
localedir = join_paths(prefix, get_option('localedir'))

# Support Debian non-standard python paths
# Fallback to Meson python3 module if command fails
message('Getting python install path')
py3_purelib = ''
r = run_command(py3.path(), '-c', 'from distutils.sysconfig import get_python_lib; print(get_python_lib(prefix=""))')
if r.returncode() != 0
  py3_purelib = py3_mod.sysconfig_path('purelib')
  if not py3_purelib.endswith('site-packages')
    error('Cannot find python install path')
  endif
  py3_dir = py3_purelib
else
  py3_dir = r.stdout().strip()
endif

message('Installing WWplot')
install_subdir('WWplot', install_dir: py3_dir)

conf_wwplot = configuration_data()
conf_wwplot.set('LOCALEDIR', localedir)
conf_wwplot.set('PROJECT_NAME', meson.project_name())
configure_file(input: 'wwplot.in',
               output: 'wwplot',
               configuration: conf_wwplot,
               install_dir: bindir)

message('Installing data files')
subdir('data')
subdir('po')

meson.add_install_script('meson_post_install.py')
