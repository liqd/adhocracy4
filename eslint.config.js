import js from '@eslint/js'
import importX from 'eslint-plugin-import-x'
import jsxA11y from 'eslint-plugin-jsx-a11y'
import n from 'eslint-plugin-n'
import promise from 'eslint-plugin-promise'
import react from 'eslint-plugin-react'
import reactHooks from 'eslint-plugin-react-hooks'
import jest from 'eslint-plugin-jest'
import globals from 'globals'
import tsParser from '@typescript-eslint/parser'
import tsPlugin from '@typescript-eslint/eslint-plugin'

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
          extensions: ['.js', '.jsx', '.ts', '.tsx'],
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
    },
  },

  {
    files: ['**/*.ts', '**/*.tsx'],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
      },
    },
    plugins: {
      '@typescript-eslint': tsPlugin,
    },
    rules: {
      ...tsPlugin.configs.recommended.rules,
      'no-unused-vars': 'off',
      'no-undef': 'off',
      '@typescript-eslint/no-unused-vars': ['warn', {
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_',
      }],
      '@typescript-eslint/no-explicit-any': 'off',
    },
  },

  {
    files: ['**/*.jest.js', '**/*.jest.jsx', '**/*.jest.ts', '**/*.jest.tsx', '**/__mocks__/*.js'],
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
