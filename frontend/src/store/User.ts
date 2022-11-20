import { defineStore } from 'pinia';
import { ref } from 'vue';
import { api } from '@/api';
import { getLocalToken, removeLocalToken, saveLocalToken } from '@/utils';

export const useUserStore = defineStore('userState', () => {

  const isLoggedIn = ref(false);
  const token = ref('');

  const loginUser = async (username: string, password: string) => {
    const response = await api.logInGetToken(username, password);
    const apiToken = response.data.access_token;

    if (apiToken) {
      saveLocalToken(apiToken);
      isLoggedIn.value = true;
      token.value = apiToken;
      return true;
    }

    return false;
  }

  return {
    loginUser
  };
});