import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import { fileURLToPath } from 'url'

// List of modules to transform (same as Jest config)
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

export default defineConfig({
  plugins: [react()],
  resolve: {
    // Module name mappings
    alias: [
      {
        find: "leaflet",
        replacement: fileURLToPath(new URL('./tests/__mocks__/leaflet.ts', import.meta.url))
      },
      {
        find: "django",
        replacement: fileURLToPath(new URL('./tests/__mocks__/django.ts', import.meta.url))
      },
      {
        find: /\.(css|less|scss|sass)$/,
        replacement: '<rootDir>/__mocks__/styleMock.js'
      },
      {
        find: /\.(gif|ttf|eot|svg)$/,
        replacement: '<rootDir>/__mocks__/fileMock.js'
      }
    ]
  },
  assetsInclude: ['**/*.js'], // Explicitly declare JS assets
  optimizeDeps: {
    exclude: [
       esModules,
      'i18n_catalog.js'
    ]
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./setupTests.ts'],
    
    // Match Jest's test patterns
    include: [
      '**/*.jest.{js,jsx,ts,tsx}',
      '**/*.test.{js,jsx,ts,tsx}'
    ],
    exclude: [
      '**/venv/**',
      '**/site-packages/**',
      '**/templates/**',
      '**/*.templated.js',
      '**/i18n_catalog.js',
      'venv/**',
      'node_modules/**',
      'build/**',
      '**/i18n_catalog.js'
    ],
    
    // Coverage configuration
    coverage: {
      enabled: true,
      provider: 'istanbul',
      reporter: ['lcov'],
      include: ['**/*.{js,jsx,ts,tsx}'],
      exclude: [
        '**/coverage/**',
        '**/node_modules/**',
        '**/babel.config.js',
        '**/vitest.config.ts',
        '**/chrome/**',
        '**/*.d.ts'
      ]
    },
  }
})