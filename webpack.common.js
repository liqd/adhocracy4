var webpack = require('webpack')
var path = require('path')
var CopyWebpackPlugin = require('copy-webpack-plugin')

module.exports = {
  entry: {
    adhocracy4: [
      './meinberlin/assets/scss/style.scss',
      './meinberlin/assets/js/app.js'
    ],
    vendor: [
      'classnames',
      '@fortawesome/fontawesome-free-webfonts/scss/fontawesome.scss',
      '@fortawesome/fontawesome-free-webfonts/scss/fa-brands.scss',
      '@fortawesome/fontawesome-free-webfonts/scss/fa-regular.scss',
      '@fortawesome/fontawesome-free-webfonts/scss/fa-solid.scss',
      'jquery/dist/jquery.min.js',
      'js-cookie',
      'react',
      'immutability-helper',
      'react-dom',
      'react-flip-move',
      'react-sticky-box',
      'shariff/dist/shariff.min.js',
      'shariff/dist/shariff.min.css'
    ],
    select2: [
      'select2'
    ],
    leaflet: [
      'leaflet',
      'mapbox-gl-leaflet',
      'mapbox-gl/dist/mapbox-gl.js',
      'mapbox-gl/dist/mapbox-gl.css',
      'leaflet/dist/leaflet.css',
      'leaflet.markercluster',
      'leaflet.markercluster/dist/MarkerCluster.css',
      './meinberlin/apps/plans/assets/plans_map.jsx',
      'react-bootstrap-typeahead',
      'react-bootstrap-typeahead/css/Typeahead.css'
    ],
    'mapboxgl': [
      'mapbox-gl/dist/mapbox-gl.js'
    ],
    datepicker: [
      './meinberlin/assets/js/init-picker.js',
      'datepicker/css/datepicker.min.css'
    ],
    embed: [
      './meinberlin/assets/js/embed.js'
    ],
    'popup-close': [
      './meinberlin/assets/js/popup-close.js'
    ],
    'map_choose_polygon_with_preset': [
      './meinberlin/apps/maps/assets/map_choose_polygon_with_preset.js',
      'leaflet-draw',
      'leaflet-draw/dist/leaflet.draw.css',
      './meinberlin/assets/js/i18n-leaflet-draw.js',
      'file-saver',
      'shpjs'
    ]
  },
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
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules\/(?!(adhocracy4|bootstrap)\/).*/, // exclude most dependencies
        loader: 'babel-loader',
        options: {
          presets: ['@babel/preset-env', '@babel/preset-react'].map(require.resolve),
          plugins: ['@babel/plugin-transform-runtime', '@babel/plugin-transform-modules-commonjs']
        }
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
    // when using `npm link`, dependencies are resolved against the linked
    // folder by default. This may result in dependencies being included twice.
    // Setting `resolve.root` forces webpack to resolve all dependencies
    // against the local directory.
    modules: [path.resolve('./node_modules')]
  },
  plugins: [
    new webpack.ProvidePlugin({
      timeago: 'timeago.js',
      $: 'jquery',
      jQuery: 'jquery'
    }),
    new webpack.optimize.SplitChunksPlugin({
      name: 'vendor',
      filename: 'vendor.js'
    }),
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
