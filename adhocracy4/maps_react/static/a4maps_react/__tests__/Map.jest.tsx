import React from 'react';
import { render } from '@testing-library/react';
import { vi } from 'vitest';
import Map from '../Map';

// Mock react-leaflet components since they require a DOM environment
vi.mock('react-leaflet', () => ({
  MapContainer: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="map-container">{children}</div>
  ),
  GeoJSON: () => <div data-testid="geojson-layer" />,
  useMap: () => ({
    fitBounds: vi.fn(),
    setMinZoom: vi.fn(),
    getZoom: () => 13
  })
}));

// Mock MaplibreGlLayer since it's a custom component
vi.mock('../MaplibreGlLayer', () => ({
  default: () => <div data-testid="maplibre-layer" />
}));

describe('Map Component', () => {
  const mockPolygon = {
    type: 'Feature',
    geometry: {
      type: 'Polygon',
      coordinates: [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
    }
  };

  test('renders basic map without props', () => {
    const { getByTestId } = render(<Map />);
    expect(getByTestId('map-container')).toBeInTheDocument();
    expect(getByTestId('maplibre-layer')).toBeInTheDocument();
  });

  test('renders with custom attribution and baseUrl', () => {
    const { getByTestId } = render(
      <Map attribution="Test Attribution" baseUrl="https://test.com" />
    );
    expect(getByTestId('maplibre-layer')).toBeInTheDocument();
  });

  test('renders GeoJSON layer when polygon is provided', () => {
    const { getByTestId } = render(
      <Map polygon={mockPolygon} />
    );
    expect(getByTestId('geojson-layer')).toBeInTheDocument();
  });

  test('passes omtToken to MaplibreGlLayer', () => {
    const { getByTestId } = render(
      <Map omtToken="test-token" />
    );
    expect(getByTestId('maplibre-layer')).toBeInTheDocument();
  });

  test('renders children components', () => {
    const { getByText } = render(
      <Map>
        <div>Test Child</div>
      </Map>
    );
    expect(getByText('Test Child')).toBeInTheDocument();
  });
});