const config = {
  testEnvironment: 'jsdom',
  modulePaths: [
    '<rootDir>'
  ],
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': '<rootDir>/__mocks__/styleMock.js',
    '\\.(gif|ttf|eot|svg)$': '<rootDir>/__mocks__/fileMock.js',
    '(django)': '<rootDir>/__mocks__/djangoMock.js',
    'react-flip-move': '<rootDir>/__mocks__/flipmoveMock.js'
  },
  testMatch: [
    '**/*.jest.js',
    '**/*.jest.jsx'
  ],
  testPathIgnorePatterns: [
    'venv/',
    'node_modules/',
    'build/'
  ],
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
    'node_modules/(?!(@?react-leaflet)/)'
  ],
  setupFiles: ['<rootDir>/setupTests.js'],
  coverageReporters: ['lcov']
}

module.exports = config
