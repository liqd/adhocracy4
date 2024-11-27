# Map Components Documentation

This document provides an annotated reference to the various custom map
components used in the project. These components leverage the react-leaflet
library, which provides React-friendly abstractions for the popular Leaflet.
js, an open-source library used to create interactive maps. These components
get further customization and extension to cater to the specific
requirements of the project.
They include a variety of features including custom map controls, geometric
layers, markers, pop-up windows, and more. In the following sections, you will
find a brief overview, key functions, and methods for each of these components
which are designed to offer a unique interactivity and to display the data in a
visually appealing and user-friendly manner.

## Components List

* **Map**:
  Main map displaying component, using polygon and map layers defined
  in other components. Also adds zoom functionality.
* **MaplibreGlLayer**:
  Map layer component which uses maplibre-gl-leaflet to
  render maps using vector tiles from an external source.
* **AddMarkerControl**:
  Leaflet Control used for adding a draggable marker to the map
  on click events within certain constraints.
* **GeoJsonMarker**:
  Represents a GeoJSON marker with a custom icon on the
  map, allowing the developer to use JSX for its content.
* **MapPopup**:
  A custom styled Popup component wrapping react-leaflet Popup
  which appears on the map. Might include an image and text.
* **MarkerClusterLayer**:
  Layer component which groups nearby markers into
  clusters for easier visualization and understanding.

