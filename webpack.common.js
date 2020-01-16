const webpack = require('webpack')
const path = require('path')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

module.exports = {
  entry: {
    adhocracy4: [
      'shariff/dist/shariff.min.css',
      'select2/dist/css/select2.min.css',
      'slick-carousel/slick/slick.css',
      './meinberlin/assets/extra_css/_slick-theme.css',
      './meinberlin/assets/scss/style.scss',
      './meinberlin/assets/js/app.js'
    ],
    vendor: [
      'classnames',
      '@fortawesome/fontawesome-free/scss/fontawesome.scss',
      '@fortawesome/fontawesome-free/scss/brands.scss',
      '@fortawesome/fontawesome-free/scss/regular.scss',
      '@fortawesome/fontawesome-free/scss/solid.scss',
      'js-cookie',
      'react',
      'immutability-helper',
      'react-dom',
      'react-flip-move',
      'react-sticky-box'
    ],
    mb_plans_map: [
      'leaflet/dist/leaflet.css',
      'mapbox-gl/dist/mapbox-gl.css',
      'leaflet.markercluster/dist/MarkerCluster.css',
      'react-bootstrap-typeahead/css/Typeahead.css',
      './meinberlin/apps/plans/assets/plans_map.jsx'
    ],
    a4maps_display_point: [
      'leaflet/dist/leaflet.css',
      'mapbox-gl/dist/mapbox-gl.css',
      'adhocracy4/adhocracy4/maps/static/a4maps/a4maps_display_point.js'
    ],
    a4maps_display_points: [
      'leaflet/dist/leaflet.css',
      'mapbox-gl/dist/mapbox-gl.css',
      'leaflet.markercluster/dist/MarkerCluster.css',
      'adhocracy4/adhocracy4/maps/static/a4maps/a4maps_display_points.js'
    ],
    a4maps_choose_point: [
      'leaflet/dist/leaflet.css',
      'mapbox-gl/dist/mapbox-gl.css',
      'adhocracy4/adhocracy4/maps/static/a4maps/a4maps_choose_point.js'
    ],
    a4maps_choose_polygon: [
      'leaflet/dist/leaflet.css',
      'mapbox-gl/dist/mapbox-gl.css',
      'leaflet-draw/dist/leaflet.draw.css',
      './meinberlin/apps/maps/assets/map_choose_polygon_with_preset.js'
    ],
    datepicker: [
      './meinberlin/assets/js/init-picker.js',
      'datepicker/css/datepicker.min.css'
    ],
    embed: [
      'bootstrap/js/dist/modal.js',
      './meinberlin/apps/embed/assets/embed.js'
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
    django: 'django'
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules\/(?!(adhocracy4)\/).*/, // exclude most dependencies
        loader: 'babel-loader',
        options: {
          presets: ['@babel/preset-env', '@babel/preset-react'].map(require.resolve),
          plugins: ['@babel/plugin-transform-runtime', '@babel/plugin-transform-modules-commonjs']
        }
      },
      {
        test: /\.s?css$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader
          },
          {
            loader: 'css-loader'
          },
          {
            loader: 'postcss-loader',
            options: {
              ident: 'postcss',
              plugins: [
                require('autoprefixer')
              ]
            }
          },
          {
            loader: 'sass-loader'
          }
        ]
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
      a4maps_common$: 'adhocracy4/adhocracy4/maps/static/a4maps/a4maps_common.js',
      bootstrap$: 'bootstrap/dist/js/bootstrap.bundle.min.js',
      jquery$: 'jquery/dist/jquery.min.js',
      select2$: 'select2/dist/js/select2.min.js',
      shariff$: 'shariff/dist/shariff.min.js',
      shpjs$: 'shpjs/dist/shp.min.js',
      tether$: 'tether/dist/js/tether.min.js',
      'slick-carousel$': 'slick-carousel/slick/slick.min.js'
    },
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
      jQuery: 'jquery',
      Promise: ['es6-promise', 'Promise']
    }),
    new webpack.optimize.SplitChunksPlugin({
      name: 'vendor',
      filename: 'vendor.js'
    }),
    new MiniCssExtractPlugin({
      filename: '[name].css',
      chunkFilename: '[name].css'
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
