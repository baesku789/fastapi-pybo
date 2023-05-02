import { writable } from "svelte/store";

const persistance_storage = (key, initValue) => {
  const storedValue = localStorage.getItem(key);

  const store = writable(storedValue ? JSON.parse(storedValue) : initValue);
  store.subscribe((val) => {
    localStorage.setItem(key, JSON.stringify(val));
  });

  return store;
};

export const page = persistance_storage("page", 0);
export const keyword = persistance_storage("keyword", "");
export const access_token = persistance_storage("access_token", "");
export const username = persistance_storage("username", "");
export const is_login = persistance_storage("is_login", false);
