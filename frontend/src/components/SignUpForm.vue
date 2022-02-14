<template>
  <div class="q-pl-xl col-8 large-screen-only" style="max-width: 400px">
    <q-form
      class="q-gutter-md column items-center content-start sign-in-box q-px-xl"
      @submit.prevent="signup"
    >
      <h1 class="text-headerColor text-h4">Sign Up</h1>

      <q-banner class="text-white bg-primary" v-if="errorMessage">
        {{ errorMessage }}
        <template #action>
          <q-btn
            flat
            color="white"
            label="Dismiss"
            @click="errorMessage = ''"
          />
        </template>
      </q-banner>

      <q-input
        filled
        v-model="fullName"
        class="full-width"
        label="Full Name"
        hint="Please enter your Full Name"
        :rules="[requiredRule]"
      />
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

      <q-input
        v-model="confirmPassword"
        class="full-width"
        filled
        :type="isPwdVisible ? 'password' : 'text'"
        label="Password Confirmation"
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
      <div>
        <q-checkbox
          color="accent"
          v-model="termsConditions"
          label="I Accept the Terms and Conditions"
        />
      </div>
      <q-btn
        no-caps
        label="Sign Up"
        type="submit"
        color="accent"
        class="full-width"
      />
      <GoogleSignInButtonVue />

      <q-separator class="bg-primary full-width" />
      <p class="text-primary text-h6 q-mr-md">FROM</p>
      <img src="~src\assets\formImage.webp" />
    </q-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import axios from 'axios';
import { api } from 'boot/axios';
import { getUser } from 'boot/auth';

import GoogleSignInButtonVue from './GoogleSignInButton.vue';

type LoginResponse = {
  access_token: string;
  token_type: string;
};

const router = useRouter();
const user = getUser();

const fullName = ref('');
const email = ref('');

const password = ref('');
const confirmPassword = ref('');
const isPwdVisible = ref(false);
const termsConditions = ref(false);

const requiredRule = (value: string) => {
  if (value) {
    return true;
  } else {
    return '* Required';
  }
};

type ErrorMessage = {
  detail: string;
};

const errorMessage = ref('');
const signup = async () => {
  errorMessage.value = '';

  if (!termsConditions.value) {
    errorMessage.value = 'Please accept the terms and conditions';
  } else if (password.value !== confirmPassword.value) {
    errorMessage.value =
      "Password and Password Confirmation don't match please check and try again.";
  } else {
    try {
      const response = await api.post('/signup', {
        email: email.value,
        password: password.value,
        full_name: fullName.value,
      });

      user.value = (response.data as LoginResponse).access_token;
      await router.push('/dashboard');
    } catch (error) {
      if (
        axios.isAxiosError(error) &&
        error.response &&
        error.response.status === 409
      ) {
        errorMessage.value = (error.response.data as ErrorMessage).detail;
      } else {
        errorMessage.value =
          'Problem creating an account, please check your details and try again.';
      }
    }
  }
};
</script>
