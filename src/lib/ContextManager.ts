import { ErisClient } from "eris-boreas";
import { Message } from "discord.js";

export default class ContextManager {
  constructor(public schwi: ErisClient) {}
  public async get(message: Message<boolean>) {
    const prompt = await this.schwi.redis.lRange(
      `schwi:context:${message.channelId}`,
      0,
      10
    );
    return prompt;
  }

  public async add(message: Message<boolean>) {
    const last = await this.schwi.redis.lRange(
      `schwi:context:${message.channelId}`,
      0,
      0
    );
    if (last.length !== 0) {
      let [username, text] = last[0].split(":");
      if (username === message.author.username) {
        // Update the last item in the list to add the current message
        await this.schwi.redis.lSet(
          `schwi:context:${message.channelId}`,
          0,
          `${
            message.author.username
          }: ${text}\n${await this.replaceMentionsWithUsernames(
            message.content
          )}`
        );
      } else {
        this._addToContext(message);
      }
    } else {
      this._addToContext(message);
    }
  }

  private async _addToContext(message: Message<boolean>) {
    await this.schwi.redis.lPush(
      `schwi:context:${message.channelId}`,
      `${message.author.username}: ${await this.replaceMentionsWithUsernames(
        message.content
      )}`
    );
    await this.schwi.redis.lTrim(`schwi:context:${message.channelId}`, 0, 9);
  }

  public async replaceMentionsWithUsernames(message: string) {
    const mentions = message.match(/<@!?(\d+)>/g);
    if (mentions) {
      for (const mention of mentions) {
        const id = mention.match(/\d+/)?.[0];
        if (!id) continue;
        try {
          const user = await this.schwi.bot.users.fetch(id);
          message = message.replace(mention, `@"${user.username}"`);
        } catch (e) {
          //@ts-expect-error
          if (e.code === 10013) {
            // User not found
            continue;
          }
          throw e;
        }
      }
    }
    return message;
  }

  public replaceUsernamesWithMentions(message: string) {
    const usernames = message.match(/@"(.*?)"/g);
    if (usernames) {
      for (const username of usernames) {
        const user = this.schwi.bot.users.cache.find(
          (u) => u.username.toLowerCase() === username.toLowerCase()
        );
        if (!user) continue;
        message = message.replace(username, `<@${user.id}>`);
      }
    }
    return message;
  }
}
