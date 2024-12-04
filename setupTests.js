// fix missing TextEncoder / TextDecocer in jsdom
// this can be removed once https://github.com/jsdom/jsdom/pull/3791 was merged
if (!globalThis.TextEncoder || !globalThis.TextDecoder) {
  const { TextDecoder, TextEncoder } = require('node:util')
  globalThis.TextEncoder = TextEncoder
  globalThis.TextDecoder = TextDecoder
}
