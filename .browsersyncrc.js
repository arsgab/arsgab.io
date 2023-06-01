module.exports = {
  server: '.',
  files: ['*.html', './**/*.js', './build/**/*.css'],
  watchEvents: ['change', 'add', 'unlink'],
  open: 'local',
  reloadOnRestart: true,
  notify: false,
  scrollProportionally: false,
  scrollThrottle: 100,
  minify: false,
}
