const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
  devtool: 'source-map',
  entry: {
    index: ['./src/js/index.js', './src/scss/style.scss'],
    scope: ['./src/js/scope.js'],
    vulns: ['./src/js/vulns.js'],
    vuln: ['./src/js/vuln.js'],
    login: ['./src/js/login.js']
  },

  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, './prod')
  },

  module: {
    rules: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
        include: path.resolve(__dirname, 'src/js')
      },
      {
        test: /\.(sass|scss)$/,
        include: path.resolve(__dirname, 'src/scss'),
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
            options: { sourceMap: true }
          },
          {
            loader: 'postcss-loader',
            options: { sourceMap: true, config: { path: './postcss.config.js' } }
          },
          {
            loader: 'sass-loader',
            options: { sourceMap: true }
          }
        ]
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "style.css",
    })
  ]
}