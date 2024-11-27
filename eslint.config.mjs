import globals from "globals";
import hooksPlugin from "eslint-plugin-react-hooks";
import importPlugin from "eslint-plugin-import";
import jsxA11y from "eslint-plugin-jsx-a11y";
import pluginJest from "eslint-plugin-jest";
import pluginJs from "@eslint/js";
import neostandard, { plugins } from "neostandard";

export default [
    ...neostandard(),
    jsxA11y.flatConfigs.recommended,
    importPlugin.flatConfigs.recommended,
    {
        files: ["**/*.{js,mjs,cjs,jsx,mjsx,ts,tsx,mtsx,jest.jsx,jest.js}"],
        ignores: ["node_modules/", "venv/", "static/"],
        languageOptions: {
            ...jsxA11y.flatConfigs.recommended.languageOptions,
            globals: {
                ...globals.browser,
                ...pluginJest.environments.globals.globals,
                ...globals.jquery,
            },
            ecmaVersion: "latest",
            parserOptions: {
                ecmaFeatures: {
                    jsx: true,
                    "experimentalObjectRestSpread": true,
                },
            },
        },
        plugins: {
            jest: pluginJest,
            "react-hooks": hooksPlugin,
        },
        rules: {
            "no-restricted-syntax": ["error", "TemplateLiteral"],
            "jsx-a11y/no-onchange": "off",
            "@stylistic/jsx-quotes": [2, "prefer-double"],
            ...hooksPlugin.configs.recommended.rules,
        },
        settings: {
            "import/core-modules": ["django"],
            "import/resolver": {
                node: {
                    extensions: [".js", ".jsx"],
                },
            },
        },
    },
];
