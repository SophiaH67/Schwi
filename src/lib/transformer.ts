import _ from "./random";

export const info = (message: string | string[]) =>
  `${_(["Info: ", "Information: ", "Notice: "])}${
    Array.isArray(message) ? _(message) : message
  }`;

export const success = (message: string | string[]) =>
  `${_(["Success: ", "Answer: ", "Response: "])}${
    Array.isArray(message) ? _(message) : message
  }`;
