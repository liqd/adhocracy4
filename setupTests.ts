import '@testing-library/jest-dom'
import { vi } from 'vitest'


/// <reference types="@vitest/browser/context" />

if (typeof window.URL.createObjectURL === 'undefined') {
  window.URL.createObjectURL = () => {}
}

// Mock Django global functions
vi.stubGlobal('django', {
  gettext: vi.fn((text) => text),
  pgettext: vi.fn((context, text) => `[${context}]${text}`),
  ngettext: vi.fn((singular, plural, count) => count === 1 ? singular : plural),
  interpolate: vi.fn((fmt, data) => fmt)
})