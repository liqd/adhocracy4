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
    '@babel/preset-env'
  ],
  externals: {
    react_markdown: 'react-markdown',
    react_popper: 'react-popper',
    react_slick: 'react-slick'
  }
}

module.exports = config
