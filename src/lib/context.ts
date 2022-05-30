import { ErisClient } from "eris-boreas";
import { Message } from "discord.js";

export default class Context {
  public static async get(message: Message<boolean>, schwi: ErisClient) {
    const prompt = await schwi.redis.lRange(
      `schwi:context:${message.channelId}`,
      0,
      -1
    );
    return prompt;
  }

  public static async add(message: Message<boolean>, schwi: ErisClient) {
    console.log("Adding to context:", message.content);
    const last = await schwi.redis.lRange(
      `schwi:context:${message.channelId}`,
      -1,
      -1
    );
    if (last.length !== 0) {
      let [username, text] = last[0].split(":");
      if (username === message.author.username) {
        // Update the last item in the list to add the current message
        await schwi.redis.lSet(
          `schwi:context:${message.channelId}`,
          -1,
          `${message.author.username}: ${text}\n${message.content}`
        );
      } else {
        await schwi.redis.lPush(
          `schwi:context:${message.channelId}`,
          `${message.author.username}: ${message.content}`
        );
      }
    } else {
      await schwi.redis.lPush(
        `schwi:context:${message.channelId}`,
        `${message.author.username}: ${message.content}`
      );
    }
    // await schwi.redis.lTrim(`schwi:context:${message.channelId}`, 0, 9);
  }
}
