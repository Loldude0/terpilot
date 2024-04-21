import React from 'react';
import { GoogleMap, Marker } from '@react-google-maps/api';
import mapStyles from '../mapStyles';
const mapContainerStyle = {
  width: '50vw',
  height: '50vh',
};

const options = {
  styles: mapStyles,
  disableDefaultUI: true,
  zoomControl: true,
};

// Component to display Google Maps with multiple markers
const MapComponent = ({ locations }) => {
  // locations: [{"name":"251 North", "lng": -76.9496090325357, "lat": 38.99274005}, {"name": "94th Aero Squadron", "lng": -76.9210122711411, "lat": 38.9781702}]
  // I will add the center of UMD later
  // 38.987886156592246, -76.94299360133668
  const center = { lat: 38.987886156592246, lng: -76.94299360133668 };
  console.log(center);
  return (
    <GoogleMap
      mapContainerStyle={mapContainerStyle}
      zoom={12}
      center={center}
      options = {options}
    >
      {locations.map((loc, index) => (
        <Marker
          key={index}
          position={{ lat: parseFloat(loc.lat), lng: parseFloat(loc.lng) }}
          label={loc.name}
        />
      ))}


    </GoogleMap>
  );
};

export default MapComponent;