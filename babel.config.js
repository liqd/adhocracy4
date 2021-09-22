const config = {
  env: {
    test: {
      plugins: [
        '@babel/plugin-transform-modules-commonjs'
      ]
    }
  },
  presets: [
    '@babel/preset-react',
    '@babel/preset-env'
  ]
}

module.exports = config
