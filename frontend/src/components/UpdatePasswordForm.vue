<template>
  <q-form class="q-px-sm" @submit.prevent="submit">
    <h2 class="text-h6">Update Password</h2>

    <q-input
      v-model="newPassword"
      class="full-width"
      filled
      :type="isPwdVisible ? 'password' : 'text'"
      label="New Password"
      hint="Please enter your new password"
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
      v-model="confirmNewPassword"
      class="full-width"
      filled
      :type="isPwdConfirmedVisible ? 'password' : 'text'"
      label="Confirm New Password"
      hint="Please confirm your new password"
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
      style="width: 100%"
      label="Change"
      type="submit"
      color="accent"
      class="full-width q-mt-lg"
    />
  </q-form>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { getUser } from 'src/boot/auth';
import { authorizedApi as api } from 'boot/axios';

const emits = defineEmits(['submit']);

const user = getUser();

const newPassword = ref('');
const confirmNewPassword = ref('');
const isPwdVisible = ref(true);
const isPwdConfirmedVisible = ref(true);

const submit = async () => {
  if (newPassword.value != confirmNewPassword.value) {
    alert("Passwords don't match. please check and try again.");
    return;
  }

  try {
    await api(user.value).put('/users/me/update-password', {
      new_password: newPassword.value,
    });
    emits('submit');
    alert('Password changed successfully');
  } catch (error: unknown) {
    console.log(error);
    alert('Password change failed, please try again. Password not updated');
  }
};

const requiredRule = (value: string): boolean | string => {
  if (value) {
    return true;
  } else {
    return '* Required';
  }
};
</script>
