<template>
  <div class="q-pa-md">
    <q-carousel
      v-model="slide"
      animated
      arrows
      class="q-pa-md"
      control-color="primary"
      infinite
    >
      <q-carousel-slide :name="1">
        <apexchart
          :options="chartOptions"
          :series="series"
          height="350"
          type="scatter"
        ></apexchart>
      </q-carousel-slide>
      <q-carousel-slide :name="2">
        <apexchart
          :options="chartOptions"
          :series="series"
          height="350"
          type="scatter"
        ></apexchart>
      </q-carousel-slide>
      <q-carousel-slide :name="3">
        <apexchart
          :options="chartOptions"
          :series="series"
          height="350"
          type="scatter"
        ></apexchart>
      </q-carousel-slide>
      <q-carousel-slide :name="4">
        <apexchart
          :options="chartOptions"
          :series="series"
          height="350"
          type="scatter"
        ></apexchart>
      </q-carousel-slide>
    </q-carousel>
  </div>
</template>

<script>
function generateDayWiseTimeSeries(baseval, count, yrange) {
  var i = 0;
  var series = [];
  while (i < count) {
    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
    var x = baseval;
    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
    var y =
      // eslint-disable-next-line @typescript-eslint/restrict-plus-operands,@typescript-eslint/no-unsafe-member-access
      Math.floor(Math.random() * (yrange.max - yrange.min + 1)) +
      // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
      yrange.min;

    series.push([x, y]);
    baseval += 86400000;
    i++;
  }
  return series;
}

import { ref } from 'vue';

export default {
  name: 'mychart',
  data() {
    return {
      series: [
        {
          name: 'TEAM 1',
          // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment,@typescript-eslint/no-unsafe-call
          data: generateDayWiseTimeSeries(
            new Date('11 Feb 2017 GMT').getTime(),
            7,
            {
              min: 0,
              max: 24,
            }
          ),
        },
      ],
      chartOptions: {
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
      },
    };
  },
  setup() {
    return {
      slide: ref(1),
    };
  },
};
</script>
