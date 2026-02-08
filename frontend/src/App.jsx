import { useState, useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap, useMapEvents } from 'react-leaflet'
import axios from 'axios'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import './index.css'

import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

const userIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const customLocationIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const ecoIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

function MapRecenter({ lat, lon }) {
  const map = useMap();
  useEffect(() => {
    map.setView([lat, lon], map.getZoom());
  }, [lat, lon, map]);
  return null;
}

function MapClickHandler({ enabled, onLocationSet }) {
  useMapEvents({
    click(e) {
      if (enabled) {
        onLocationSet({ lat: e.latlng.lat, lon: e.latlng.lng });
      }
    },
  });
  return null;
}

function App() {
  const [location, setLocation] = useState({ lat: 12.923365, lon: 77.501078 })
  const [userLocation, setUserLocation] = useState(null)
  const [customLocation, setCustomLocation] = useState(null)
  const [useCustomLocation, setUseCustomLocation] = useState(false)
  const [pois, setPois] = useState([])
  const [selectedPoi, setSelectedPoi] = useState(null)
  const [routes, setRoutes] = useState([])
  const [selectedRouteIdx, setSelectedRouteIdx] = useState(0)
  const [loading, setLoading] = useState(false)
  const [radius, setRadius] = useState(5)
  const [type, setType] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [searchMode, setSearchMode] = useState('radius')
  const [kValue, setKValue] = useState(3)
  const [locationError, setLocationError] = useState(null)

  const updateUserLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const newLocation = {
            lat: pos.coords.latitude,
            lon: pos.coords.longitude
          }
          setUserLocation(newLocation)
          setLocation(newLocation)
          setLocationError(null)
          console.log('Location updated:', newLocation)
        },
        (err) => {
          console.error('Geolocation error:', err)
          setLocationError(err.message)
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
      )
    } else {
      setLocationError('Geolocation not supported')
    }
  }

  useEffect(() => {
    updateUserLocation()

    let watchId
    if (navigator.geolocation) {
      watchId = navigator.geolocation.watchPosition(
        (pos) => {
          const newLocation = {
            lat: pos.coords.latitude,
            lon: pos.coords.longitude
          }
          setUserLocation(newLocation)
          if (!useCustomLocation) {
            setLocation(newLocation)
          }
          setLocationError(null)
        },
        (err) => console.error('Watch position error:', err),
        { enableHighAccuracy: true, maximumAge: 30000 }
      )
    }

    return () => {
      if (watchId) {
        navigator.geolocation.clearWatch(watchId)
      }
    }
  }, [useCustomLocation])

  useEffect(() => {
    if (useCustomLocation && customLocation) {
      setLocation(customLocation)
    } else if (userLocation) {
      const isOnCampus = (lat, lon) => {
        const CAMPUS_BOUNDS = {
          lat_min: 12.9220,
          lat_max: 12.9250,
          lon_min: 77.4980,
          lon_max: 77.5010
        }
        return (lat >= CAMPUS_BOUNDS.lat_min && lat <= CAMPUS_BOUNDS.lat_max &&
          lon >= CAMPUS_BOUNDS.lon_min && lon <= CAMPUS_BOUNDS.lon_max)
      }

      if (isOnCampus(userLocation.lat, userLocation.lon)) {
        const MAIN_GATE = { lat: 12.924050, lon: 77.500750 }
        console.log('On campus - snapping to Main Gate')
        setLocation(MAIN_GATE)
      } else {
        setLocation(userLocation)
      }
    }
  }, [useCustomLocation, customLocation, userLocation])


  useEffect(() => {
    const timeoutId = setTimeout(() => {
      fetchPois()
    }, 500)
    return () => clearTimeout(timeoutId)
  }, [location, radius, type, searchQuery, searchMode, kValue])

  const fetchPois = async () => {
    setLoading(true)
    try {
      const res = await axios.get(`http://localhost:8000/search`, {
        params: { lat: location.lat, lon: location.lon, type, radius, query: searchQuery, mode: searchMode, k: kValue }
      })
      if (res.data && Array.isArray(res.data.results)) {
        setPois(res.data.results)
      } else if (Array.isArray(res.data)) {
        setPois(res.data)
      } else {
        console.error("API returned unexpected data format:", res.data)
        setPois([])
      }
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  const handlePoiClick = async (poi) => {
    setSelectedPoi(poi)
    setRoutes([])
    setSelectedRouteIdx(0)

    try {
      console.log('Routing from:', location.lat, location.lon, 'to:', poi.lat, poi.lon)
      const res = await axios.get(`http://localhost:8000/route`, {
        params: {
          start_lat: location.lat,
          start_lon: location.lon,
          end_lat: poi.lat,
          end_lon: poi.lon
        }
      })
      console.log('Route response:', res.data)
      setRoutes(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="flex h-screen bg-gray-900 text-white font-sans overflow-hidden">
      <div className="w-1/3 p-6 flex flex-col glass-sidebar z-20 shadow-2xl overflow-hidden">
        <h1 className="text-3xl font-bold mb-2 bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-blue-500">
          SmartPOI Finder
        </h1>
        <p className="text-gray-400 mb-4 text-sm">Discover nearby places intelligently.</p>

        <div className="mb-4 p-3 bg-gray-800/50 border border-gray-700 rounded-lg">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-gray-400">Start Location:</span>
            <button
              onClick={updateUserLocation}
              className="text-xs text-green-400 hover:text-green-300 underline"
              title="Refresh GPS location"
            >
              🔄 Refresh GPS
            </button>
          </div>

          <div className="flex gap-2 mb-2">
            <button
              onClick={() => setUseCustomLocation(false)}
              className={`flex-1 px-2 py-1 text-xs rounded transition-colors ${!useCustomLocation
                ? 'bg-green-600 text-white'
                : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
                }`}
            >
              📍 My Location
            </button>
            <button
              onClick={() => setUseCustomLocation(true)}
              className={`flex-1 px-2 py-1 text-xs rounded transition-colors ${useCustomLocation
                ? 'bg-blue-600 text-white'
                : 'bg-gray-700 text-gray-400 hover:bg-gray-600'
                }`}
            >
              📌 Custom Point
            </button>
          </div>

          {locationError && !useCustomLocation ? (
            <div className="text-xs text-red-400">⚠️ {locationError}</div>
          ) : useCustomLocation && customLocation ? (
            <div className="text-xs text-blue-400">
              📌 {customLocation.lat.toFixed(6)}, {customLocation.lon.toFixed(6)}
            </div>
          ) : useCustomLocation ? (
            <div className="text-xs text-yellow-400">👆 Click map to set start point</div>
          ) : userLocation ? (
            <div className="text-xs text-green-400">
              {location.lat === 12.924050 && location.lon === 77.500750 ? (
                <div>🏫 Main Gate (On Campus)</div>
              ) : (
                <div>✓ {userLocation.lat.toFixed(6)}, {userLocation.lon.toFixed(6)}</div>
              )}
            </div>
          ) : (
            <div className="text-xs text-yellow-400">📍 Getting location...</div>
          )}
        </div>

        <div className="flex flex-col gap-3 mb-4">
          <input
            type="text"
            placeholder="Search places or categories..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="bg-gray-800 border border-gray-700 rounded px-3 py-2 text-sm focus:outline-none focus:border-green-500 w-full"
          />
          <div className="flex gap-2">
            <select
              value={type}
              onChange={(e) => setType(e.target.value)}
              className="bg-gray-800 border border-gray-700 rounded px-3 py-2 text-sm focus:outline-none focus:border-green-500 flex-1"
            >
              <option value="all">All Categories</option>
              <option value="restaurant">Restaurant</option>
              <option value="cafe">Cafe</option>
              <option value="fast_food">Fast Food</option>
              <option value="hospital">Hospital/Clinic</option>
              <option value="pharmacy">Pharmacy</option>
              <option value="school">School</option>
              <option value="college">College</option>
              <option value="mall">Mall/Shop</option>
              <option value="bank">Bank/ATM</option>
              <option value="bus_stop">Bus/Metro</option>
              <option value="park">Park</option>
            </select>
          </div>

          <div className="flex gap-2 items-center">
            <select
              value={searchMode}
              onChange={(e) => setSearchMode(e.target.value)}
              className="bg-gray-800 border border-gray-700 rounded px-3 py-2 text-sm focus:outline-none focus:border-green-500 flex-1"
            >
              <option value="radius">Radius Search</option>
              <option value="knn">Nearest Neighbors</option>
            </select>

            {searchMode === 'radius' ? (
              <div className="flex items-center gap-1 bg-gray-800 border border-gray-700 rounded px-2 py-2">
                <span className="text-xs text-gray-500">R:</span>
                <input
                  type="number"
                  value={radius}
                  onChange={(e) => setRadius(e.target.value)}
                  className="bg-transparent w-10 text-sm focus:outline-none"
                  min="1" max="50"
                />
                <span className="text-xs text-gray-500">km</span>
              </div>
            ) : (
              <div className="flex items-center gap-1 bg-gray-800 border border-gray-700 rounded px-2 py-2">
                <span className="text-xs text-gray-500">K:</span>
                <input
                  type="number"
                  value={kValue}
                  onChange={(e) => setKValue(e.target.value)}
                  className="bg-transparent w-10 text-sm focus:outline-none"
                  min="1" max="20"
                />
              </div>
            )}
          </div>

          <button
            onClick={() => { setType('all'); setSearchQuery(''); setSearchMode('radius'); }}
            className="text-xs text-gray-400 hover:text-white underline self-end"
          >
            Clear Filters
          </button>
        </div>

        <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar">
          {selectedPoi ? (
            <div className="animate-fade-in">
              <button
                onClick={() => setSelectedPoi(null)}
                className="mb-4 text-sm text-green-400 hover:text-green-300 flex items-center gap-1"
              >
                ← Back to List
              </button>
              <h2 className="text-2xl font-semibold mb-1">{selectedPoi.name}</h2>
              <span className="text-xs uppercase tracking-wider text-gray-500 bg-gray-800 px-2 py-1 rounded">{selectedPoi.type}</span>

              <div className="mt-6 space-y-4">
                <h3 className="font-medium text-gray-300">Available Routes</h3>
                {routes.length === 0 ? (
                  <div className="flex items-center gap-2 text-gray-400 p-4 bg-gray-800/30 rounded-lg">
                    <div className="animate-spin h-4 w-4 border-2 border-green-500 border-t-transparent rounded-full"></div>
                    <span>Calculating routes...</span>
                  </div>
                ) : (
                  routes.map((route, idx) => (
                    <div
                      key={idx}
                      onClick={() => setSelectedRouteIdx(idx)}
                      className={`p-4 rounded-lg cursor-pointer transition-all border ${selectedRouteIdx === idx
                        ? 'bg-gray-800 border-green-500 shadow-lg shadow-green-900/20'
                        : 'bg-gray-800/50 border-gray-700 hover:bg-gray-800'
                        }`}
                    >
                      <div className="flex justify-between items-center mb-2">
                        <span className={`font-bold ${route.co2_grams === 0 ? 'text-green-400' : 'text-blue-400'}`}>
                          {route.label}
                        </span>
                        {idx === 0 && <span className="text-xs bg-green-900 text-green-300 px-2 py-0.5 rounded-full">Eco Best</span>}
                      </div>
                      <div className="flex gap-4 text-sm text-gray-300">
                        <div>🕒 {route.duration_min} min</div>
                        <div>📏 {route.distance_km} km</div>
                      </div>
                      <div className="mt-2 text-sm">
                        🌍 <span className={`${route.co2_grams < 100 ? 'text-green-400' : 'text-red-400'}`}>
                          {route.co2_grams} g CO₂
                        </span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          ) : (
            <div className="space-y-2">
              <div className="text-sm text-gray-400 mb-2">Found {pois.length} places nearby</div>
              {pois.map(poi => (
                <div
                  key={poi.id}
                  onClick={() => handlePoiClick(poi)}
                  className="p-3 bg-gray-800/40 hover:bg-gray-800 border border-gray-800 hover:border-gray-600 rounded-lg cursor-pointer transition-colors"
                >
                  <div className="font-medium">{poi.name}</div>
                  <div className="text-xs text-gray-500 capitalize">{poi.type}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="flex-1 z-10 relative">
        <MapContainer center={[location.lat, location.lon]} zoom={13} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <MapRecenter lat={location.lat} lon={location.lon} />
          <MapClickHandler
            enabled={useCustomLocation}
            onLocationSet={setCustomLocation}
          />

          {useCustomLocation && customLocation ? (
            <Marker position={[customLocation.lat, customLocation.lon]} icon={customLocationIcon}>
              <Popup>Custom Start Point</Popup>
            </Marker>
          ) : userLocation ? (
            <Marker position={[location.lat, location.lon]} icon={userIcon}>
              <Popup>
                {location.lat === 12.924050 && location.lon === 77.500750
                  ? "Main Gate (Auto-snapped from campus)"
                  : "Your GPS Location"}
              </Popup>
            </Marker>
          ) : null}

          {pois.map(poi => (
            <Marker
              key={poi.id}
              position={[poi.lat, poi.lon]}
              eventHandlers={{
                click: () => handlePoiClick(poi),
              }}
            >
            </Marker>
          ))}

          {selectedPoi && routes.length > 0 && (
            <Polyline
              positions={routes[selectedRouteIdx].geometry}
              color={routes[selectedRouteIdx].co2_grams === 0 ? '#4ade80' : '#60a5fa'}
              weight={5}
              opacity={0.8}
            />
          )}
        </MapContainer>
      </div>
    </div>
  )
}

export default App
