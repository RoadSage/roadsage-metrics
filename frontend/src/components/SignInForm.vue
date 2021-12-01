<template>
  <div class="q-pl-xl col-8 large-screen-only" style="max-width: 400px">
    <q-form
      class="q-gutter-md column items-center content-start sign-in-box q-px-xl"
    >
      <h1 class="text-headerColor text-h4">Sign In</h1>
      <q-input
        filled
        type="email"
        v-model="email"
        class="full-width"
        label="Email"
        hint="Please enter your email"
      />
      <q-input
        v-model="password"
        class="full-width"
        filled
        :type="isPwdVisible ? 'password' : 'text'"
        label="Password"
        hint="Please enter your password"
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

<script>
import { ref } from 'vue';

export default {
  setup() {
    return {
      password: ref(''),
      email: ref(''),
      isPwdVisible: ref(true),
      rememberMe: ref(false),
    };
  },
};
</script>
