<template>
  <div class="q-pl-xl col-8 large-screen-only" style="max-width: 400px">
    <q-form
      class="items-center content-start q-gutter-md column sign-in-box q-px-xl"
      @submit.prevent="login"
    >
      <h1 class="text-headerColor text-h4">Sign In</h1>

      <q-banner class="text-white bg-primary" v-if="hadError">
        Problem signing in, please check your details and try again.
        <template #action>
          <q-btn flat color="white" label="Dismiss" @click="hadError = false" />
        </template>
      </q-banner>

      <q-input
        filled
        type="email"
        v-model="email"
        class="full-width"
        label="Email"
        hint="Please enter your email"
        :rules="[requiredRule]"
      />
      <q-input
        v-model="password"
        class="full-width"
        filled
        :type="isPwdVisible ? 'password' : 'text'"
        label="Password"
        hint="Please enter your password"
        :rules="[requiredRule]"
      >
        <template v-slot:append>
          <q-icon
            :name="isPwdVisible ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPwdVisible = !isPwdVisible"
          />
        </template>
      </q-input>

      <q-btn
        no-caps
        style="width: 100%"
        label="Sign In"
        type="submit"
        color="accent"
        class="full-width"
      />

      <div>
        <q-checkbox color="accent" v-model="rememberMe" label="Remember Me" />
      </div>
      <q-separator class="bg-primary full-width" />
      <p class="items-center">You don't have an account?</p>
      <q-btn
        no-caps
        outline
        color="accent"
        label="Sign Up Now"
        class="q-px-xl full-width"
        to="/signup"
      />
      <p class="text-primary text-h6 q-mr-md">FROM</p>
      <img src="~src\assets\formImage.webp" />
    </q-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useQuasar } from 'quasar';
import { useRouter } from 'vue-router';

import { api } from 'boot/axios';
import { getUser } from 'boot/auth';

type LoginResponse = {
  access_token: string;
  token_type: string;
};

const $q = useQuasar();
const router = useRouter();
const user = getUser();

const remeberedEmail = $q.cookies.get('rememberedEmail');

const requiredRule = (value) => {
  if (value) {
    return true;
  } else {
    return '* Required';
  }
};

const email = ref(remeberedEmail || '');
const password = ref('');
const isPwdVisible = ref(true);
const rememberMe = ref(!!remeberedEmail);

const hadError = ref(false);
const login = async () => {
  hadError.value = false;
  $q.cookies.set('rememberedEmail', rememberMe.value ? email.value : '');

  try {
    // OAuth spec says that the login information must be sent as URL Encoded FormData
    const formData = new URLSearchParams({
      username: email.value, // OAuth spec expects a username (even though its an email)
      password: password.value,
    });

    const response = await api.post('/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });

    user.value = (response.data as LoginResponse).access_token;
    await router.push('/dashboard');
  } catch {
    hadError.value = true;
  }
};
</script>
