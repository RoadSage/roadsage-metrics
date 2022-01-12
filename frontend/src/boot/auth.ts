import { boot } from 'quasar/wrappers';
import { ref, watch, inject } from 'vue';
import type { Ref } from 'vue';
import { Cookies } from 'quasar';

export default boot(({ app }) => {
  const userCookie: string | null = Cookies.get('user');
  const user = ref(userCookie ?? '');

  app.provide('user', user);
  watch(user, (value) => Cookies.set('user', value));
});

export const getUser = (): Ref<string> => inject('user', ref(''));
