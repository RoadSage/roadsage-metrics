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

      <SelectUser v-if="userData.admin" v-model="selectedUser" />
    </div>

    <div class="col-9">
      <h2 v-if="userData.admin && selectedUser" class="text-h5 q-pl-xl">
        Viewing data for user: {{ selectedUser }}
      </h2>
      <Chart :selected-user="selectedUser" />

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
import { ref, type Ref, watchEffect } from 'vue';
import { authorizedApi as api } from 'boot/axios';
import { getUser } from 'boot/auth';
import Chart from '../components/Chart.vue';
import SelectUser from '../components/SelectUser.vue';

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

const selectedUser = ref('');

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

const rows: Ref<{ message: string; times_displayed: number }[]> = ref([]);
watchEffect(async function () {
  let userQuery = '';
  if (selectedUser.value) {
    userQuery = `?user=${selectedUser.value}`;
  }
  rows.value = await api(user.value)
    .get(`/sensor-readings/messages${userQuery}`)
    .then((response) =>
      Object.entries(response.data as Record<string, number>).map(
        ([message, times_displayed]) => ({ message, times_displayed })
      )
    );
});
</script>
