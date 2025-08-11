import React, { useEffect } from 'react';
import { useLeafletContext } from '@react-leaflet/core';
import L from 'leaflet';
import { Feature, Point } from 'geojson';
import { Popup, Tooltip } from 'react-leaflet';

interface GeoJsonMarkerProps {
  feature: Feature<Point>;
  categoryIcon?: string;
  children?: React.ReactNode;
  eventHandlers?: Record<string, (e: any) => void>;
}

// Properly type the layer prop for children
interface LayerProps {
  layer: L.Layer;
}

export const makeIcon = (iconUrl?: string): L.Icon => {
  return L.icon({
    iconUrl: iconUrl || '/static/images/map_pin_default.svg',
    shadowUrl: '/static/images/map_shadow_01.svg',
    iconSize: [30, 36],
    iconAnchor: [15, 36],
    shadowSize: [40, 54],
    shadowAnchor: [20, 54],
    popupAnchor: [0, -10]
  });
};

const GeoJsonMarker: React.FC<GeoJsonMarkerProps> = ({ 
  feature, 
  categoryIcon, 
  children,
  eventHandlers
}) => {
  const context = useLeafletContext();
  const coords = React.useMemo(() => 
    [...feature.geometry.coordinates].reverse() as L.LatLngExpression, 
    [feature.geometry.coordinates]
  );
  
  const icon = React.useMemo(() => 
    makeIcon(categoryIcon || feature.properties?.category_icon),
    [categoryIcon, feature.properties?.category_icon]
  );

  const markerRef = React.useRef<L.Marker | null>(null);

  // Create and add marker
  useEffect(() => {
    const marker = L.marker(coords, { icon });
    
    if (eventHandlers) {
      Object.entries(eventHandlers).forEach(([event, handler]) => {
        marker.on(event, handler);
      });
    }

    marker.addTo(context.map);
    markerRef.current = marker;

    return () => {
      marker.remove();
      markerRef.current = null;
    };
  }, []);

  // Update marker position and icon when props change
  useEffect(() => {
    if (markerRef.current) {
      markerRef.current.setLatLng(coords);
      markerRef.current.setIcon(icon);
    }
  }, [coords, icon]);

  // Handle children (popups/tooltips)
  if (!markerRef.current || !children) {
    return null;
  }

  return (
    <>
      {React.Children.map(children, child => {
        if (React.isValidElement(child)) {
          // Special handling for Popup and Tooltip components
          if (child.type === Popup || child.type === Tooltip) {
            return React.cloneElement(child, { 
              position: coords 
            } as React.HTMLAttributes<HTMLElement>);
          }
          return React.cloneElement(child, { 
            layer: markerRef.current 
          } as LayerProps);
        }
        return child;
      })}
    </>
  );
};

export default GeoJsonMarker;