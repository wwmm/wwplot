i18n_mod.merge_file(
  input: 'com.github.wwmm.wwplot.desktop.in',
  output: 'com.github.wwmm.wwplot.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(datadir, 'applications')
)

icondir = join_paths(datadir, 'icons', 'hicolor')
install_data('wwplot.svg',
  install_dir: join_paths(icondir, 'scalable', 'apps')
)
