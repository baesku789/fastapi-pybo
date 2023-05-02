import qs from "qs";
import { push } from "svelte-spa-router";
import { get } from "svelte/store";
import { access_token, is_login, username } from "./store";

export const fastapi = (
  operation,
  url,
  params,
  sucessCallback,
  failureCallback
) => {
  let method = operation;
  let _url = import.meta.env.VITE_SERVER_URL + url;
  let contentType = "application/json";
  let body = JSON.stringify(params);

  if (operation === "login") {
    method = "post";
    contentType = "application/x-www-form-urlencoded";
    body = qs.stringify(params);
  }

  if (method === "get") {
    _url += "?" + new URLSearchParams(params);
  }

  let options = {
    method,
    headers: {
      "Content-Type": contentType,
    },
  };

  const _access_token = get(access_token);

  if (_access_token) {
    options.headers["Authorization"] = "Bearer " + _access_token;
  }

  if (method !== "get") {
    options["body"] = body;
  }

  fetch(_url, options)
    .then((res) => {
      if (res.status === 204) {
        sucessCallback && sucessCallback();
        return;
      }
      res.json().then((json) => {
        if (res.status >= 200 && res.status < 300) {
          sucessCallback && sucessCallback(json);
        } else if (operation !== "login" && res.status === 401) {
          access_token.set("");
          username.set("");
          is_login.set(false);
          alert("로그인이 필요합니다.");
          push("/user-login");
        } else {
          failureCallback ? failureCallback(json) : alert(JSON.stringify(json));
        }
      });
    })
    .catch((e) => (failureCallback ? failureCallback(e) : alert(e)));
};
