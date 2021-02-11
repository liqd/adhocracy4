const common = require('./webpack.common.js')
const { merge } = require('webpack-merge')
const TerserPlugin = require('terser-webpack-plugin')

module.exports = merge(common, {
  devtool: 'eval',
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        parallel: true,
        terserOptions: {
          ecma: 5
        }
      })
    ]
  }
})
