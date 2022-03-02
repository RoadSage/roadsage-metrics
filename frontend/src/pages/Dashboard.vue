<template>
  <q-page class="row">
    <div class="col-3 dashboardBG">
      <!-- Profile Card Beginning -->
      <div class="row q-mt-xl q-ml-md">
        <div>
          <q-avatar>
            <q-img src="~src\assets\UniticLogo.webp" />
          </q-avatar>
        </div>
        <div class="q-ml-md">
          <p class="text-caption">Account Name</p>
          <p class="text-body2 text-weight-medium">{{ userData.full_name }}</p>
        </div>
      </div>
      <!-- Profile Card End -->

      <div class="q-mt-xl q-ml-md">
        <p class="text-caption">Email</p>
        <div class="row justify-between items-center">
          <p>{{ userData.email }}</p>
          <q-btn class="q-mb-md q-mr-sm" flat>Change</q-btn>
        </div>
      </div>

      <div class="q-mt-xl q-ml-md">
        <p class="text-caption">Password</p>
        <div class="row justify-between items-center">
          <p>*********</p>
          <q-btn class="q-mb-md q-mr-sm" flat>Change</q-btn>
        </div>
      </div>
    </div>

    <div class="col-9">
      <Chart />

      <div class="q-pa-lg">
        <q-table
          title="Messages Displayed"
          :rows="rows"
          :columns="messagesTableColumns"
          row-key="name"
        />
      </div>
    </div>
  </q-page>
</template>
<script lang="ts" setup>
import { authorizedApi as api } from 'boot/axios';
import { getUser } from 'boot/auth';
import Chart from '../components/Chart.vue';

type UserResponse = {
  email: string;
  full_name: string;
  disabled: boolean;
  admin: boolean;
};

const user = getUser();
const userData = await api(user.value)
  .get('/users/me/')
  .then((response) => response.data as UserResponse);

const messagesTableColumns = [
  {
    name: 'message',
    label: 'Message',
    field: 'message',
    sortable: true,
  },
  {
    name: 'times_displayed',
    label: 'Times Displayed',
    field: 'times_displayed',
    sortable: true,
    sort: (a: number, b: number) => Number(a) - Number(b),
  },
];
const rows = await api(user.value)
  .get('/sensor-readings/messages')
  .then((response) =>
    Object.entries(response.data as Record<string, number>).map(
      (message, times_displayed) => ({ message, times_displayed })
    )
  );
</script>
