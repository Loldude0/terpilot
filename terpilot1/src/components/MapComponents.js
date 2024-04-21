import React from 'react';
import { GoogleMap, MarkerF } from '@react-google-maps/api';
import mapStyles from '../mapStyles';
import mapIcon from "./red_turtle.png"; 


const mapContainerStyle = {
  width: '100%', // Adjusted for full width for better visibility
  height: '400px', // Increased height for better visibility
};

const options = {
  styles: mapStyles,
  disableDefaultUI: true,
  zoomControl: true,
};

const MapComponent = ({ locations }) => {
  console.log("Locations:", locations); // Debugging line
  const center = { lat: 38.987886, lng: -76.942994 }; // Updated for clarity

  return (
    <GoogleMap
      mapContainerStyle={mapContainerStyle}
      zoom={15} // Increased zoom for closer view
      center={center}
      options={options}
    >
      {locations.map((location, index) => (
        <MarkerF
          key={index}
          position={{ lat: parseFloat(location.lat), lng: parseFloat(location.lng) }}
          label={location.name}
          icon={{
            url: mapIcon,
            scaledSize: new window.google.maps.Size(30, 30), // Adjust size as needed
            origin: new window.google.maps.Point(0,0),
            
          }}
        />
      ))}
    </GoogleMap>
  );
};

export default MapComponent;