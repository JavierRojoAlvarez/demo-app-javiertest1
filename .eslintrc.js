module.exports = {
  env: {
    browser: true,
    es2021: true
  },
  extends: 'standard',
  overrides: [
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  rules: {
    'semi': ['error', 'always'],
    'object-curly-spacing': ['error', 'never'],
    'space-before-function-paren': 'off',
    'quote-props': ['error', 'consistent'],
    'space-infix-ops': 'off',
    'no-new': 'off',
    'comma-dangle': ['error', 'only-multiline'],
  }
};
