export default {
  '*.{js,jsx,ts,tsx}': [
    'eslint'
  ],
  '*.{ts,tsx}': [
    () => 'tsc --noEmit'
  ],
  '*.scss': [
    'stylelint'
  ],
  '*.py': [
    'make lint-python-files'
  ]
}
