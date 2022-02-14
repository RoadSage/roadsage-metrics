import { ref, watch, inject } from 'vue';
import type { Ref } from 'vue';
import { Cookies } from 'quasar';
import { boot } from 'quasar/wrappers';
import GoogleAuth from './googleAuth';

// TODO: Get better way for changing this
const GOOGLE_CLIENT_ID =
  '829462298080-qus8dgp18ajuhfi2onhs51ks56c1m1q8.apps.googleusercontent.com';

export default boot(({ app }) => {
  // Set up Google Signin
  app.use(GoogleAuth, {
    clientId: GOOGLE_CLIENT_ID,
    scope: 'email',
    prompt: 'consent',
    fetch_basic_profile: false,
  });

  // Set up cookie to store token
  const userCookie: string | null = Cookies.get('user');
  const user = ref(userCookie ?? '');

  app.provide('user', user);
  watch(user, (value) => Cookies.set('user', value));
});

export const getUser = (): Ref<string> => inject('user', ref(''));
