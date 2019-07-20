project('wwplot',
  version: '0.0.5',
  meson_version: '>= 0.51.0'
)

pymod = import('python')
i18n_mod = import('i18n')

required_modules = ['PySide2','numpy','scipy']

py3 = pymod.find_installation('python3', modules:required_modules)

message('python version: ' + py3.language_version())
message('module install path: ' + py3.get_install_dir())

prefix = get_option('prefix')
bindir = join_paths(prefix, get_option('bindir'))
datadir = join_paths(prefix, get_option('datadir'))
localedir = join_paths(prefix, get_option('localedir'))

install_subdir('WWplot', install_dir: py3.get_install_dir())

conf_wwplot = configuration_data()
conf_wwplot.set('LOCALEDIR', localedir)
conf_wwplot.set('PROJECT_NAME', meson.project_name())
configure_file(input: 'wwplot.in',
               output: 'wwplot',
               configuration: conf_wwplot,
               install_dir: bindir)

subdir('data')
subdir('po')
