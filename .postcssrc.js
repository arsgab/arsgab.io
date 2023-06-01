module.exports = ({env}) => ({
  parser: require('postcss-comment'),
  plugins: {
    'postcss-import': {},
    'postcss-nesting': {},
    'postcss-custom-media': {},
    'postcss-easing-gradients': {},
    'autoprefixer': {},
    'cssnano': env === 'production' ? {} : false,
  }
});
