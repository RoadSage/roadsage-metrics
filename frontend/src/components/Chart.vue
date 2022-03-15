<template>
  <div class="q-pa-md">
    <div class="row">
      <q-btn
        class="no-padding"
        flat
        icon="arrow_back"
        @click="changeDateBy(-7)"
      />
      <apexchart
        :options="chartOptions"
        :series="series"
        class="col-11"
        height="350"
        type="scatter"
      />
      <q-btn
        class="no-padding"
        flat
        icon-right="arrow_forward"
        @click="changeDateBy(7)"
      />
    </div>
    <p>
      Showing data from {{ formatDateForUser(dateWeekAgo) }} until
      {{ formatDateForUser(date) }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref, shallowRef, computed, triggerRef, watchEffect } from 'vue';
import { authorizedApi as api } from 'boot/axios';
import { getUser } from 'boot/auth';
import type { Ref } from 'vue';

type GraphData = {
  timestamp: string;
  text_displayed?: string;
  lidar_distance: number;
  ultrasonic_distance: number;
  accelerometer: {
    x: number;
    y: number;
    z: number;
  };
  gyroscope: {
    x: number;
    y: number;
    z: number;
  };
};

const user = getUser();

const chartOptions = {
  chart: {
    height: 350,
    type: 'scatter',
    zoom: {
      type: 'xy',
    },
  },
  dataLabels: {
    enabled: false,
  },
  grid: {
    xaxis: {
      lines: {
        show: true,
      },
    },
    yaxis: {
      lines: {
        show: true,
      },
    },
  },
  xaxis: {
    type: 'datetime',
  },
  yaxis: {
    max: 24,
  },
};

const date = shallowRef(new Date());
const changeDateBy = (days: number) => {
  date.value.setDate(date.value.getDate() + days);
  triggerRef(date);
};
const dateWeekAgo = computed(() => {
  let d = new Date(date.value);
  d.setDate(d.getDate() - 7);
  return d;
});

const formatDate = (date: Date) => {
  let year = date.getFullYear();
  let month = String(date.getMonth() + 1).padStart(2, '0');
  let day = String(date.getDate()).padStart(2, '0');

  return `${year}-${month}-${day}`;
};
const formatDateForUser = (date: Date) => {
  let year = date.getFullYear();
  let month = String(date.getMonth() + 1).padStart(2, '0');
  let day = String(date.getDate()).padStart(2, '0');

  return `${day}/${month}/${year}`;
};

const chartData: Ref<GraphData[]> = ref([]);
watchEffect(async function () {
  chartData.value = await api(user.value)
    .get(
      `/sensor-readings/?from_date=${formatDate(
        dateWeekAgo.value
      )}&to_date=${formatDate(date.value)}`
    )
    .then((response) => response.data as GraphData[]);
});

const calculateGraphPoints = (graphData: GraphData[]) => {
  return graphData.map((reading) => {
    let date = new Date(reading.timestamp);
    let y = date.getHours();
    let x =
      date.getTime() -
      date.getHours() * 60 * 60 -
      date.getMinutes() * 60 -
      date.getSeconds();

    return [x, y];
  });
};

var groupByTextDisplayed = (xs: GraphData[]) => {
  return xs.reduce((groups, record) => {
    (groups[record.text_displayed ?? 'No Message'] =
      groups[record.text_displayed ?? 'No Message'] || []).push(record);
    return groups;
  }, {} as Record<string, GraphData[]>);
};

const series = computed(() =>
  Object.entries(groupByTextDisplayed(chartData.value)).map(
    ([key, values]) => ({
      name: key,
      data: calculateGraphPoints(values),
    })
  )
);
</script>
