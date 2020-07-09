const common = require('./webpack.common.js')
const { merge } = require('webpack-merge')
const TerserPlugin = require('terser-webpack-plugin')

module.exports = merge(common, {
  optimization: {
    minimizer: [
      new TerserPlugin({
        sourceMap: true,
        parallel: true,
        terserOptions: {
          ecma: 5,
          arrows: false
        }
      })
    ]
  }
})
