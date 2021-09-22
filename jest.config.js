const config = {
  testEnvironment: 'jsdom',
  modulePaths: [
    '<rootDir>'
  ],
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': '<rootDir>/__mocks__/styleMock.js',
    '\\.(gif|ttf|eot|svg)$': '<rootDir>/__mocks__/fileMock.js',
    '(django)': '<rootDir>/__mocks__/djangoMock.js'
  },
  testMatch: [
    '**/*.jest.js',
    '**/*.jest.jsx'
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
  }
}

module.exports = config
