<template>
  <div id="map" style="height: 100vh; width: 100vw;"></div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import leaflet from 'leaflet';

const emit = defineEmits(['points-selected']);
const map = ref(null);
const markers = ref([]);
const routeLine = ref(null);

onMounted(() => {
  map.value = leaflet.map('map').setView([41.3851, 2.1734], 13);

  leaflet.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map.value);

  let step = 0;
  map.value.on('click', (e) => {
    if (markers.value.length >= 2) {
      markers.value.forEach(m => m.remove());
      markers.value = [];
      step = 0;
    }

    const marker = leaflet.marker(e.latlng).addTo(map.value);
    markers.value.push(marker);

    step++;
    if (step === 2) {
      const [origin, destination] = markers.value.map(m => m.getLatLng());
      emit('points-selected', { origin, destination });
    }
  });
});

// 👇 Expose method to parent
function drawRoute(latlngs, color = 'cyan') {
  if (routeLine.value) {
    routeLine.value.remove();
  }

  routeLine.value = leaflet.polyline(latlngs, {
    color: color,
    weight: 5
  }).addTo(map.value);

  map.value.fitBounds(routeLine.value.getBounds(), {
    padding: [30, 30]
  });
}

defineExpose({ drawRoute });

</script>

