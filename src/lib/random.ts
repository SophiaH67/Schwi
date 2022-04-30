export default function _(messages: string[]) {
  return messages[Math.floor(Math.random() * messages.length)];
}
