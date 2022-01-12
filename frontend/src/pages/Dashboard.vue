<template>
  <q-page class="items-center row justify-evenly">
    <h1>Hello {{ userData.full_name }}!</h1>
  </q-page>
</template>
<script setup lang="ts">
import { authorizedApi as api } from 'boot/axios';
import { getUser } from 'boot/auth';

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
</script>
