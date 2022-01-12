<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar class="justify-between constrain">
        <!--
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />
        -->

        <q-avatar>
          <q-img src="~src\assets\UniticLogo.webp" />
        </q-avatar>

        <div>
          <q-btn label="Home" to="/" unelevated />
          <template v-if="!user">
            <q-btn label="Sign In" unelevated to="/signin" />
            <q-btn label="Sign Up" to="/signup" unelevated />
          </template>
          <template v-else>
            <q-btn label="Dashboard" to="/dashboard" unelevated />
            <q-btn label="Logout" unelevated @click="logout" />
          </template>
        </div>
      </q-toolbar>
    </q-header>
    <!--
    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label header> Essential Links </q-item-label>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>
-->
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>
<script setup lang="ts">
import { useRouter } from 'vue-router';
import { getUser } from 'boot/auth';

const router = useRouter();
const user = getUser();

const logout = async () => {
  user.value = '';
  await router.push('/');
};
</script>