For more detailed understanding, dive deeper into individual components and
refer to official documentation
of [react-leaflet](https://react-leaflet.js.org/)
and [Leaflet.js](https://leafletjs.com/reference.html).

## Making non-react leaflet modules into React components

We are using `@react-leaflet/core` to wrap basic Leaflet elements into a react
wrapper. This allows us to use JSX syntax instead of having to do a complicated
mixture of JSX and JS.
You can read more about this method and
examples [here](https://react-leaflet.js.org/docs/core-architecture/).
Examples of those within a4 will be the `AddMarkerControl`, `MaplibreGlLayer`,
`MarkerClusterLayer`, `GeoJsonMarker`.

## Map

This is a Map component which uses the React Leaflet library to create maps. The
map can include polygons and tiles, and supports zoom control. It uses
`react-leaflet`, `MaplibreGlLayer` for tiles rendering, and the GeoJSON feature
to
parse geographical features.

### Props

* **attribution**: This prop is passed to MaplibreGlLayer. It allows you to
  specify an attribution displayed.
* **baseUrl**: This prop is passed to MaplibreGlLayer. It determines the vector
  tiles URL.
* **omtToken**: This prop is passed to MaplibreGlLayer. It's added to the URL
  for tiles in case you need to pass a token.
* **polygon**: This prop is used to generate a polygon on the map. It will be in
  the center of the map.
* **children**: Add any other Components you will need in here. Markers, Popups,
  GeoJSON, [etc](https://react-leaflet.js.org/docs/api-components/).
* ...**rest**: This is a placeholder for all other props, which are passed
  directly to the
  underlying `react-leaflet` [MapContainer component](https://react-leaflet.js.org/docs/api-map/#mapcontainer).
  This means, you can also specify leaflet options in here.

### Accessing Leaflet Instance

If you need to access the leaflet instance directly, you can use a reference to
it like so:

```jsx
const map = useRef();

useEffect(() => {
  if (map.current) {
    // do stuff with map.current
    map.current.panTo([50, 20])
  }
}, [map]);

<Map {...props} ref={map}/>
```

### Building a Map

To build a map you will currently need to pass a baseUrl for it to have access
to a vector tile server. After that you'll either need to specify a `center`
prop to prevent the map from focusing somewhere in the ocean, or pass a polygon
which automatically gets centered. Now you have a map.
If you need to add objects
like [Markers](https://react-leaflet.js.org/docs/api-components/#marker)
you can easily do that:

```jsx
import { Marker } from 'react-leaflet/Marker';


<Map {...props}>
  <Marker {...markerProps} />
</Map>
```

In case you want to build a Marker from GeoJSON you can use the GeoJsonMarker.

## MaplibreGlLayer

This is a `MaplibreGlLayer` component which uses `leaflet`
and `maplibre-gl-leaflet` to render a map layer that can display tiles from an
external services.

### Props

* **baseUrl**: This is the base URL which will be used to fetch the tiles.
* **attribution**: This should be a string that contains the attribution for the
  tile layer.
* **omtToken**: This is an optional token needed to access the tile service at
  the baseUrl.

## AddMarkerControl

This is a Leaflet Control used for adding a draggable marker to the map on click
events. It prevents the marker from being dragged out of a set constraint area,
which is checked using the `checkPointInsidePolygon` helper function.

### Props

* **input**: The input that will receive the GeoJSON position of the newly added
  marker. This has to be an HTMLElement.
* **point**: Optional default marker in GeoJSON

### Defining the limiting polygon

Currently, the area that can have a marker added to it is defined by the polygon
you pass to the `Map` component:

```jsx

<Map polygon={polygonData}> {/* <- this polygon is used as limiting area for the AddMarkerControl */}
  <AddMarkerControl {...props} />
</Map>
```

## GeoJsonMarker

The `GeoJsonMarker` component is a custom marker that represents a GeoJSON
marker with a custom icon on the map.

### Props:

* **feature**: A single GeoJSON feature that the coords will be extracted from
  to generate a Marker
* **...rest**: [Any other option](https://leafletjs.com/reference.html#marker)
  that you could pass to L.marker

### Change the icon

If you find yourself in a situation where you want to change the icon, for example
when you want to highlight a marker that's currently active, you can pass `GeoJsonMarker`
a `icon` prop. You can generate that by using the helper function mentioned below
or call `L.icon` yourself to create an icon instance.

### makeIcon

You can find this utility function in `GeoJsonMarker.js`. It creates and returns
a new Leaflet Icon instance with the provided iconUrl, or default icon if no URL
is provided.

## MapPopup

This component wraps the react-leaflet Popup component and adds custom styling
and behavior. It provides the same css classes as previous jQuery Maps.

### Props

* **feature**: A single GeoJSON feature, if it has an image
  in `feature.properties.image` it displays that.
* **className**: Any additional classes you want to pass to the outmost `div`.
* **children**: The content you want to render inside. It will be
  within `.maps-popups-popup-text-content`.
* **...rest**: [Any other option](https://react-leaflet.js.org/docs/api-components/#popup)
  that you could pass to `Popup`

## MarkerClusterLayer

The `MarkerClusterLayer` is a layer component that groups close markers together
into clusters. It uses the `leaflet.markercluster` plugin for Leaflet.

### Usage

```jsx

<Map {...props}>
  <MarkerClusterLayer>
    <GeoJsonMarker feature={feature}/>
    <GeoJsonMarker feature={feature2}/>
  </MarkerClusterLayer>
</Map>
```


## Examples for Maps

### Map with one or more markers.

If there are more than one marker, it also adds the `ClusterLayer`.

```jsx
const MapWithMarkers = ({ points, withoutPopup, ...props }) => {
  const markers = points.map((feature) => (
    <GeoJsonMarker key={feature.id} feature={feature}>
      {!withoutPopup && <IdeaPopup feature={feature}/>}
    </GeoJsonMarker>
  ))
  return (
    <Map
      {...props}
    >
      {points.length > 1 ?
        <MarkerClusterLayer>{markers}</MarkerClusterLayer> : markers}
    </Map>
  )
}
```

### Map for allowing users to set a point

This sets the value after each marker update in `valueInputEl` and if there is
a `point` prop present, this will be the initial value.

```jsx
<Map {...props.map}>
  <AddMarkerControl input={valueInputEl} point={props.map.point}/>
</Map>
```
