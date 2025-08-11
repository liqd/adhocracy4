import { vi } from "vitest";

const mockDjango = {
  gettext: vi.fn((text) => text),
  pgettext: vi.fn((context, text) => text),
  ngettext: vi.fn((singular, plural, count) => count === 1 ? singular : plural),
  interpolate: vi.fn((fmt, data) => fmt)
};
export default mockDjango;