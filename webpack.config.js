var ExtractTextPlugin = require('extract-text-webpack-plugin')
var CopyWebpackPlugin = require('copy-webpack-plugin')
var webpack = require('webpack')
var path = require('path')
var autoprefixer = require('autoprefixer')

module.exports = {
  entry: {
    adhocracy4: [
      './meinberlin/assets/scss/style.scss',
      './meinberlin/assets/js/app.js'
    ],
    vendor: [
      'classnames',
      'font-awesome/scss/font-awesome.scss',
      'jquery',
      'js-cookie',
      'react',
      'immutability-helper',
      'react-dom',
      'react-flip-move',
      'shariff',
      'shariff/dist/shariff.min.css'
    ],
    select2: [
      'select2'
    ],
    leaflet: [
      'leaflet',
      'leaflet/dist/leaflet.css'
    ],
    datepicker: [
      './meinberlin/assets/js/init-picker.js',
      'datepicker/css/datepicker.min.css'
    ],
    'leaflet.draw': [
      'leaflet-draw',
      'leaflet-draw/dist/leaflet.draw.css',
      './meinberlin/assets/js/i18n-leaflet-draw.js'
    ],
    embed: [
      './meinberlin/assets/js/embed.js'
    ],
    'popup-close': [
      './meinberlin/assets/js/popup-close.js'
    ]
  },
  devtool: 'eval',
  output: {
    libraryTarget: 'this',
    library: '[name]',
    path: path.resolve('./meinberlin/static/'),
    publicPath: '/static/',
    filename: '[name].js'
  },
  externals: {
    'django': 'django'
  },
  module: {
    noParse: /\.min\.js$/,
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules\/(?!adhocracy4|bootstrap|shariff)/, // exclude most dependencies
        loader: 'babel-loader',
        options: {
          presets: ['babel-preset-es2015', 'babel-preset-react'].map(require.resolve)
        }
      },
      {
        test: /\.s?css$/,
        use: ExtractTextPlugin.extract({
          fallback: 'style-loader',
          use: [
            'css-loader',
            {
              loader: 'postcss-loader',
              options: {
                ident: 'postcss',
                plugins: (loader) => [
                  autoprefixer({
                    browsers: ['last 3 versions', 'ie >= 10']
                  })
                ]
              }
            },
            'sass-loader'
          ]
        })
      },
      {
        test: /fonts\/.*\.(svg|woff2?|ttf|eot)(\?.*)?$/,
        loader: 'file-loader',
        options: {
          name: 'fonts/[name].[ext]'
        }
      },
      {
        test: /\.svg$|\.png$/,
        loader: 'file-loader',
        options: {
          name: 'images/[name].[ext]'
        }
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx', '.scss', '.css'],
    alias: {
      'jquery$': 'jquery/dist/jquery.min.js'
    },
    // when using `npm link`, dependencies are resolved against the linked
    // folder by default. This may result in dependencies being included twice.
    // Setting `resolve.root` forces webpack to resolve all dependencies
    // against the local directory.
    modules: [path.resolve('./node_modules')]
  },
  plugins: [
    new webpack.ProvidePlugin({
      timeago: 'timeago.js'
    }),
    new webpack.optimize.CommonsChunkPlugin({
      name: 'vendor',
      filename: 'vendor.js'
    }),
    new ExtractTextPlugin({filename: '[name].css'}),
    new CopyWebpackPlugin([
      {
        from: './meinberlin/assets/images/**/*',
        to: 'images/',
        flatten: true
      },
      {
        from: './meinberlin/assets/info',
        to: 'info/',
        flatten: false
      }
    ])
  ]
}
