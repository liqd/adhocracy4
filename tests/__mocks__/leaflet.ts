// __mocks__/leaflet.ts
import { vi } from 'vitest';

export const mockControl = vi.fn().mockImplementation(() => ({
  addTo: vi.fn().mockReturnThis(),
  onRemove: vi.fn(),
  getContainer: vi.fn()
}));

export const mockMarker = vi.fn().mockImplementation(() => ({
  addTo: vi.fn().mockReturnThis(),
  setLatLng: vi.fn(),
  on: vi.fn(),
  off: vi.fn(),
  remove: vi.fn(),
  toGeoJSON: vi.fn().mockReturnValue({ type: 'Feature' }),
  getLatLng: vi.fn().mockReturnValue({ lat: 0, lng: 0 })
}));

export const mockGeoJSON = vi.fn().mockReturnValue({
  eachLayer: vi.fn(),
  getLayers: vi.fn()
});

const mockLatLng = vi.fn((lat, lng) => ({ lat, lng }));

export default {
  Control: mockControl,
  marker: mockMarker,
  geoJSON: mockGeoJSON,
  latLng: mockLatLng,
  Icon: vi.fn() // Simple mock for Icon
};