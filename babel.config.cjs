const config = {
  env: {
    test: {
      plugins: [
        '@babel/plugin-transform-modules-commonjs',
        '@babel/plugin-transform-runtime'
      ]
    }
  },
  presets: [
    '@babel/preset-react',
    '@babel/preset-env',
    '@babel/preset-typescript'
  ]
}

module.exports = config
