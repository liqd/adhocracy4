var ExtractTextPlugin = require('extract-text-webpack-plugin')
var webpack = require('webpack')
var autoprefixer = require('autoprefixer')

module.exports = {
  entry: {
    meinberlin: [
      './meinberlin/assets/scss/style.scss',
      './meinberlin/assets/js/app.js'
    ],
    vendor: [
      'classnames',
      'font-awesome/scss/font-awesome.scss',
      'jquery',
      'js-cookie',
      'moment',
      'moment/locale/de.js',
      'react',
      'react-addons-update',
      'react-dom',
      'react-flip-move'
    ]
  },
  devtool: 'eval',
  output: {
    libraryTarget: 'var',
    library: 'adhocracy4',
    path: './meinberlin/static/',
    publicPath: '/static/',
    filename: '[name].js'
  },
  externals: {
    'django': 'django'
  },
  module: {
    noParse: /\.min\.js$/,
    loaders: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules\/(?!adhocracy4|bootstrap)/,  // exclude all dependencies but adhocracy4 and bootstrap
        loader: 'babel-loader',
        query: {
          presets: ['babel-preset-es2015', 'babel-preset-react'].map(require.resolve)
        }
      },
      {
        test: /\.s?css$/,
        loader: ExtractTextPlugin.extract('style?sourceMap', '!css?sourceMap!postcss?sourceMap!sass?sourceMap')
      },
      {
        test: /fonts\/.*\.(svg|woff2?|ttf|eot)(\?.*)?$/,
        loader: 'file-loader?name=fonts/[name].[ext]'
      },
      {
        test: /\.svg$|\.png$/,
        loader: 'file-loader?name=images/[name].[ext]'
      }
    ]
  },
  postcss: [
    autoprefixer({browsers: ['last 3 versions', 'ie >= 10']})
  ],
  resolve: {
    extensions: ['', '.js', '.jsx', '.scss', '.css'],
    alias: {
      'jquery$': 'jquery/dist/jquery.min.js'
    }
  },
  plugins: [
    new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
    new webpack.optimize.CommonsChunkPlugin('vendor', 'vendor.js'),
    new ExtractTextPlugin('[name].css')
  ]
}
