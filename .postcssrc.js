module.exports = ({env}) => ({
  plugins: {
    'postcss-import': {},
    'postcss-nesting': {},
    'autoprefixer': {},
    'cssnano': env === 'production' ? {} : false,
  }
});
