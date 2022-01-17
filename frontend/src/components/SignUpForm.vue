<template>
  <div class="q-pl-xl col-8 large-screen-only" style="max-width: 400px">
    <q-form
      class="q-gutter-md column items-center content-start sign-in-box q-px-xl"
    >
      <h1 class="text-headerColor text-h4">Sign Up</h1>
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
        :type="isPwdConfirmedVisible ? 'password' : 'text'"
        label="Password"
        hint="Please enter your password"
        :rules="[requiredRule]"
      >
        <template v-slot:append>
          <q-icon
            :name="isPwdConfirmedVisible ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPwdConfirmedVisible = !isPwdConfirmedVisible"
          />
        </template>
      </q-input>

      <q-btn
        no-caps
        label="Sign Up"
        type="submit"
        color="accent"
        class="full-width"
      />
      <div>
        <q-checkbox
          color="accent"
          v-model="termsConditions"
          label="I Accept the Terms and Conditions"
        />
      </div>
      <q-separator class="bg-primary full-width" />
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
      confirmPassword: ref(''),
      email: ref(''),
      fullName: ref(''),
      isPwdVisible: ref(true),
      isPwdConfirmedVisible: ref(true),
      termsConditions: ref(false),

      requiredRule(value) {
        if (value) {
          return true;
        } else {
          return '* Required';
        }
      },
    };
  },
};
</script>
