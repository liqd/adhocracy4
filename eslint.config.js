import js from '@eslint/js'
import importX from 'eslint-plugin-import-x'
import jsxA11y from 'eslint-plugin-jsx-a11y'
import n from 'eslint-plugin-n'
import promise from 'eslint-plugin-promise'
import react from 'eslint-plugin-react'
import reactHooks from 'eslint-plugin-react-hooks'
import jest from 'eslint-plugin-jest'
import globals from 'globals'

export default [
  js.configs.recommended,
  importX.configs['flat/recommended'],

  {
    plugins: {
      'jsx-a11y': jsxA11y,
    },
    rules: jsxA11y.configs.recommended.rules,
  },

  n.configs['flat/recommended'],
  n.configs['flat/recommended'],
  promise.configs['flat/recommended'],
  react.configs.flat.recommended,
  reactHooks.configs.flat.recommended,

  {
    files: ['**/*.jest.js', '**/*.jest.jsx'],
    ...jest.configs['flat/recommended'],
  },

  {
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.commonjs,
        ...globals.es2021,
        ...globals.jquery,
      },
    },
    settings: {
      react: {
        version: 'detect',
      },
      'import-x/core-modules': ['django'],
      'import-x/resolver': {
        node: {
          extensions: ['.js', '.jsx'],
          moduleDirectory: ['node_modules', 'node_modules/.pnpm'],
        },
      },
    },
    rules: {
      'jsx-quotes': ['error', 'prefer-double'],
      'jsx-a11y/no-onchange': 'off',
      'react/prop-types': 'off',
      'n/no-missing-require': 'off',
      'n/no-unsupported-features/es-syntax': 'off',
      'n/no-unsupported-features/node-builtins': 'off',
      'n/no-missing-import': 'off',
      'n/no-unpublished-import': 'off',
      'n/no-extraneous-import': 'off',
      'import-x/named': 'off',
      'no-unused-vars': 'warn',
      'jest/valid-title': 'off',
      'jest/no-identical-title': 'off',
      'jest/no-export': 'off',
      'react-hooks/refs': 'off',
      'no-restricted-syntax': ['error', 'TemplateLiteral'],
    },
  },

  {
    files: ['**/*.jest.js', '**/*.jest.jsx', '**/__mocks__/*.js'],
    languageOptions: {
      globals: {
        ...globals.jest,
      },
    },
  },

  {
    ignores: ['node_modules/', 'venv/'],
  },
]
