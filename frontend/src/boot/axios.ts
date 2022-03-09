/*
  URL Address of the Backend API

  All requests in the application will be made to the backend API at this address.
  The typical development enviroment will have the fastAPI backend running at: 'http://localhost:8000'.
  When deployed to a server, the backend API will be running at a different address and this variable needs to be updated.
*/
const BACKEND_URL = 'http://localhost:8000';

import { boot } from 'quasar/wrappers';
import axios, { AxiosInstance } from 'axios';

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
  }
}

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const api = axios.create({ baseURL: BACKEND_URL });

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios;
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
});

const authorizedApi = (token: string) =>
  axios.create({
    baseURL: BACKEND_URL,
    headers: { Authorization: `Bearer ${token}` },
  });

export { api, authorizedApi };
