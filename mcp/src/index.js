// Worker entry. The entry module exports only the handler; logic lives in http.js.
import { routeRequest } from './http.js';

export default {
  fetch: (request, env) => routeRequest(request, env),
};
