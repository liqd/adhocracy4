// List of node modules which need to be transformed for jest to work
const esModules = [
  /** react-leaflet */
  '@?react-leaflet',
  /** react-markdown 9.0.1 */
  'react-markdown',
  'bail',
  'comma-separated-tokens',
  'decode-named-character-reference',
  'devlop/lib/default',
  'estree-util-is-identifier-name',
  'hast-util-.*',
  'html-url-attributes',
  'is-plain-obj',
  'mdast-util-.*',
  'micromark.*',
  'property-information',
  'remark-.*',
  'space-separated-tokens',
  'trim-lines',
  'trough',
  'unified',
  'unist-.*',
  'vfile-message',
  /** react-markdown 8.0.3 */
  'vfile'
].join('|')

const config = {
  testEnvironment: 'jsdom',
  modulePaths: ['<rootDir>'],
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': '<rootDir>/__mocks__/styleMock.js',
    '\\.(gif|ttf|eot|svg)$': '<rootDir>/__mocks__/fileMock.js',
    '(django)': '<rootDir>/__mocks__/djangoMock.js',
    'react-flip-move': '<rootDir>/__mocks__/flipmoveMock.js'
  },
  testMatch: ['**/*.jest.js', '**/*.jest.jsx'],
  testPathIgnorePatterns: ['venv/', 'node_modules/', 'build/'],
  collectCoverage: true,
  collectCoverageFrom: [
    '**/*.jsx',
    '!**/coverage/**',
    '!**/node_modules/**',
    '!**/babel.config.js',
    '!**/jest.setup.js',
    '!**/chrome/**'
  ],
  transform: {
    '^.+\\.[t|j]sx?$': 'babel-jest'
  },
  transformIgnorePatterns: [
    '[/\\\\]node_modules[/\\\\](?!' +
      esModules +
      ').+\\.(js|jsx|mjs|cjs|ts|tsx)$'
  ],
  setupFilesAfterEnv: ['<rootDir>/setupTests.js'],
  coverageReporters: ['lcov']
}

module.exports = config
