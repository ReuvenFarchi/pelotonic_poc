<template>
  <MapView ref="mapView" @points-selected="handlePointsSelected" />
</template>

<script setup>
import { ref, nextTick } from 'vue';
import MapView from './components/MapView.vue';

const mapView = ref(null);

const handlePointsSelected = async ({ origin, destination }) => {
  const originStr = `${origin.lat},${origin.lng}`;
  const destinationStr = `${destination.lat},${destination.lng}`;

  try {
    const res = await fetch(`http://localhost:8000/route?origin=${originStr}&destination=${destinationStr}`);
    const data = await res.json();

    const path = data.routes[0].path;  // Already in [[lat, lng], ...] format

    await nextTick();

    if (mapView.value) {
      mapView.value.drawRoute(path, 'cyan');  // single route, color: cyan
    } else {
      console.warn('MapView ref not ready yet.');
    }
  } catch (err) {
    console.error('Failed to fetch or draw route:', err);
  }
};
</script>



<style>
body {
  margin: 0;
  font-family: sans-serif;
}
#app {
  height: 100vh;
  overflow: hidden;
}
</style>
