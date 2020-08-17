let mode = process.argv[3];
if (mode == "development") {
  module.exports = {
    plugins: [
      require('autoprefixer')
    ]
  }
} else {
  module.exports = {
    plugins: [
      require('autoprefixer'),
      require('css-mqpacker'),
      require('cssnano')({
        preset: [
          'default', {
            discardComments: {
              removeAll: true,
            }
          }
        ]
      })
    ]
  }
}